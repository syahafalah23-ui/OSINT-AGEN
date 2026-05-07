"""IP Recon Agent"""
from crewai import Agent
from src.tools.ip_tools import IPInfoTool, AbuseIPDBTool, PortScanTool, GeoIPTool


def create_ip_recon() -> Agent:
    return Agent(
        role="IP & Network Reconnaissance Specialist",
        goal=(
            "Analisis IP address target: geolokasi, ISP, ASN, riwayat abuse, "
            "port yang terbuka, dan koneksi jaringan. Identifikasi apakah IP "
            "digunakan untuk aktivitas berbahaya."
        ),
        backstory=(
            "Kamu adalah pakar jaringan dan forensik IP. Kamu bisa membaca "
            "peta jaringan seperti membaca buku, mengidentifikasi infrastruktur "
            "hosting, VPN, proxy, dan aktivitas mencurigakan dari pola traffic."
        ),
        tools=[
            IPInfoTool(),
            AbuseIPDBTool(),
            PortScanTool(),
            GeoIPTool(),
        ],
        verbose=True,
        allow_delegation=False,
        max_iter=4,
    )
