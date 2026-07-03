from .analyzer import ImprovementAnalyzer
from .planner import ImprovementPlanner
from .report import ImprovementReportWriter
from .models import ImprovementReport

class ImprovementEngine:
    def __init__(self,output_root):
        self.analyzer=ImprovementAnalyzer()
        self.planner=ImprovementPlanner()
        self.writer=ImprovementReportWriter(output_root)
    def run(self,reflection_report):
        candidates=self.analyzer.analyze(reflection_report)
        plan=self.planner.build(candidates)
        report=ImprovementReport(
            summary="Improvement analysis completed.",
            plan=plan,
            overall_priority=plan.highest_priority,
            recommendations=plan.items,
        )
        self.writer.write(report)
        return report
