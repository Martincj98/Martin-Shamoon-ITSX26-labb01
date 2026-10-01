# Security Automation Report

## Syfte 

Pythonprogrammet src/security_report.py ser till att läsa av loggarna för varje rad, den räknar Failed login per IP, den jämför IP-adresser mot indikatorlistan och sedan skriver output/security_report.txt. Dem raderna utan src= hoppar man över och redovisas. Programmet ser till att indata läses av, den kontaktar inga externa system och den blockerar inte något. 

## Rapport 

- Datakällor: auth.log, access.log, firewall.log, suspicious_ips.txt (katalog: data)  

- Misslyckade inloggningar: 4 gånger
- Unika IP-adresser med misslyckad inloggning: 2 gånger

203.0.113.15: 3 gånger

198.51.100.44: 1 gång

- Indikatorer i listan: 3
- IOC-träffar (unika IP-adresser): 3 

198.51.100.44: access.log 1, auth.log 1

203.0.113.15: access log 2, auth.log 3, firewall.log 1

203.0.113.99: firewall.log 1 

- Hoppade rader: 1 
auth.log rad 6: saknar src= -> "Malformed line without source"

- Observation
203.0.113.15 har flest misslyckade inloggningar (3 gånger) och finns i indikatorlistan

- Begränsning
Många misslyckade inloggningar eller en IOC-träff bevisar inte en attack. Det är oklart hur den aktuella indikatorlistan är, och datasetet är litet. Dem hoppade raderna ingår inte i antalen. 

## Analys

- Rådata - auth.log (rad 1-3): Failed login user=admin/root src=203.0.113.15. Rad 6 saknar src= och den hoppades över.

- Observation - 4 misslyckade inloggningar där 3 av dem är från 203.0.113.15. Adressen finns i indikatorlistan och syns också i access.log och firewall.log. 

- Slutsats - Tre misslyckade försök mot admin och root från en listad adress. Mönstret kan kännas som att någon försöker gissa lösenord, men inga bevis på attack. 

- Osäkerhet - Underlaget är litet så loggarna visar inte vem som använde adressen.

- Alternativ förklaring - En person kan ha glömt sitt lösenord

- Säkerhetsbetydelse - Försöken riktas mot viktiga konton och adresser syns i 3 loggar, manuell granskning behövs. 


## Testfall 

| Test | Indata | Förväntat | Resultat |
|---|---|---|---|
| Känt positivt | data/ | 4 Failed login, 3 IOC-träffar, 1 hoppad rad | OK | 
| Noll träffar | tests/testdata/no_hits/ | 0 Failed login, 0 IOC-träffar | OK |
| Formatfel | tests/testdata/malformed/ | 2 Failed login, 1 hoppad rad | OK |
| Saknad fil | katalog som inte finns | Felmeddelelande, exitkod 1 | OK |


**Begränsningar**
En IOC-träff är inte tillräckligt bevis och indikatorlistans aktualitet är fortfarande okänd. Dem hoppade raderna räknas inte. Tidsstämplar och IP-format valideras ej, datasetet är fortfarande för litet. 

**AI-redovisning**
 Chat GPT hjälpte till med stavningsfel och grammatiken. Sedan så kollade jag ifall jag var klar med uppgiften och ifall jag har missat någon del.

 **Min egen granskning** 

 Jag körde dem tre testfallen själv och såg till att kontrollera resultaten med dem förvämntade värden som jag fick. Jag räknade dem misslyckade inloggnigarna manuellt i auth.log och med grep och sedan jämförde mot rapporten. Jag såg till att koden läser av filerna i data/ i en stängd miljö så att inga externa system var med. Sedan granskade jag analysen och kontrollerade att IP inte är en angripare bara för att den finns i  indikator listan.  
