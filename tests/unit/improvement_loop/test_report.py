import json
from core.improvement_loop.models import ImprovementPlan, ImprovementReport
from core.improvement_loop.report import ImprovementReportWriter

def test_report_writer(tmp_path):
    report=ImprovementReport("done",ImprovementPlan(),"Low")
    writer=ImprovementReportWriter(tmp_path)
    writer.write(report)
    jf=tmp_path/"improvement"/"improvement.json"
    assert jf.exists()
    data=json.loads(jf.read_text())
    assert data["summary"]=="done"
