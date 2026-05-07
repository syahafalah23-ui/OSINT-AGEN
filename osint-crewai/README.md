# 🔍 OSINT CrewAI Intelligence Tools

> Multi-agent OSINT framework menggunakan CrewAI — otomatis investigasi username, email, domain, dan IP address

[![CI Status](https://github.com/YOUR_USERNAME/osint-crewai/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/osint-crewai/actions)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![CrewAI](https://img.shields.io/badge/CrewAI-0.67+-orange.svg)](https://crewai.com)

## 🏗️ Arsitektur

```
INPUT TARGET (username/email/domain/IP/nama)
         ↓
CREW ORCHESTRATOR (auto-detect tipe target)
         ↓
┌──────────┬──────────┬──────────┬──────────┐
│ Social   │ Domain   │ Email    │ IP/Net   │
│ Scout    │ Intel    │ Hunter   │ Recon    │
└──────────┴──────────┴──────────┴──────────┘
         ↓
REPORT WRITER AGENT
         ↓
OUTPUT (Markdown / JSON)
```

## 🤖 Agents

| Agent | Target | Tools |
|-------|--------|-------|
| **Social Scout** | Username, Nama | Username checker, Twitter, Google Dork |
| **Domain Intel** | Domain | WHOIS, DNS, Shodan, VirusTotal, Subdomain enum |
| **Email Hunter** | Email | Validator, HaveIBeenPwned, Hunter.io |
| **IP Recon** | IP Address | IPInfo, AbuseIPDB, Port scan, GeoIP |
| **Report Writer** | Semua | Markdown/JSON formatter |

## 🚀 Quick Start

### 1. Clone repository
```bash
git clone https://github.com/YOUR_USERNAME/osint-crewai.git
cd osint-crewai
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup environment
```bash
cp .env.example .env
# Edit .env dengan API keys kamu
nano .env
```

### 4. Jalankan
```bash
# Mode interaktif
python main.py

# Dengan argumen
python main.py --target johndoe --type username
python main.py --target john@example.com --type email --output both
python main.py --target example.com --type domain --verbose
python main.py --target 8.8.8.8 --type ip --output json
```

## 📋 API Keys

| Service | Kegunaan | Free Tier | Link |
|---------|----------|-----------|------|
| OpenAI | LLM (wajib) | — | [platform.openai.com](https://platform.openai.com) |
| Shodan | Port/services scan | 100 req | [account.shodan.io](https://account.shodan.io) |
| Hunter.io | Email discovery | 25 req/bulan | [hunter.io](https://hunter.io) |
| HaveIBeenPwned | Breach check | Berbayar $3.95/bln | [haveibeenpwned.com](https://haveibeenpwned.com) |
| VirusTotal | Reputasi domain | 500 req/hari | [virustotal.com](https://www.virustotal.com) |
| IPInfo | Geolokasi IP | 50k req/bulan | [ipinfo.io](https://ipinfo.io) |
| AbuseIPDB | IP abuse check | 1000 req/hari | [abuseipdb.com](https://www.abuseipdb.com) |

> Tools akan **otomatis disabled** jika API key tidak dikonfigurasi, dan memberikan link manual sebagai fallback.

## 🌐 Deploy di CrewAI Platform

1. Push ke GitHub
2. Login ke [app.crewai.com](https://app.crewai.com)
3. Connect GitHub repository
4. Set environment variables di dashboard
5. Deploy!

## 📁 Struktur Project

```
osint-crewai/
├── main.py                    # Entry point
├── requirements.txt
├── .env.example               # Template env vars
├── config/crew.yaml           # CrewAI deploy config
├── src/
│   ├── crew.py                # Orchestrator utama
│   ├── agents/
│   │   ├── social_scout.py
│   │   ├── domain_intel.py
│   │   ├── email_hunter.py
│   │   ├── ip_recon.py
│   │   └── report_writer.py
│   ├── tasks/
│   │   └── osint_tasks.py
│   ├── tools/
│   │   ├── social_tools.py
│   │   ├── domain_tools.py
│   │   ├── email_tools.py
│   │   ├── ip_tools.py
│   │   └── report_tools.py
│   └── utils/
│       ├── target_detector.py
│       └── report_saver.py
├── tests/
│   └── test_basic.py
└── outputs/                   # Hasil laporan tersimpan di sini
```

## ⚠️ Disclaimer

Tool ini dibuat **hanya untuk tujuan investigasi yang sah**, keamanan defensif, dan penelitian.
- Selalu dapatkan izin sebelum menginvestigasi
- Patuhi Terms of Service setiap platform
- Jangan gunakan untuk aktivitas ilegal atau melanggar privasi

## 📝 License

MIT License — lihat [LICENSE](LICENSE)
