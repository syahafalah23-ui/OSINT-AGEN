"""Report Writer Agent"""
from crewai import Agent
from src.tools.report_tools import MarkdownReportTool, JsonExportTool


def create_report_writer() -> Agent:
    return Agent(
        role="OSINT Intelligence Report Writer",
        goal=(
            "Kompilasi semua temuan dari agent lain menjadi laporan intelijen "
            "yang terstruktur, komprehensif, dan mudah dibaca. Sertakan ringkasan "
            "eksekutif, temuan kunci, timeline, dan rekomendasi."
        ),
        backstory=(
            "Kamu adalah analis intelijen senior dengan kemampuan menulis laporan "
            "yang jernih dan actionable. Kamu tahu cara menyajikan data kompleks "
            "menjadi narasi yang mudah dipahami, dengan struktur yang profesional "
            "seperti laporan intelijen sesungguhnya."
        ),
        tools=[
            MarkdownReportTool(),
            JsonExportTool(),
        ],
        verbose=True,
        allow_delegation=False,
        max_iter=3,
    )
