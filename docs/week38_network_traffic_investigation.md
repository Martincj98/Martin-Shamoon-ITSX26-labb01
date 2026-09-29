# Network Traffic Investigation – ITSX26 vecka 38

- **Fil:** week38_packet_journey_basic 
- **Spår:** Reservspår 
- **SHA-256:** `9042a0fd0190305c0b68a4126837a240d331c446d0894cb94303849d20d9540e`
- **Miljö:** WSL 2 med Ubuntu
- **Analysdatum:** 2026-09-30

---

## Del A – Miljö och metod

Fångstens omfattning: Reserv-pcapen innehåller 34 paket och omfattar cirka 1,65 sekunder.

Jag använder WSL 2 med Ubuntu på min Windows-dator.

Jag valde reservspåret. I WSL 2 körs Ubuntu i en liten virtuell maskin bakom Windows NAT. Interfacet `eth0` i WSL ser därför bara WSL:s egen interna trafik och inte datorns riktiga nätverkskort. Jag tyckte inte att jag kunde få en bra och avgränsad fångst på det sättet, så jag analyserade lärarens pcap i stället.

Pcap-filen ligger bara lokalt på min dator och inte i GitHub. Jag behövde inte sanera något, eftersom filen redan använder testadresser (`192.0.2.x` och `198.51.100.x`), domänen `training.example` och påhittade MAC-adresser. Det finns inga lösenord eller cookies i filen.

Skillnaden mot lärarens OCI-demo är att en OCI-maskin har en privat IP och en publik IP via OCI:s gateway, och att den har OCI:s egna brandväggsregler. I WSL går trafiken först genom Windows NAT och sedan genom min hemrouter.

Kommandon jag använde:

```bash
sha256sum week38_packet_journey_basic.pcap
tcpdump -nn -r week38_packet_journey_basic.pcap
tcpdump -nn -A -r week38_packet_journey_basic.pcap 'tcp port 80'
```

I Wireshark använde jag filtren `dns`, `icmp`, `tcp`, `http` och `tls`.

---

## Del B – Paketets väg

Flödet jag följer är när klienten hämtar `http://training.example/index.html`.

```
Program på klienten
   → DNS-fråga till 192.0.2.53 (pkt 1–2)
   → Klienten 192.0.2.10 skickar till gatewayen (default route)
   → Router/brandvägg, kanske NAT
   → Server 198.51.100.50, TCP port 80 (pkt 9–18)
```

- **Lokal IP:** Klienten har `192.0.2.10` (syns i pcap).
- **DNS:** Klienten frågar efter `training.example` och får svaret `198.51.100.50` (syns i pcap, pkt 1–2).
- **Default route/gateway:** Alla paket går till samma MAC-adress (`02:00:00:00:00:01`).
- **Privat/publik adress:** Båda adresserna är testadresser. I övningen fungerar `192.0.2.10` som den interna klienten och `198.51.100.50` som den externa servern.
- **Brandvägg:** Klientens utgående regler, routern och serverns inkommande regler kan alla stoppa trafiken. Här gick allt igenom, och det finns inga RST eller felmeddelanden.
- **Transport:** TCP från port 41000 till port 80 (syns i pcap).
- **Applikation:** HTTP, `GET /index.html` (syns i pcap).

---

## Del C – Protokollinventering

| Protokoll | Paket | Vad jag ser | Vad det betyder |
|---|---|---|---|
| DNS | 1–2, 33–34 | Fråga efter `training.example` ger svaret `198.51.100.50`. Fråga efter `missing.training.example` ger **NXDOMAIN**. | DNS fungerar. NXDOMAIN betyder att namnet inte finns, inte att nätet är trasigt. |
| ICMP | 3–8 | 3 ping (echo request) och 3 svar (echo reply). Tiden fram och tillbaka är ca 50 ms. | Servern går att nå. Man vet däremot inte om port 80 eller 443 är öppen. Om en server inte svarar på ping betyder det inte att den är nere, för ping blockeras ofta. |
| TCP | 9–11, 19–21 | SYN, SYN/ACK, ACK två gånger: till port 80 och till port 443. Båda stängs med FIN. | Båda anslutningarna fungerar. Det finns inga RST eller omsändningar. |
| HTTP | 12, 14 | `GET /index.html`, `Host: training.example`, `User-Agent: ITSX26-Lab`. Svaret är `200 OK` med texten `Hello from ITSX26 lab`. | Allt går att läsa i klartext. |
| TLS/HTTPS | 22, 24, 26, 28 | ClientHello (22), ServerHello (26) och Application Data (24, 28). TLS 1.2. | Man ser IP, port, TLS-version och chiffer. Innehållet ska vara krypterat. |

---

## Del D – Två flöden

### Flöde 1: HTTP (pkt 9–18)

`192.0.2.10:41000 → 198.51.100.50:80`, TCP + HTTP

**Ordning:**

1. Handskakning (pkt 9–11)
2. GET-förfrågan (pkt 12)
3. ACK (pkt 13)
4. `200 OK` (pkt 14)
5. ACK (pkt 15)
6. Stängning med FIN/ACK (pkt 16–18)

