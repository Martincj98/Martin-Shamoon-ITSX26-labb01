LOGFILE="network.log"
TARGET="example.com"
declare -i SUCCESS="0"
declare -i ACTIONS="0"

log() {
    printf "%s [%s] %s\n" "$(date -Is)" "$1" "$2" | tee -a "$LOGFILE"
}

log INFO "Kontroll startad"

ACTIONS=$ACTIONS+1
if getent hosts "$TARGET" >/dev/null;
    then log OK "DNS fungerar för $TARGET"
    SUCCESS=$SUCCESS+1
else
    log ERROR "DNS fungerar inte för $TARGET"
fi

ACTIONS="$ACTIONS+1"
if curl -I http://127.0.0.1:8080/>/dev/null 2>&1;
    then log OK "Port 8080 svarar"
    SUCCESS="$SUCCESS+1"
else
    log WARN "Port 8080 svarar inte"
fi

log INFO "Kontroll avslutad, $SUCCESS av $ACTIONS lyckade calls"

2026-09-24T08:47:33+02:00 [INFO] Kontroll startad
2026-09-24T08:47:33+02:00 [INFO] Mål domän: example.com, mål host: 127.0.0.1, port: 8080

2026-09-24T08:47:33+02:00 [OK] DNS fungerar för example.com 

2026-09-24T08:47:33+02:00 [WARN] Port 8080 på 127.0.0.1 svarar inte 

2026-09-24T08:47:33+02:00 [OK] Port 8080 finns i listan över lyssnande sockets 

2026-09-24T08:47:33+02:00 [INFO] Kontroll avslutad, 2 av 3 lyckade kontroller
2026-09-24T08:47:33+02:00 [WARN] Resultat: En eller flera kontroller misslyckades. 
