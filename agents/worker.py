class WorkerAgent:
    def __init__(self, name):
        self.name = name

    def work(self, task):
        print(f"[{self.name}] Doing task: {task}")
        return {
            "agent": self.name,
            "task": task,
            "result": f"Completed: {task}"
        }
