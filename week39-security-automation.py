"""
security_report.py - ITSX26 vecka 39
Läser loggar i data/, räknar misslyckade inloggningar per IP, jämför IP mot
suspicious_ips.txt och skriver output/security_report.txt.
Indata läses bara (ändras inte). Inga externa anrop, ingen blockering.

Kör från projektroten:  python3 src/security_report.py [datakatalog] [rapportfil]
"""
import os
import sys

DATA = sys.argv[1] if len(sys.argv) > 1 else "data"
REPORT = sys.argv[2] if len(sys.argv) > 2 else "output/security_report.txt"
LOGS = ["auth.log", "access.log", "firewall.log"]


def read_lines(name):
    """Läser en fil i läsläge. Ger tydligt fel om filen saknas."""
    path = os.path.join(DATA, name)
    try:
        with open(path, encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"FEL: Hittar inte {path}. Kör från projektroten.")
        sys.exit(1)


def get_ip(line):
    """Returnerar IP från fältet src=, eller None om fältet saknas."""
    for field in line.split():
        if field.startswith("src="):
            return field[4:]
    return None


def main():
    indicators = set(read_lines("suspicious_ips.txt"))  # set: dubbletter räknas en gång
    failed, matches, skipped = {}, {}, []

    for log in LOGS:
        for number, line in enumerate(read_lines(log), start=1):
            ip = get_ip(line)
            if ip is None:                                  # formatfel redovisas
                skipped.append(f"  {log} rad {number}: saknar src= -> '{line}'")
                continue
            if log == "auth.log" and "Failed login" in line:
                failed[ip] = failed.get(ip, 0) + 1
            if ip in indicators:
                matches[ip] = matches.get(ip, 0) + 1

    ranked = sorted(failed.items(), key=lambda item: (-item[1], item[0]))
    report = ["ITSX26 SECURITY REPORT",
              f"Datakällor: {', '.join(LOGS)}, suspicious_ips.txt",
              f"Misslyckade inloggningar: {sum(failed.values())}"]
    report += [f"  {ip}: {count}" for ip, count in ranked]
    report += [f"IOC-träffar (loggrader per listad IP): {len(matches)} IP"]
    report += [f"  {ip}: {matches[ip]}" for ip in sorted(matches)]
    report += [f"Hoppade rader: {len(skipped)}"] + skipped

    report.append("OBSERVATION")
    if ranked:
        ip, count = ranked[0]
        listed = "finns" if ip in indicators else "finns inte"
        report.append(f"  {ip} har flest misslyckade inloggningar ({count}) och {listed} i indikatorlistan.")
    else:
        report.append("  Inga misslyckade inloggningar hittades.")
    report += ["BEGRÄNSNING",
               "  En IOC-träff eller misslyckade inloggningar bevisar inte en attack.",
               "  Indikatorlistans aktualitet är okänd. Hoppade rader ingår inte i antalen."]

    os.makedirs(os.path.dirname(REPORT) or ".", exist_ok=True)
    with open(REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(report) + "\n")
    print("\n".join(report))


if __name__ == "__main__":
    main()
