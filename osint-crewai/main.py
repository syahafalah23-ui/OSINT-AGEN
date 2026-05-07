#!/usr/bin/env python3
"""
OSINT Tools menggunakan CrewAI
Dibuat sebagai project consultant pribadi
"""

import os
import sys
import argparse
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from src.crew import OsintCrew


def parse_args():
    parser = argparse.ArgumentParser(
        description="OSINT Intelligence Gathering Tool menggunakan CrewAI"
    )
    parser.add_argument(
        "--target",
        type=str,
        help="Target OSINT (username, email, domain, IP, atau nama lengkap)",
    )
    parser.add_argument(
        "--type",
        type=str,
        choices=["username", "email", "domain", "ip", "fullname", "auto"],
        default="auto",
        help="Tipe target (default: auto-detect)",
    )
    parser.add_argument(
        "--output",
        type=str,
        choices=["markdown", "json", "both"],
        default="markdown",
        help="Format output laporan",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Tampilkan proses detail",
    )
    return parser.parse_args()


def validate_env():
    """Cek environment variables yang diperlukan"""
    required = ["OPENAI_API_KEY"]
    optional = {
        "SHODAN_API_KEY": "Shodan (IP/Domain intel)",
        "HUNTER_API_KEY": "Hunter.io (Email lookup)",
        "HIBP_API_KEY": "HaveIBeenPwned (Breach check)",
        "VIRUSTOTAL_API_KEY": "VirusTotal (Malware/Domain scan)",
        "IPINFO_TOKEN": "IPInfo (IP geolocation)",
    }

    missing_required = [k for k in required if not os.getenv(k)]
    if missing_required:
        print(f"[ERROR] API key wajib tidak ditemukan: {', '.join(missing_required)}")
        print("Silakan buat file .env dari .env.example")
        sys.exit(1)

    print("\n=== OSINT CrewAI Tools ===")
    print("API Keys tersedia:")
    for key, desc in optional.items():
        status = "✓" if os.getenv(key) else "✗ (disabled)"
        print(f"  {status} {desc}")
    print()


def main():
    args = parse_args()
    validate_env()

    # Interactive mode jika target tidak diberikan
    if not args.target:
        print("Mode interaktif - masukkan target OSINT")
        args.target = input("Target (username/email/domain/IP/nama): ").strip()
        if not args.target:
            print("[ERROR] Target tidak boleh kosong")
            sys.exit(1)

    print(f"Target    : {args.target}")
    print(f"Tipe      : {args.type}")
    print(f"Output    : {args.output}")
    print(f"Timestamp : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 40)

    # Jalankan OSINT Crew
    crew = OsintCrew(
        target=args.target,
        target_type=args.type,
        output_format=args.output,
        verbose=args.verbose,
    )
    result = crew.run()

    print("\n=== OSINT SELESAI ===")
    print(f"Laporan disimpan di folder: outputs/")
    return result


if __name__ == "__main__":
    main()
