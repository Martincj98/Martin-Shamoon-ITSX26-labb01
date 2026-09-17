# Week 36 OCI Cloud Security Lab
## 1. Min OCI-miljö/Min lokala Linux-miljö/Min lokala WSL-miljö

                             ....              martinsh@CJ
              .',:clooo:  .:looooo:.           -----------
           .;looooooooc  .oooooooooo'          OS: Ubuntu 26.04.1 LTS (Resolute Raccoon) aarch64
        .;looooool:,''.  :ooooooooooc          Host: Virtual Machine (Hyper-V UEFI Release v4.1)
       ;looool;.         'oooooooooo,          Kernel: Linux 6.18.33.2-microsoft-standard-WSL2
      ;clool'             .cooooooc.  ,,       Uptime: 2 mins
         ...                ......  .:oo,      Packages: 544 (dpkg)
  .;clol:,.                        .loooo'     Shell: bash 5.3.9
 :ooooooooo,                        'ooool     Display (rdp-0): 1920x1200, 60 Hz
'ooooooooooo.                        loooo.    WM: WSLg 1.0.73.2 (Wayland)
'ooooooooool                         coooo.    Theme: Yaru [GTK3]
 ,loooooooc.                        .loooo.    Icons: Yaru [GTK3]
   .,;;;'.                          ;ooooc     Terminal: xterm-256color
       ...                         ,ooool.     CPU: Oryon 1*8 (8)
    .cooooc.              ..',,'.  .cooo.      GPU: Qualcomm(R) Adreno(TM) X1-45 GPU (128.00 MiB) [Integrated]
      ;ooooo:.           ;oooooooc.  :l.       Memory: 607.57 MiB / 15.37 GiB (4%)
       .coooooc,..      coooooooooo.           Swap: 0 B / 4.00 GiB (0%)
         .:ooooooolc:. .ooooooooooo'           Disk (/): 2.64 GiB / 1006.85 GiB (0%) - ext4
           .':loooooo;  ,oooooooooc            Disk (/mnt/c): 180.89 GiB / 951.37 GiB (19%) - 9p
               ..';::c'  .;loooo:'             Local IP (eth0): 172.30.221.200/20
                                               Battery (Microsoft Hyper-V Virtual Battery): 69% [Discharging]
                                               Locale: C.UTF-8
  
- VM-namn/hostnamn/WSL-maskinnamn: 
- Operativsystem: Ubuntu 26.04.01 
- Shape (Hårdvara, gäller alla): 
- Inloggningsmetod: SSH
---
## 2. Linux-kommandon
| Kommando | Vad visar det? | CIA-koppling |
|-----------|-----------|-----------|
| whoami | Visar vilken adress som är inloggad | Konfidentialitet och integritet|
| hostname | Visar datorns eller serverns namn | Integritet |
| pwd | Visar aktuell arbetskatalog |Integritet |
| uname -a | Visar arkitektur, OS och kernel| Tillgänglighet |
| uptime |Visar hur länge systemet varit igång | Tillgänglighet |
---
## 3. Hardening
| Kontroll | Risk | Vad gjorde jag? | Hur verifierade jag? | CIA |
|--------|-------|-----------|-----------|-----------|
|ID och behörighet| En användare kan ha större rättigheter än nödvändigt|Jag körde kommando "whoami", "id" och "groups". Användaren var "martinsh" och tillhörde "martinsh adm cdrom sudo dip plugdev users"  |Jämförde användarens grupper med rättigheterna, administrativa kommandon kördes bara med "sudo". | Konfidentialitet och integritet|

   Hardening
| Kontroll | Risk | Vad gjorde jag? | Hur verifierade jag? | CIA |
|-----------|-----------|-----------|-----------|-----------|
| Sytemuppdateringar|brister kan finnas installerade i paketet|kommandot "sudo apt update" sedan "apt list --upgradable" | Resultatet visade att ett paket kunde upgraderas, sedan installerade jag uppdateringen| Integritet,tillgänglighet och konfidentialitet|

   Hardening
| Kontroll | Risk | Vad gjorde jag? | Hur verifierade jag? | CIA |
|-----------|-----------|-----------|-----------|-----------|
|Loggar|Händelser och fel kan missas utan en loggkontroll | kommandot "ls/var/log"| Jag såg många loggar | Integritet och tillgänglighet. |

 Hardening
| Kontroll | Risk | Vad gjorde jag? | Hur verifierade jag? | CIA |
|-----------|-----------|-----------|-----------|-----------|
| SSH|felaktig ssh eller borttappad nyckel kan hindra åtkomst | jag anslöt med ssh| verifierade inloggningen med "whoami","hostname" och sedan "uptime"|Konfidentialitet, tillgänglighet och integritet.  |

---
## 4. Recovery-plan
### Vad kan gå fel?

Fel som kan hända är att WSL2 fungerar inte som väntat, att inte kunna ha internet.

### Hur upptäcker jag problemet?

Jag får fel meddelande såsom "connect to host X.X.X.X port 22: network in unreachable" trots att servern är på. 

### Vad kontrollerar jag först?

Det första man ska göra är att kolla ifall DNS fungerar, om det bara gäller WSL eller windows också och ifall windows brandvägg blockerar WSL.

### Hur återställer jag åtkomst?

Jag börjar med att starta om WSL nätverket "wsl --shutdown" eller att starta om windows nätverk. eller att WSL kanske bara behhövde uppdateras till senaste versionen. 

### När behöver jag hjälp?

ifall allt jag gjort inte fungerar så ber jag läraren om hjälp genom en annan enhet. 

---
## 5. Backup
### Vad har jag sparat?

Allt jag har dokumenterat i VS code finns  i Github under namnet "docs/week36-oci-cloud-security.md"

### Vad finns i GitHub?

Allt ovan och allt denna fil innehåller 

### Vad kan återskapas?

Miljön, kommandon och kontroller. 

### Vad går inte att återskapa?

Det jag inte kan återskapa är det som inte har säkerhetskopierats. 
---
## 6. Cleanup
### VM-instans
Behålls enligt läraren
### Diskar
Behålls enligt läraren
### Backuper
Behålls enligt läraren
### Publika IP-adresser
Behålls enligt läraren
### GitHub-evidens
Behålls enligt läraren. Finns på rätt plats 
---
## 7. CIA-reflektion
### Konfidentialitet
Skyddade det genom att inte publicera privata nycklar och rättigheter.
### Integritet
Jag kontrollerade användare och uppdateringar.
### Tillgänglighet
Kontrollerade SSH och kontrollerade uptime. 
---
## 8. Reflektion
### Vad fungerade bra?
Hjälpen jag fick av mina klasskamrater 
### Vad var svårt?
Hela uppgiften, eftersom jag inte har någon erfarenhet av detta tidigare.
### Vad lärde jag mig?
Mycket mer än vad jag trodde. 