"""
Tools untuk Social Media OSINT
"""

import os
import re
import json
import requests
from typing import Type, Optional
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


# --- Input Schemas ---

class UsernameInput(BaseModel):
    username: str = Field(..., description="Username yang akan dicari di berbagai platform")


class TwitterInput(BaseModel):
    query: str = Field(..., description="Query pencarian Twitter/X")


class DorkInput(BaseModel):
    target: str = Field(..., description="Target untuk Google Dork search")
    dork_type: str = Field(
        default="general",
        description="Tipe dork: general, social, document, email"
    )


# --- Tools ---

class UsernameCheckTool(BaseTool):
    name: str = "username_checker"
    description: str = (
        "Cek keberadaan username di berbagai platform media sosial. "
        "Gunakan untuk menemukan akun-akun yang terkait dengan target."
    )
    args_schema: Type[BaseModel] = UsernameInput

    def _run(self, username: str) -> str:
        """Check username di berbagai platform menggunakan requests"""
        platforms = {
            "Twitter/X": f"https://twitter.com/{username}",
            "GitHub": f"https://github.com/{username}",
            "Instagram": f"https://www.instagram.com/{username}/",
            "Reddit": f"https://www.reddit.com/user/{username}",
            "TikTok": f"https://www.tiktok.com/@{username}",
            "YouTube": f"https://www.youtube.com/@{username}",
            "LinkedIn": f"https://www.linkedin.com/in/{username}",
            "Pinterest": f"https://www.pinterest.com/{username}/",
            "Medium": f"https://medium.com/@{username}",
            "Dev.to": f"https://dev.to/{username}",
            "Keybase": f"https://keybase.io/{username}",
            "HackerNews": f"https://news.ycombinator.com/user?id={username}",
            "ProductHunt": f"https://www.producthunt.com/@{username}",
            "Telegram": f"https://t.me/{username}",
        }

        results = {"found": [], "not_found": [], "errors": []}
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; OSINT-Research/1.0)"
        }

        for platform, url in platforms.items():
            try:
                response = requests.get(
                    url, headers=headers, timeout=5, allow_redirects=True
                )
                if response.status_code == 200:
                    results["found"].append({"platform": platform, "url": url})
                elif response.status_code == 404:
                    results["not_found"].append(platform)
                else:
                    results["errors"].append(
                        f"{platform}: HTTP {response.status_code}"
                    )
            except requests.exceptions.RequestException as e:
                results["errors"].append(f"{platform}: {str(e)[:50]}")

        summary = (
            f"Username '{username}' ditemukan di {len(results['found'])} platform:\n"
        )
        for item in results["found"]:
            summary += f"  ✓ {item['platform']}: {item['url']}\n"
        summary += f"\nTidak ditemukan di: {', '.join(results['not_found'])}\n"

        return summary


class TwitterSearchTool(BaseTool):
    name: str = "twitter_search"
    description: str = (
        "Cari informasi dari Twitter/X menggunakan API atau scraping publik. "
        "Temukan tweet, profil, dan koneksi terkait target."
    )
    args_schema: Type[BaseModel] = TwitterInput

    def _run(self, query: str) -> str:
        """Search Twitter — gunakan API jika tersedia, fallback ke info dasar"""
        api_key = os.getenv("TWITTER_BEARER_TOKEN")

        if api_key:
            headers = {"Authorization": f"Bearer {api_key}"}
            params = {
                "query": query,
                "max_results": 10,
                "tweet.fields": "created_at,public_metrics,author_id",
            }
            try:
                r = requests.get(
                    "https://api.twitter.com/2/tweets/search/recent",
                    headers=headers,
                    params=params,
                    timeout=10,
                )
                if r.status_code == 200:
                    data = r.json()
                    tweets = data.get("data", [])
                    result = f"Ditemukan {len(tweets)} tweet untuk query '{query}':\n"
                    for t in tweets[:5]:
                        result += f"  - {t.get('text', '')[:100]}...\n"
                    return result
            except Exception as e:
                return f"Twitter API error: {e}. Gunakan pencarian manual di twitter.com/search?q={query}"

        # Fallback tanpa API
        return (
            f"Twitter Bearer Token tidak dikonfigurasi.\n"
            f"Cari manual: https://twitter.com/search?q={query}\n"
            f"Atau gunakan: https://nitter.net/search?q={query}"
        )


class GoogleDorkTool(BaseTool):
    name: str = "google_dork"
    description: str = (
        "Buat Google Dork queries untuk menemukan informasi target di internet. "
        "Menghasilkan query-query yang bisa digunakan untuk pencarian manual maupun otomatis."
    )
    args_schema: Type[BaseModel] = DorkInput

    def _run(self, target: str, dork_type: str = "general") -> str:
        """Generate Google Dork queries untuk target"""
        dorks = {
            "general": [
                f'"{target}"',
                f'"{target}" site:linkedin.com',
                f'"{target}" site:github.com',
                f'"{target}" email OR contact',
                f'"{target}" filetype:pdf OR filetype:doc',
            ],
            "social": [
                f'"{target}" site:twitter.com OR site:x.com',
                f'"{target}" site:instagram.com',
                f'"{target}" site:facebook.com',
                f'"{target}" site:reddit.com',
            ],
            "document": [
                f'"{target}" filetype:pdf',
                f'"{target}" filetype:xlsx OR filetype:csv',
                f'"{target}" inurl:cv OR inurl:resume',
                f'"{target}" site:slideshare.net',
            ],
            "email": [
                f'"{target}" "@gmail.com" OR "@yahoo.com"',
                f'"{target}" email contact',
                f'"mailto:{target}"',
            ],
        }

        selected_dorks = dorks.get(dork_type, dorks["general"])
        result = f"Google Dork queries untuk '{target}' (tipe: {dork_type}):\n\n"
        for i, dork in enumerate(selected_dorks, 1):
            result += f"{i}. {dork}\n"
            result += f"   URL: https://www.google.com/search?q={dork.replace(' ', '+')}\n\n"

        return result
