"""
Task definitions untuk semua operasi OSINT
"""

from typing import List, Optional
from crewai import Agent, Task


class OsintTasks:
    def __init__(self, target: str, target_type: str):
        self.target = target
        self.target_type = target_type

    def social_media_task(self, agent: Agent) -> Task:
        return Task(
            description=f"""
            Lakukan investigasi media sosial untuk target: **{self.target}**
            Tipe target: {self.target_type}

            Langkah yang harus dilakukan:
            1. Cari username di platform utama: Twitter/X, Instagram, GitHub, LinkedIn, 
               Reddit, TikTok, Facebook, YouTube, Telegram
            2. Untuk setiap akun yang ditemukan, kumpulkan:
               - URL profil
               - Bio dan deskripsi
               - Jumlah followers/following
               - Tanggal pembuatan akun
               - Postingan/aktivitas terbaru (jika publik)
               - Foto profil URL
            3. Lakukan Google Dork search untuk menemukan referensi lain
            4. Catat semua temuan, termasuk yang negatif (tidak ditemukan)

            Format output: Structured JSON dengan semua temuan per platform
            """,
            expected_output="""
            JSON report berisi:
            - platforms_found: list platform dengan profil ditemukan
            - platforms_not_found: list platform tanpa profil
            - profiles: dict dengan detail setiap profil
            - additional_findings: temuan lain dari Google Dork
            - confidence_score: 0-100 seberapa yakin ini adalah orang yang sama
            """,
            agent=agent,
        )

    def domain_recon_task(self, agent: Agent) -> Task:
        return Task(
            description=f"""
            Lakukan reconnaissance domain untuk target: **{self.target}**

            Langkah investigasi:
            1. WHOIS lookup — pemilik domain, registrar, tanggal registrasi, expiry
            2. DNS records — A, AAAA, MX, NS, TXT, CNAME records
            3. Subdomain enumeration — temukan semua subdomain aktif
            4. Shodan search — port terbuka, teknologi, banner services
            5. VirusTotal check — riwayat malware, reputation score
            6. Teknologi web yang digunakan (jika web server)
            7. IP address terkait dan historical IPs
            8. SSL certificate info

            Format output: Structured report dengan semua temuan teknis
            """,
            expected_output="""
            Technical report berisi:
            - whois_data: informasi registrasi domain
            - dns_records: semua DNS records
            - subdomains: list subdomain yang ditemukan
            - shodan_data: port dan services
            - reputation: skor reputasi dan riwayat
            - associated_ips: IP addresses terkait
            - technologies: teknologi yang terdeteksi
            """,
            agent=agent,
        )

    def email_hunt_task(self, agent: Agent) -> Task:
        return Task(
            description=f"""
            Investigasi email untuk target: **{self.target}**

            Langkah investigasi:
            1. Validasi format dan keberadaan email
            2. HaveIBeenPwned — cek apakah email ada di data breach database
            3. Hunter.io — cari email lain yang terkait dengan domain yang sama
            4. Cari akun media sosial yang terdaftar dengan email ini
            5. Identifikasi provider email dan metadata
            6. Cek apakah email digunakan di forum atau database publik

            PENTING: Jangan lakukan spam atau unauthorized access.
            Gunakan hanya API dan database publik yang legal.
            """,
            expected_output="""
            Email intelligence report berisi:
            - email_valid: boolean apakah email valid
            - breaches: list data breach yang melibatkan email ini
            - associated_accounts: akun yang ditemukan
            - related_emails: email lain dari domain yang sama
            - risk_score: 0-100 skor risiko
            """,
            agent=agent,
        )

    def ip_recon_task(self, agent: Agent) -> Task:
        return Task(
            description=f"""
            Lakukan IP/Network reconnaissance untuk target: **{self.target}**

            Langkah investigasi:
            1. IPInfo — geolokasi, ISP, ASN, timezone
            2. AbuseIPDB — cek riwayat abuse dan laporan
            3. Port scanning (common ports: 80, 443, 22, 21, 8080, 8443)
            4. Reverse DNS lookup
            5. Cek apakah IP bagian dari VPN/Proxy/Tor exit node
            6. Historical data — domain yang pernah hosted di IP ini

            PENTING: Hanya lakukan passive reconnaissance. 
            Jangan lakukan port scan agresif atau exploit.
            """,
            expected_output="""
            Network intelligence report berisi:
            - geolocation: negara, kota, koordinat
            - isp_asn: ISP dan ASN info
            - abuse_reports: jumlah dan detail laporan abuse
            - open_ports: port yang terbuka
            - is_vpn_proxy: apakah VPN/Proxy/Tor
            - hosted_domains: domain yang pernah di-host
            - threat_level: low/medium/high/critical
            """,
            agent=agent,
        )

    def compile_report_task(
        self,
        agent: Agent,
        context_tasks: List[Task],
        output_format: str = "markdown",
    ) -> Task:
        return Task(
            description=f"""
            Kompilasi semua temuan OSINT dari agent lain menjadi laporan final.
            Target: **{self.target}** | Tipe: {self.target_type}
            Format output yang diinginkan: {output_format}

            Struktur laporan yang harus dibuat:

            # OSINT Intelligence Report
            ## 1. Ringkasan Eksekutif
            - Siapa target ini?
            - Temuan paling penting
            - Risk assessment keseluruhan

            ## 2. Identitas Digital
            - Akun media sosial yang ditemukan
            - Profil singkat berdasarkan data

            ## 3. Infrastruktur Teknis (jika relevan)
            - Domain, IP, hosting info

            ## 4. Data Breach & Security
            - Riwayat breach
            - Potensi risiko

            ## 5. Timeline Aktivitas
            - Kronologi penemuan

            ## 6. Temuan Detail per Kategori
            - Semua data raw dari setiap agent

            ## 7. Kesimpulan & Rekomendasi

            ## 8. Disclaimer
            - Laporan ini dibuat untuk tujuan legal/edukasi

            Gunakan format yang profesional, terstruktur, dan mudah dibaca.
            """,
            expected_output=f"""
            Laporan intelijen lengkap dalam format {output_format} yang mencakup
            semua temuan dari agent Social Scout, Domain Intel, Email Hunter, 
            dan IP Recon. Laporan harus profesional, terstruktur, dan actionable.
            """,
            agent=agent,
            context=context_tasks,
        )
