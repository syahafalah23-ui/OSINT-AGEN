"""Email Hunter Agent"""
from crewai import Agent
from src.tools.email_tools import EmailValidateTool, HaveIBeenPwnedTool, HunterIOTool


def create_email_hunter() -> Agent:
    return Agent(
        role="Email Intelligence Hunter",
        goal=(
            "Validasi email target, cek apakah pernah terlibat dalam data breach, "
            "temukan akun terkait, dan kumpulkan metadata email yang tersedia secara publik."
        ),
        backstory=(
            "Kamu adalah spesialis intelijen email yang memahami seluk-beluk "
            "infrastruktur email, breach databases, dan cara melacak identitas "
            "digital melalui alamat email."
        ),
        tools=[
            EmailValidateTool(),
            HaveIBeenPwnedTool(),
            HunterIOTool(),
        ],
        verbose=True,
        allow_delegation=False,
        max_iter=4,
    )
