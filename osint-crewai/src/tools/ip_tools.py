"""IP & Network OSINT Tools"""
import os, socket, requests
from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class IPInput(BaseModel):
    ip: str = Field(..., description="IP address yang akan diinvestigasi")


class IPInfoTool(BaseTool):
    name: str = "ipinfo"
    description: str = "Dapatkan informasi geolokasi, ISP, dan ASN dari IP address"
    args_schema: Type[BaseModel] = IPInput

    def _run(self, ip: str) -> str:
        token = os.getenv("IPINFO_TOKEN", "")
        url = f"https://ipinfo.io/{ip}/json"
        if token:
            url += f"?token={token}"
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                d = r.json()
                result = f"IPInfo untuk {ip}:\n"
                result += f"  Hostname  : {d.get('hostname', 'N/A')}\n"
                result += f"  City      : {d.get('city', 'N/A')}\n"
                result += f"  Region    : {d.get('region', 'N/A')}\n"
                result += f"  Country   : {d.get('country', 'N/A')}\n"
                result += f"  Location  : {d.get('loc', 'N/A')}\n"
                result += f"  ISP/Org   : {d.get('org', 'N/A')}\n"
                result += f"  Timezone  : {d.get('timezone', 'N/A')}\n"
                return result
            return f"IPInfo: HTTP {r.status_code}"
        except Exception as e:
            return f"IPInfo error: {e}"


class AbuseIPDBTool(BaseTool):
    name: str = "abuseipdb"
    description: str = "Cek riwayat abuse dan laporan untuk sebuah IP address"
    args_schema: Type[BaseModel] = IPInput

    def _run(self, ip: str) -> str:
        api_key = os.getenv("ABUSEIPDB_API_KEY")
        if not api_key:
            return (
                f"ABUSEIPDB_API_KEY tidak dikonfigurasi.\n"
                f"Cek manual: https://www.abuseipdb.com/check/{ip}\n"
                f"API key gratis: https://www.abuseipdb.com/register"
            )
        headers = {"Key": api_key, "Accept": "application/json"}
        try:
            r = requests.get(
                "https://api.abuseipdb.com/api/v2/check",
                headers=headers,
                params={"ipAddress": ip, "maxAgeInDays": 90, "verbose": True},
                timeout=10,
            )
            if r.status_code == 200:
                d = r.json().get("data", {})
                result = f"AbuseIPDB untuk {ip}:\n"
                result += f"  Abuse Score : {d.get('abuseConfidenceScore', 0)}%\n"
                result += f"  Total laporan: {d.get('totalReports', 0)}\n"
                result += f"  Last report : {d.get('lastReportedAt', 'N/A')}\n"
                result += f"  Country     : {d.get('countryCode', 'N/A')}\n"
                result += f"  ISP         : {d.get('isp', 'N/A')}\n"
                result += f"  Domain      : {d.get('domain', 'N/A')}\n"
                result += f"  Is tor      : {d.get('isTor', False)}\n"
                return result
            return f"AbuseIPDB: HTTP {r.status_code}"
        except Exception as e:
            return f"AbuseIPDB error: {e}"


class PortScanTool(BaseTool):
    name: str = "port_scan"
    description: str = "Lakukan passive port scan untuk menemukan services yang berjalan"
    args_schema: Type[BaseModel] = IPInput

    def _run(self, ip: str) -> str:
        """Passive port check — hanya common ports"""
        common_ports = {
            21: "FTP", 22: "SSH", 23: "Telnet",
            25: "SMTP", 53: "DNS", 80: "HTTP",
            110: "POP3", 143: "IMAP", 443: "HTTPS",
            445: "SMB", 3306: "MySQL", 3389: "RDP",
            5432: "PostgreSQL", 6379: "Redis",
            8080: "HTTP-Alt", 8443: "HTTPS-Alt",
            27017: "MongoDB",
        }
        open_ports = []
        for port, service in common_ports.items():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((ip, port))
                sock.close()
                if result == 0:
                    open_ports.append((port, service))
            except:
                pass

        if open_ports:
            result = f"Open ports pada {ip}:\n"
            for port, service in open_ports:
                result += f"  ✓ {port}/{service}\n"
        else:
            result = f"Tidak ada port terbuka yang ditemukan pada {ip} (common ports)\n"
        return result


class GeoIPTool(BaseTool):
    name: str = "geoip"
    description: str = "Dapatkan koordinat GPS dan info lokasi dari IP address"
    args_schema: Type[BaseModel] = IPInput

    def _run(self, ip: str) -> str:
        try:
            r = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
            if r.status_code == 200:
                d = r.json()
                if d.get("status") == "success":
                    result = f"GeoIP untuk {ip}:\n"
                    result += f"  Country  : {d.get('country')} ({d.get('countryCode')})\n"
                    result += f"  Region   : {d.get('regionName')}\n"
                    result += f"  City     : {d.get('city')}\n"
                    result += f"  ZIP      : {d.get('zip')}\n"
                    result += f"  Lat/Lon  : {d.get('lat')}, {d.get('lon')}\n"
                    result += f"  Timezone : {d.get('timezone')}\n"
                    result += f"  ISP      : {d.get('isp')}\n"
                    result += f"  ASN      : {d.get('as')}\n"
                    result += f"  Maps     : https://maps.google.com/?q={d.get('lat')},{d.get('lon')}\n"
                    return result
            return f"GeoIP: status {r.status_code}"
        except Exception as e:
            return f"GeoIP error: {e}"
