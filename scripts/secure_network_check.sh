#!/usr/bin/env bash
set -euo pipefail

# ============================================
# Secure network check – DNS + portkontroll
# ============================================

LOGFILE="network_check.log"
TARGET_DOMAIN="example.com"
TARGET_HOST="127.0.0.1"
TARGET_PORT="8080"

# Räknare för resultat
SUCCESS=0
ACTIONS=0

# Enkel loggfunktion med tidsstämpel
log() {
    local level="$1"
    local message="$2"
    printf "%s [%s] %s\n" "$(date -Is)" "$level" "$message" | tee -a "$LOGFILE"
}

log INFO "Kontroll startad"
log INFO "Mål domän: $TARGET_DOMAIN, mål host: $TARGET_HOST, port: $TARGET_PORT"

# ==========================
# DNS‑kontroll
# ==========================
ACTIONS=$((ACTIONS + 1))
if getent hosts "$TARGET_DOMAIN" >/dev/null 2>&1; then
    log OK "DNS fungerar för $TARGET_DOMAIN (namn kan översättas)"
    SUCCESS=$((SUCCESS + 1))
else
    log ERROR "DNS fungerar inte för $TARGET_DOMAIN (namn kan inte översättas)"
fi

# ==========================
# Port‑kontroll (HTTP HEAD)
# ==========================
ACTIONS=$((ACTIONS + 1))
if curl -I "http://$TARGET_HOST:$TARGET_PORT/" >/dev/null 2>&1; then
    log OK "Port $TARGET_PORT på $TARGET_HOST svarar (HTTP‑tjänst nåbar)"
    SUCCESS=$((SUCCESS + 1))
else
    log WARN "Port $TARGET_PORT på $TARGET_HOST svarar inte (ingen HTTP‑respons)"
fi

# ==========================
# Extra: lyssnande portar (ss)
# ==========================
ACTIONS=$((ACTIONS + 1))
if ss -tuln | grep -q "$TARGET_PORT"; then
    log OK "Port $TARGET_PORT finns i listan över lyssnande sockets (ss -tuln)"
    SUCCESS=$((SUCCESS + 1))
else
    log WARN "Port $TARGET_PORT syns inte som lyssnande i ss -tuln"
fi

# ==========================
# Sammanfattning
# ==========================
log INFO "Kontroll avslutad, $SUCCESS av $ACTIONS lyckade kontroller"

if [[ "$SUCCESS" -eq "$ACTIONS" ]]; then
    log INFO "Resultat: ALLA kontroller lyckades."
    echo "== Resultat: Alla kontroller OK =="
    exit 0
else
    log WARN "Resultat: En eller flera kontroller misslyckades. Se $LOGFILE för detaljer."
    echo "== Resultat: Granskning krävs =="
    exit 1
fi
