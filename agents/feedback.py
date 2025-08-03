class FeedbackAgent:
    def review(self, results):
        print("[FeedbackAgent] Reviewing results...")
        for r in results:
            print(f"{r['agent']} → {r['task']} ✅")
