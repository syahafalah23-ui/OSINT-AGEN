"""
Tools untuk Domain & Infrastructure OSINT
"""

import os
import json
import socket
import requests
import dns.resolver
from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class DomainInput(BaseModel):
    domain: str = Field(..., description="Domain yang akan diinvestigasi")


class WhoisTool(BaseTool):
    name: str = "whois_lookup"
    description: str = "Lakukan WHOIS lookup untuk mendapatkan informasi registrasi domain"
    args_schema: Type[BaseModel] = DomainInput

    def _run(self, domain: str) -> str:
        try:
            import whois
            w = whois.whois(domain)
            result = f"WHOIS Data untuk {domain}:\n"
            result += f"  Registrar    : {w.registrar}\n"
            result += f"  Created      : {w.creation_date}\n"
            result += f"  Expires      : {w.expiration_date}\n"
            result += f"  Updated      : {w.updated_date}\n"
            result += f"  Name Servers : {w.name_servers}\n"
            result += f"  Status       : {w.status}\n"
            result += f"  Emails       : {w.emails}\n"
            result += f"  Country      : {w.country}\n"
            return result
        except ImportError:
            return self._whois_api_fallback(domain)
        except Exception as e:
            return f"WHOIS error untuk {domain}: {e}\n" + self._whois_api_fallback(domain)

    def _whois_api_fallback(self, domain: str) -> str:
        """Fallback menggunakan whois API publik"""
        try:
            r = requests.get(
                f"https://rdap.org/domain/{domain}", timeout=10
            )
            if r.status_code == 200:
                data = r.json()
                return f"RDAP Data untuk {domain}:\n{json.dumps(data, indent=2)[:1000]}"
        except Exception as e:
            pass
        return f"Gunakan manual: https://who.is/whois/{domain}"


class DnsLookupTool(BaseTool):
    name: str = "dns_lookup"
    description: str = "Lookup semua DNS records untuk sebuah domain"
    args_schema: Type[BaseModel] = DomainInput

    def _run(self, domain: str) -> str:
        record_types = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"]
        results = [f"DNS Records untuk {domain}:"]

        for rtype in record_types:
            try:
                answers = dns.resolver.resolve(domain, rtype)
                results.append(f"\n{rtype} Records:")
                for rdata in answers:
                    results.append(f"  {rdata}")
            except dns.resolver.NoAnswer:
                results.append(f"\n{rtype}: (tidak ada record)")
            except dns.resolver.NXDOMAIN:
                return f"Domain {domain} tidak ditemukan (NXDOMAIN)"
            except Exception as e:
                results.append(f"\n{rtype}: Error - {e}")

        return "\n".join(results)


class ShodanTool(BaseTool):
    name: str = "shodan_search"
    description: str = "Search Shodan untuk informasi port, services, dan teknologi"
    args_schema: Type[BaseModel] = DomainInput

    def _run(self, domain: str) -> str:
        api_key = os.getenv("SHODAN_API_KEY")
        if not api_key:
            return (
                f"SHODAN_API_KEY tidak dikonfigurasi.\n"
                f"Cari manual: https://www.shodan.io/search?query={domain}\n"
                f"Daftar gratis di: https://account.shodan.io/register"
            )
        try:
            # Resolve IP dulu
            ip = socket.gethostbyname(domain)
            r = requests.get(
                f"https://api.shodan.io/shodan/host/{ip}?key={api_key}",
                timeout=10,
            )
            if r.status_code == 200:
                data = r.json()
                result = f"Shodan data untuk {domain} ({ip}):\n"
                result += f"  OS          : {data.get('os', 'Unknown')}\n"
                result += f"  Country     : {data.get('country_name', 'Unknown')}\n"
                result += f"  ISP         : {data.get('isp', 'Unknown')}\n"
                result += f"  Last update : {data.get('last_update', 'Unknown')}\n"
                result += f"  Open ports  : {data.get('ports', [])}\n"
                vulns = data.get('vulns', [])
                if vulns:
                    result += f"  Vulnerabilities: {list(vulns)[:5]}\n"
                return result
            else:
                return f"Shodan error: HTTP {r.status_code}"
        except Exception as e:
            return f"Shodan error: {e}"


class VirusTotalTool(BaseTool):
    name: str = "virustotal_check"
    description: str = "Cek reputasi domain di VirusTotal"
    args_schema: Type[BaseModel] = DomainInput

    def _run(self, domain: str) -> str:
        api_key = os.getenv("VIRUSTOTAL_API_KEY")
        if not api_key:
            return (
                f"VIRUSTOTAL_API_KEY tidak dikonfigurasi.\n"
                f"Cek manual: https://www.virustotal.com/gui/domain/{domain}\n"
                f"Daftar gratis di: https://www.virustotal.com/gui/join-us"
            )
        try:
            headers = {"x-apikey": api_key}
            r = requests.get(
                f"https://www.virustotal.com/api/v3/domains/{domain}",
                headers=headers,
                timeout=10,
            )
            if r.status_code == 200:
                data = r.json().get("data", {}).get("attributes", {})
                stats = data.get("last_analysis_stats", {})
                result = f"VirusTotal untuk {domain}:\n"
                result += f"  Malicious   : {stats.get('malicious', 0)}\n"
                result += f"  Suspicious  : {stats.get('suspicious', 0)}\n"
                result += f"  Harmless    : {stats.get('harmless', 0)}\n"
                result += f"  Reputation  : {data.get('reputation', 0)}\n"
                result += f"  Categories  : {data.get('categories', {})}\n"
                return result
            return f"VirusTotal: HTTP {r.status_code}"
        except Exception as e:
            return f"VirusTotal error: {e}"


class SubdomainEnumTool(BaseTool):
    name: str = "subdomain_enum"
    description: str = "Enumerasi subdomain dari sebuah domain"
    args_schema: Type[BaseModel] = DomainInput

    def _run(self, domain: str) -> str:
        """Subdomain enumeration menggunakan crt.sh (certificate transparency)"""
        found = []
        try:
            r = requests.get(
                f"https://crt.sh/?q=%.{domain}&output=json",
                timeout=15,
            )
            if r.status_code == 200:
                data = r.json()
                subdomains = set()
                for entry in data:
                    name = entry.get("name_value", "")
                    for sub in name.split("\n"):
                        sub = sub.strip().lower()
                        if sub.endswith(domain) and sub != domain:
                            subdomains.add(sub)

                found = sorted(list(subdomains))[:30]  # Limit 30
                result = f"Subdomain dari {domain} (via crt.sh):\n"
                result += f"Total ditemukan: {len(found)}\n\n"
                for sub in found:
                    result += f"  • {sub}\n"
                return result
        except Exception as e:
            pass

        return f"Subdomain enum error. Coba manual: https://crt.sh/?q=%.{domain}"
