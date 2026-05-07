"""
Social Scout Agent — mencari jejak digital di media sosial
"""

from crewai import Agent
from src.tools.social_tools import (
    UsernameCheckTool,
    TwitterSearchTool,
    GoogleDorkTool,
)


def create_social_scout() -> Agent:
    return Agent(
        role="Social Media Intelligence Scout",
        goal=(
            "Temukan semua akun media sosial, profil publik, dan jejak digital "
            "dari target yang diberikan. Kumpulkan informasi seperti bio, foto profil, "
            "followers, following, dan konten publik."
        ),
        backstory=(
            "Kamu adalah analis intelijen digital berpengalaman yang ahli dalam "
            "mencari jejak seseorang di internet. Kamu tahu cara menggunakan "
            "berbagai platform dan teknik OSINT untuk menemukan informasi yang relevan. "
            "Kamu selalu bekerja dalam batas hukum dan etika."
        ),
        tools=[
            UsernameCheckTool(),
            TwitterSearchTool(),
            GoogleDorkTool(),
        ],
        verbose=True,
        allow_delegation=False,
        max_iter=5,
    )
