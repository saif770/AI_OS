class ImprovementAnalyzer:
    PRIORITY={"Critical":0,"High":1,"Medium":2,"Low":3}
    def analyze(self, reflection_report):
        return list(getattr(reflection_report,"recommendations",[]))
