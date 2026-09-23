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