- **Förväntat:** Handskakning, förfrågan, svar och sedan stängning.
- **Observerat:** Allt ser normalt ut. Sekvens- och ACK-nummer stämmer.
- **Avvikelser:** Inga avvikelser.
- **Alternativ förklaring:** Tiden mellan alla paket är exakt 50 ms, vilket är ovanligt i riktig trafik.
- **Behövs för säkrare slutsats:** Serverns logg och en fångst på serversidan.

### Flöde 2: TLS (pkt 19–32)

`192.0.2.10:41001 → 198.51.100.50:443`, TCP + TLS

**Ordning:**

1. Handskakning (pkt 19–21)
2. ClientHello (22)
3. Application Data från klienten (24)
4. ServerHello (26)
5. Application Data från servern (28)
6. Stängning med FIN (30–32)

- **Förväntat:** ClientHello → ServerHello → certifikat → nyckelutbyte → **sedan** krypterad data.
- **Observerat, med avvikelser:**
  - Klienten skickar data (24) **innan** servern har svarat med ServerHello (26). Det ska inte gå, eftersom inga nycklar finns än.
  - Inget certifikat skickas.
  - Servern väljer chiffret `TLS_NULL_WITH_NULL_NULL`, alltså ingen kryptering.
  - Den "krypterade" datan går att läsa: `ENCRYPTED_CLIENT_DATA`.
- **Alternativ förklaring:** Troligen är filen gjord med ett skript som en förenklad TLS-modell. I ett riktigt nät kan det också bero på en felaktig klient eller på att paket saknas i fångsten, men TCP-numren visar inga luckor.
- **Behövs för säkrare slutsats:** En egen fångst av en riktig HTTPS-anslutning där certifikatet syns.

---

## Del E – HTTP jämfört med TLS

| | HTTP (pkt 9–18) | TLS (pkt 19–32) |
|---|---|---|
| Synlig metadata | IP, port 80, tider, storlekar | IP, port 443, tider, storlekar, TLS-version, chiffer |
| Läsbar data | Allt: URL, headers och sidans text | Normalt inget. Här syns platshållartext eftersom filen är en övning. |
| Felsökning | Man ser exakt vad som frågades efter och vilket svar som kom | Man ser om anslutningen och handskakningen fungerar, men inte innehållet |
| Risk | Alla på vägen kan läsa allt, även lösenord eller cookies om sådana fanns | Vem som pratar med vem, när och hur mycket syns ändå. DNS-frågan (pkt 1) är okrypterad och visar namnet. |

---

## Del F – Brandvägg och hardening

Jag väljer HTTP-flödet (pkt 9–18). Klienten behöver en **utgående** regel som tillåter TCP port 80. Servern behöver en **inkommande** regel som tillåter TCP port 80. Svarspaketen till klienten släpps in eftersom brandväggen kommer ihåg anslutningen (established).

**Lyssnar vs. tillåts:** Att en tjänst lyssnar på en port (syns med `ss -tulpn`) betyder att den väntar på trafik. Brandväggen bestämmer om trafiken får komma fram. Båda måste stämma för att det ska fungera.

**Default deny:** All inkommande trafik blockeras, och man öppnar bara det som behövs. I pcapen startar klienten alla anslutningar själv, så den behöver inga öppna inkommande portar.

**Hardening:** Flödena (DNS, ping, HTTP och HTTPS ut från klienten) är rimliga för en vanlig klient. Det som inte är bra är HTTP i klartext. Det borde vara HTTPS i stället.

---

## Del G – CIA och evidens

| | |
|---|---|
| **Konfidentialitet** | Pcapen kan innehålla känsliga saker, till exempel HTTP i klartext (pkt 12–14). Därför ligger den bara lokalt. Med TLS döljs innehållet. |
| **Integritet** | Jag visar att analysen hör till rätt fil med filnamnet, SHA-256-hashen och paketnumren. |
| **Tillgänglighet** | DNS svarar (pkt 2), ping svarar (pkt 4, 6, 8), TCP-anslutningarna fungerar och HTTP ger `200 OK`. Allt fungerar under de 1,65 sekunderna. |
| **Evidenskvalitet** | Fångsten är väldigt kort och tagen bara från klientens sida, så NAT och brandvägg syns inte. Certifikat saknas.|

---

## Del H – Slutsats

**Vad hände?** Klienten slog upp `training.example` med DNS, pingade servern och hämtade en sida med HTTP (`200 OK`). Sedan gjorde den en TLS-anslutning på port 443 och frågade till sist efter ett namn som inte fanns (NXDOMAIN).

**Säkrast:** DNS, ping, TCP-handskakningarna och HTTP-innehållet, eftersom de syns direkt i paketen.

**Osäkert:** Vägen via router, NAT och brandvägg är min tolkning. TLS-flödet följer inte riktig TLS, så jag drar inga slutsatser om krypteringen.

**Rekommendation:** Använd HTTPS i stället för HTTP, eftersom pcapen visar att HTTP går att läsa helt. 

**Nästa steg:** Göra en egen kort fångst av riktig HTTPS-trafik och titta på brandväggsloggar och serverloggar.

## AI-användning 

Jag använde AI som stöd för stavfel och layout för dokumentet. Jag kontrollerade ifall jag missade någon del i uppgiften genom AI. AI användes också för grammatiska förslag och ändringar. 

---