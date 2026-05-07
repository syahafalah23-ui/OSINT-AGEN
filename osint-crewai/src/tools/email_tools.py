"""Email OSINT Tools"""
import os, re, requests
from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class EmailInput(BaseModel):
    email: str = Field(..., description="Email address yang akan diinvestigasi")


class EmailValidateTool(BaseTool):
    name: str = "email_validate"
    description: str = "Validasi dan analisis email address"
    args_schema: Type[BaseModel] = EmailInput

    def _run(self, email: str) -> str:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        is_valid = bool(re.match(pattern, email))
        domain = email.split('@')[1] if '@' in email else ''
        result = f"Email Analysis: {email}\n"
        result += f"  Format valid : {is_valid}\n"
        result += f"  Domain       : {domain}\n"
        # Cek MX record
        if domain:
            try:
                import dns.resolver
                mx = dns.resolver.resolve(domain, 'MX')
                result += f"  MX Records   : {[str(r.exchange) for r in mx]}\n"
            except:
                result += f"  MX Records   : Error atau tidak ada\n"
        return result


class HaveIBeenPwnedTool(BaseTool):
    name: str = "haveibeenpwned"
    description: str = "Cek apakah email ada di data breach database"
    args_schema: Type[BaseModel] = EmailInput

    def _run(self, email: str) -> str:
        api_key = os.getenv("HIBP_API_KEY")
        if not api_key:
            return (
                f"HIBP_API_KEY tidak dikonfigurasi.\n"
                f"Cek manual: https://haveibeenpwned.com/account/{email}\n"
                f"API key: https://haveibeenpwned.com/API/Key"
            )
        headers = {
            "hibp-api-key": api_key,
            "User-Agent": "OSINT-Research-Tool"
        }
        try:
            r = requests.get(
                f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}",
                headers=headers, timeout=10
            )
            if r.status_code == 200:
                breaches = r.json()
                result = f"HIBP — Email {email} ditemukan di {len(breaches)} breach:\n"
                for b in breaches[:10]:
                    result += f"  • {b['Name']} ({b['BreachDate']}) — {b['DataClasses']}\n"
                return result
            elif r.status_code == 404:
                return f"HIBP — Email {email} TIDAK ditemukan dalam breach database. ✓"
            return f"HIBP error: HTTP {r.status_code}"
        except Exception as e:
            return f"HIBP error: {e}"


class HunterIOTool(BaseTool):
    name: str = "hunter_io"
    description: str = "Gunakan Hunter.io untuk mencari email terkait sebuah domain atau orang"
    args_schema: Type[BaseModel] = EmailInput

    def _run(self, email: str) -> str:
        api_key = os.getenv("HUNTER_API_KEY")
        domain = email.split('@')[1] if '@' in email else email
        if not api_key:
            return (
                f"HUNTER_API_KEY tidak dikonfigurasi.\n"
                f"Cek manual: https://hunter.io/email-finder\n"
                f"API key gratis: https://hunter.io/users/sign_up"
            )
        try:
            r = requests.get(
                f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={api_key}",
                timeout=10
            )
            if r.status_code == 200:
                data = r.json().get('data', {})
                emails = data.get('emails', [])
                result = f"Hunter.io untuk domain {domain}:\n"
                result += f"  Total email ditemukan: {len(emails)}\n"
                for e in emails[:10]:
                    result += f"  • {e.get('value')} ({e.get('type')}) — confidence: {e.get('confidence')}%\n"
                return result
            return f"Hunter.io error: HTTP {r.status_code}"
        except Exception as e:
            return f"Hunter.io error: {e}"
