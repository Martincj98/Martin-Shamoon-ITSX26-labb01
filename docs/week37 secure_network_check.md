# Del A - Miljöbeskrivning

- Ange om du använder Oracle Cloud, WSL eller Linux på PC.

Jag använder Docker med Ubuntu som operativsystem på en Linux-baserad dator.
Docker används för att isolera miljön och undvika konflikter med Git.

- Beskriv operativsystem/distribution på en rimlig nivå.

Ett operativsystem är mjukvara som kommunicerar direkt med hårdvaran och styr hur resurser fördelas.
$ uname -r
7.2.6-arch2-1
Ubuntu 26.04 körs i en Docker-container och delar kernel med värdmaskinen.

- Redovisa relevanta nätverksinterface utan att publicera känsliga uppgifter.

$ ip -br a
lo           UNKNOWN        127.0.0.1/8 ::1/128
eth0@if6     UP             172.17.0.2/16
Det finns två nätverksinterface: loopback och ett Ethernet-interface som används av containern.

- Förklara skillnaden mellan lokal adress, privat adress och publik adress där det är relevant.

En lokal adress (loopback) används för intern kommunikation i samma maskin.
En privat adress tilldelas inom det lokala nätverket, exempelvis av router eller Docker.
En publik adress är den externa adress som används för kommunikation med internet.
All trafik från privata adresser passerar routern innan den når externa mål.

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
Loggar och evidens finns under /agent prompts/evidence-agent.md





