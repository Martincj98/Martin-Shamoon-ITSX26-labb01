"""
security_report.py - ITSX26 kursvecka 5 (vecka 39)

Läser loggfiler i data/, räknar misslyckade inloggningar, jämför käll-IP
mot suspicious_ips.txt och skriver en rapport till output/security_report.txt.

Programmet läser bara indata (ändrar inga originalfiler), kontaktar inga
externa system och blockerar ingenting.

Körs från projektroten:
    python3 src/security_report.py
    python3 src/security_report.py <datakatalog> <rapportfil>   (används vid test)
"""

import os
import sys

LOG_FILES = ["auth.log", "access.log", "firewall.log"]
IOC_FILE = "suspicious_ips.txt"


def read_lines(path):
    """Läser en fil i läsläge. Avslutar med tydligt fel om filen saknas."""
    try:
        with open(path, encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"FEL: Hittar inte {path}. Kör programmet från projektroten.")
        sys.exit(1)


def get_src_ip(line):
    """Returnerar IP-adressen i fältet src=, eller None om fältet saknas."""
    for field in line.split():
        if field.startswith("src="):
            return field.split("=", 1)[1]
    return None


def load_indicators(path):
    """Läser indikatorlistan till en set (dubbletter blir ett värde)."""
    return set(read_lines(path))


def analyze_log(path):
    """
    Går igenom en logg rad för rad.
    Returnerar: lista med (radnummer, IP, rad) och lista med hoppade rader.
    """
    events = []
    skipped = []
    for number, line in enumerate(read_lines(path), start=1):
        ip = get_src_ip(line)
        if ip is None:
            skipped.append(f"rad {number}: saknar src= -> '{line}'")
            continue
        events.append((number, ip, line))
    return events, skipped


def count_failed_logins(auth_events):
    """Räknar 'Failed login' per käll-IP med en dictionary."""
    counts = {}
    for _, ip, line in auth_events:
        if "Failed login" in line:
            counts[ip] = counts.get(ip, 0) + 1
    return counts


def match_indicators(all_events, indicators):
    """Räknar hur många rader per IP och loggfil som matchar indikatorlistan."""
    matches = {}
    for file_name, events in all_events.items():
        for _, ip, _ in events:
            if ip in indicators:
                matches.setdefault(ip, {})
                matches[ip][file_name] = matches[ip].get(file_name, 0) + 1
    return matches


def write_report(lines, path):
    """Skriver rapporten till en ny fil (skapar output/ vid behov)."""
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main():
    data_dir = sys.argv[1] if len(sys.argv) > 1 else "data"
    report_path = sys.argv[2] if len(sys.argv) > 2 else "output/security_report.txt"

    # 1. Läs och filtrera
    indicators = load_indicators(os.path.join(data_dir, IOC_FILE))
    all_events = {}
    all_skipped = {}
    for file_name in LOG_FILES:
        events, skipped = analyze_log(os.path.join(data_dir, file_name))
        all_events[file_name] = events
        all_skipped[file_name] = skipped

    # 2. Räkna och jämför
    failed = count_failed_logins(all_events["auth.log"])
    matches = match_indicators(all_events, indicators)

    # 3. Rapport (sorterad så att samma indata ger samma rapport)
    report = [
        "=" * 50,
        "ITSX26 SECURITY REPORT",
        "=" * 50,
        f"Datakällor: {', '.join(LOG_FILES)}, {IOC_FILE} (katalog: {data_dir})",
        "",
        f"Misslyckade inloggningar: {sum(failed.values())}",
        f"Unika IP med misslyckad inloggning: {len(failed)}",
    ]
    for ip, count in sorted(failed.items(), key=lambda item: (-item[1], item[0])):
        report.append(f"  {ip}: {count}")

    report.append("")
    report.append(f"Indikatorer i listan: {len(indicators)}")
    report.append(f"IOC-träffar (unika IP): {len(matches)}")
    for ip in sorted(matches):
        per_file = ", ".join(f"{name} {n}" for name, n in sorted(matches[ip].items()))
        report.append(f"  {ip}: {per_file}")

    report.append("")
    total_skipped = sum(len(s) for s in all_skipped.values())
    report.append(f"Hoppade rader (formatfel): {total_skipped}")
    for file_name in LOG_FILES:
        for text in all_skipped[file_name]:
            report.append(f"  {file_name} {text}")

    report.append("")
    report.append("OBSERVATION")
    if failed:
        top_ip = sorted(failed.items(), key=lambda item: (-item[1], item[0]))[0][0]
        in_list = "finns" if top_ip in indicators else "finns inte"
        report.append(f"  {top_ip} har flest misslyckade inloggningar ({failed[top_ip]}) "
                      f"och {in_list} i indikatorlistan.")
    else:
        report.append("  Inga misslyckade inloggningar hittades.")

    report.append("")
    report.append("BEGRÄNSNING")
    report.append("  En IOC-träff eller många misslyckade inloggningar bevisar inte en attack.")
    report.append("  Det är okänt hur aktuell indikatorlistan är, och datasetet är litet.")
    report.append("  Hoppade rader ingår inte i antalen.")
    report.append("=" * 50)

    write_report(report, report_path)
    print("\n".join(report))
    print(f"\nRapport sparad i {report_path}")


if __name__ == "__main__":
    main()
