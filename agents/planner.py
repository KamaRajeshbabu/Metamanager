class PlanningAgent:
    def plan(self, goal):
        print(f"[PlanningAgent] Goal received: {goal}")
        return {
            "Design": "Create visuals and branding",
            "Campaign": "Schedule email & social posts",
            "Analytics": "Set up user tracking"
        }
