class DelegationAgent:
    def delegate(self, tasks):
        print("[DelegationAgent] Assigning tasks...")
        assignments = {}
        for idx, (name, desc) in enumerate(tasks.items()):
            agent_name = f"WorkerAgent_{idx+1}"
            assignments[agent_name] = desc
            print(f"{agent_name} ← {desc}")
        return assignments
