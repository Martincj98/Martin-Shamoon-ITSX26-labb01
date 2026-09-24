LOG_FILE="network_check.log"

function log(){
    echo -e "$(date -Is): $*" >> "$LOG_FILE"
}

function port_check(){
    if ss -tuln | grep 8080 > /dev/null; then
        log [PASSED] "Port Check \n$(ss -tuln | grep LISTEN)"
    else
        log [FAILED] "Port Check \n$(ss -tuln | grep LISTEN)"
    fi
}

function dns_check(){
    if dig +short example.com | grep -q .; then
        log [PASSED] "-> DNS CHECK"
    else
        log [FAILED] "-> DNS CHECK"
    fi
}

main (){
     dns_check
     port_check
}