#!/usr/bin/env python3
"""
Awareness-Schulung: Passwort-Stärke & Brute-Force-Zeitabschätzung
==================================================================

Reine Rechen-Demo. Es werden KEINE Login-Versuche durchgeführt, nichts wird
gespeichert oder übertragen.

WICHTIG für Teilnehmende: Niemals ein echtes, aktiv genutztes Passwort eingeben!
Nur ausgedachte Beispiel-Passwörter verwenden.

Start:  python3 passwort_simulation.py
        python3 passwort_simulation.py --sichtbar   (Eingabe am Beamer sichtbar)
"""

import argparse
import getpass
import string

# Auszug typischer Passwörter aus öffentlichen Leak-Listen (für die Demo).
# Echte Angreifer nutzen Listen mit Milliarden Einträgen (z. B. "rockyou").
TOP_PASSWOERTER = {
    "123456", "123456789", "12345678", "password", "passwort", "qwertz",
    "qwerty", "hallo", "hallo123", "admin", "admin123", "welcome", "letmein",
    "iloveyou", "sommer2026", "winter2026", "andernach", "andernach1",
    "stadt123", "fussball", "schalke04", "master", "geheim", "test123",
}

# Rateversuche pro Sekunde – grobe Größenordnungen (Stand ca. 2025/26).
SZENARIEN = [
    ("Online-Login mit Sperre (z. B. 10 Versuche/Std.)", 10 / 3600),
    ("Online-Login ohne Sperre", 100),
    ("Offline, bcrypt-Hash, 1 GPU", 200_000),
    ("Offline, MD5/NTLM-Hash, 1 Gaming-GPU", 100_000_000_000),
    ("Offline, NTLM, GPU-Cluster (8 GPUs)", 1_000_000_000_000),
]


def zeichensatz_groesse(pw: str) -> int:
    """Ermittelt die Größe des genutzten Zeichenvorrats."""
    groesse = 0
    if any(c in string.ascii_lowercase for c in pw):
        groesse += 26
    if any(c in string.ascii_uppercase for c in pw):
        groesse += 26
    if any(c in string.digits for c in pw):
        groesse += 10
    if any(c in "äöüÄÖÜß" for c in pw):
        groesse += 7
    if any(not c.isalnum() for c in pw):
        groesse += 33
    return max(groesse, 1)


def als_lesbare_zeit(sekunden: float) -> str:
    einheiten = [
        ("Jahre", 365.25 * 86400), ("Tage", 86400), ("Stunden", 3600),
        ("Minuten", 60), ("Sekunden", 1),
    ]
    if sekunden < 1:
        return "sofort (< 1 Sekunde)"
    for name, faktor in einheiten:
        if sekunden >= faktor:
            wert = sekunden / faktor
            if name == "Jahre" and wert > 1e6:
                return f"{wert:.1e} Jahre (praktisch nicht knackbar)"
            return f"{wert:,.1f} {name}".replace(",", ".")
    return "sofort"


def main() -> None:
    parser = argparse.ArgumentParser(description="Passwort-Awareness-Demo")
    parser.add_argument("--sichtbar", action="store_true",
                        help="Eingabe sichtbar anzeigen (für Vorführung)")
    args = parser.parse_args()

    print(__doc__.split("Start:")[0])
    abfrage = "Beispiel-Passwort eingeben: "
    pw = input(abfrage) if args.sichtbar else getpass.getpass(abfrage)
    pw = pw.strip()
    if not pw:
        print("Leere Eingabe – Abbruch.")
        return

    print("\n--- 1) Wörterbuch-Angriff ---")
    basis = pw.lower().rstrip("0123456789!?.")
    if pw.lower() in TOP_PASSWOERTER or basis in TOP_PASSWOERTER:
        print("⚠  Treffer in der Liste häufiger Passwörter!")
        print("   Ein Angreifer probiert solche Passwörter ZUERST –")
        print("   geknackt in Sekundenbruchteilen, egal wie lang.")
    else:
        print("✓  Nicht in der (kleinen) Demo-Liste.")
        print("   Hinweis: Echte Listen sind millionenfach größer.")

    n = zeichensatz_groesse(pw)
    kombis = n ** len(pw)
    print("\n--- 2) Reines Durchprobieren (Brute Force) ---")
    print(f"Länge: {len(pw)} Zeichen | Zeichenvorrat: {n}")
    print(f"Mögliche Kombinationen: {n}^{len(pw)} ≈ {kombis:.2e}")
    print("Durchschnittliche Zeit (halber Suchraum):")
    for name, rate in SZENARIEN:
        print(f"  • {name:<50} {als_lesbare_zeit(kombis / 2 / rate)}")

    print("\n--- Merksätze ---")
    print("  • Länge schlägt Komplexität: lieber 4–5 zufällige Wörter.")
    print("  • Für jeden Dienst ein eigenes Passwort → Passwort-Manager.")
    print("  • MFA aktivieren – dann reicht ein geknacktes Passwort nicht.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nAbgebrochen.")
