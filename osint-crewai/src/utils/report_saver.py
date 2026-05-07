"""Utility untuk menyimpan laporan OSINT"""
import os
import json
from datetime import datetime


def save_report(content: str, target: str, output_format: str = "markdown") -> str:
    """Simpan laporan ke folder outputs/"""
    os.makedirs("outputs", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Sanitize target name untuk filename
    safe_target = "".join(c if c.isalnum() or c in "._-" else "_" for c in target)
    safe_target = safe_target[:50]  # Limit panjang

    paths_saved = []

    if output_format in ("markdown", "both"):
        filename = f"outputs/osint_{safe_target}_{timestamp}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(str(content))
        paths_saved.append(filename)

    if output_format in ("json", "both"):
        filename = f"outputs/osint_{safe_target}_{timestamp}.json"
        data = {
            "target": target,
            "generated_at": datetime.now().isoformat(),
            "content": str(content)
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        paths_saved.append(filename)

    return ", ".join(paths_saved)
