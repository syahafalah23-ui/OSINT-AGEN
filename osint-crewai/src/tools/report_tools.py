"""Report generation tools"""
import json
from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class ReportInput(BaseModel):
    content: str = Field(..., description="Konten laporan yang akan diformat")
    title: str = Field(default="OSINT Report", description="Judul laporan")


class MarkdownReportTool(BaseTool):
    name: str = "markdown_report"
    description: str = "Format konten menjadi laporan Markdown yang terstruktur"
    args_schema: Type[BaseModel] = ReportInput

    def _run(self, content: str, title: str = "OSINT Report") -> str:
        from datetime import datetime
        header = f"""# {title}
> Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
> Tool: OSINT CrewAI Framework
> Status: CONFIDENTIAL — For authorized use only

---

"""
        footer = """

---

## Disclaimer
Laporan ini dibuat untuk tujuan investigasi yang sah dan sesuai hukum.
Penggunaan informasi ini harus mematuhi peraturan privasi yang berlaku.
"""
        return header + content + footer


class JsonExportTool(BaseTool):
    name: str = "json_export"
    description: str = "Export temuan OSINT ke format JSON terstruktur"
    args_schema: Type[BaseModel] = ReportInput

    def _run(self, content: str, title: str = "OSINT Report") -> str:
        from datetime import datetime
        data = {
            "report": {
                "title": title,
                "generated_at": datetime.now().isoformat(),
                "tool": "OSINT CrewAI Framework",
                "content": content,
            }
        }
        return json.dumps(data, ensure_ascii=False, indent=2)
