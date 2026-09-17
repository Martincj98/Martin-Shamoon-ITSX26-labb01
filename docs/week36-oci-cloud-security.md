# Week 36 OCI Cloud Security Lab
## 1. Min OCI-miljö/Min lokala Linux-miljö/Min lokala WSL-miljö
  
- VM-namn/hostnamn/WSL-maskinnamn: 
- Operativsystem: 
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
|----------|-----------|-----------|-----------|-----------|
|whoami | ID och behörighet | En användare kan ha större rättigheter än nödvändigt| Jag körde kommando "whoami", "id" och "groups". Användaren var "martinsh" och tillhörde "martinsh adm cdrom sudo dip plugdev users"  |Jämförde användarens grupper med rättigheterna, administrativa kommandon kördes bara med "sudo". | Konfidentialitet och integritet.
---
## 4. Recovery-plan
### Vad kan gå fel?
### Hur upptäcker jag problemet?
### Vad kontrollerar jag först?
### Hur återställer jag åtkomst?
### När behöver jag hjälp?
---
## 5. Backup
### Vad har jag sparat?
### Vad finns i GitHub?
### Vad kan återskapas?
### Vad går inte att återskapa?
---
## 6. Cleanup
### VM-instans
### Diskar
### Backuper
### Publika IP-adresser
### GitHub-evidens
---
## 7. CIA-reflektion
### Konfidentialitet
### Integritet
### Tillgänglighet
---
## 8. Reflektion
### Vad fungerade bra?
### Vad var svårt?
### Vad lärde jag mig?