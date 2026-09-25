# Del A - Miljöbeskrivning

- Ange om du använder Oracle Cloud, WSL eller Linux på PC.

Jag använder WSL med Ubuntu som operativsystem på en Linux-baserad dator.
WSL används för att isolera miljön och undvika konflikter med Git.

- Beskriv operativsystem/distribution på en rimlig nivå.

Ett operativsystem är mjukvara som kommunicerar direkt med hårdvaran och styr hur resurser fördelas.
$ uname -r
7.2.6-arch2-1
Ubuntu 26.04 körs i en WSL-container och delar kernel med värdmaskinen.

- Redovisa relevanta nätverksinterface utan att publicera känsliga uppgifter.

$ ip -br a
lo               UNKNOWN        127.0.0.1/8 10.255.255.254/32 ::1/128
eth0             UP             172.30.221.200/20 fe80::215:5dff:fe31:10f4/64
Det finns två nätverksinterface: loopback och ett Ethernet-interface som används av containern.

- Förklara skillnaden mellan lokal adress, privat adress och publik adress där det är relevant.

En lokal adress (loopback) används för intern kommunikation i samma maskin.
En privat adress tilldelas inom det lokala nätverket, exempelvis av router eller WSL.
En publik adress är den externa adress som används för kommunikation med internet.
All trafik från privata adresser passerar routern innan den når externa mål.

- Beskriv vilka begränsningar din miljö innebär för uppgiften och vilka skillnader du observerar jämfört med
lärardemonstrationen i OCI. Skillnader är förväntade och påverkar inte bedömningen när du förklarar dem korrekt.

Nätverksmiljön är isolerad i WSL. I OCI körs systemen direkt på en virtuell maskin med full åtkomst till nätverket.
I min miljö körs Ubuntu i en container som använder ett eget virtuellt nätverk. 


# Del B - Manuella Observation

| ip adress, hostname -I     | Ser två interface och IPv4                     |

| ip route                   | default route visas                             |

| getent hosts               | Domännamn kan översättas till IP-adress         |

| ss -tuln                   | Port 631 är öppen, används för nätverksutskrifter |

| curl 127.0.0.1:8080        | Ingen anslutning till porten                    |

| ps                         | Visar aktiva processer, bland annat bash och ps |

# Del C - Bygg Bash Verktyg
Scriptet finns under /scripts/secure_network_check.sh

# Del D - Testning
Loggar och evidens finns under /agent prompts/evidence-agent.md (Startar Python server utanför script)

# Del E - CIA-analys

1. Konfidentialitet: Vilka uppgifter i nätverksutdata kan vara känsliga, och hur sanerar du dem?
Information som kan identifiera en specifik maskin, som IP‑adresser eller hårdvaruidentifierare, bör tas bort eller ersättas. Adresser kan anonymiseras genom att bytas ut mot generiska domännamn, och MAC‑adresser bör inte inkluderas.

2. Integritet: Hur hjälper loggar, versionshistorik, tydliga statusar och kontroller till att skapa tillit till resultatet?
Loggar med tidsangivelser gör det möjligt att följa händelser i rätt ordning. Klara statusmeddelanden och återkommande kontroller skapar en spårbar struktur som visar vad som har skett och när det skedde.

3. Tillgänglighet: Hur visar DNS, route, tjänst och port om en funktion är tillgänglig?
DNS‑uppslag visar om ett namn kan översättas. Test av tjänster med exempelvis curl visar om de svarar. Portar kan kontrolleras med ss eller liknande verktyg för att se om de är öppna och nåbara.

4. Avvägning: Ge ett exempel där en säkerhetsåtgärd kan försämra tillgänglighet om den konfigureras fel.
Om en brandvägg blockerar en port som används för fjärranslutning, exempelvis port 22, kan legitima anslutningar stoppas och åtkomst förhindras.

# Del F – Reflektion och förbättring

1. Vilken kontroll gav mest värde och varför?

DNS‑kontrollen gav mest värde eftersom den direkt visar om namntjänsten fungerar. Om DNS fallerar spelar det ingen roll om portar eller tjänster är öppna, eftersom systemet inte kan hitta målet. Den kontrollen ger därför en tydlig indikation på om nätverket fungerar på en grundläggande nivå.

2. Vilken miljöskillnad påverkade ditt arbete?

Att köra verktyget i en containeriserad miljö påverkade arbetet mest. WSL använder ett eget virtuellt nätverk, vilket innebär att IP‑adresser och routing skiljer sig från värdmaskinen. Det gjorde att vissa kommandon gav andra resultat än om de körts direkt på host‑systemet.

3. Vilket fel var svårast att tolka?

Det svåraste felet att tolka var när curl inte fick svar från porten. Det är inte direkt tydligt om problemet beror på att tjänsten inte körs, att porten är stängd, att brandväggen blockerar trafiken eller att adressen pekar fel. Flera möjliga orsaker gör felet mer komplext att förstå.

4. Vad skulle du förbättra i en version 2?

En förbättrad version skulle inkludera mer detaljerade felmeddelanden och en tydligare sammanställning av orsaker. Dessutom skulle verktyget kunna kontrollera om tjänsten faktiskt körs lokalt, inte bara om porten svarar. Automatiska sanity‑checks för nätverksmiljön skulle också vara värdefulla.

5. Hur kan verktyget användas i en verklig drift- eller säkerhetsprocess utan att bli riskabelt?

Verktyget kan användas som ett enkelt hälsotest för nätverkstjänster, så länge det inte loggar känsliga adresser eller interna strukturer. Genom att anonymisera IP‑adresser, undvika att samla in onödig information och begränsa loggarnas innehåll kan det användas säkert i driftmiljöer utan att exponera intern nätverksdata.






