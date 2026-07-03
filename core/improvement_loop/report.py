from dataclasses import asdict
from pathlib import Path
import json

class ImprovementReportWriter:
    def __init__(self,root):
        self.root=Path(root)/"improvement"
        self.root.mkdir(parents=True,exist_ok=True)
    def write(self,report):
        (self.root/"improvement.json").write_text(json.dumps(asdict(report),default=str,indent=2),encoding="utf-8")
        (self.root/"improvement.md").write_text(f"# Improvement Report\n\n{report.summary}\n",encoding="utf-8")
