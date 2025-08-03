from agents.planner import PlanningAgent
from agents.delegator import DelegationAgent
from agents.worker import WorkerAgent
from agents.feedback import FeedbackAgent
from memory.vector_store import VectorStore
import config

def main():
    print("🚀 Launching MetaManager.ai")

    # Initialize agents
    planner = PlanningAgent()
    delegator = DelegationAgent()
    feedback = FeedbackAgent()
    memory = VectorStore() if config.USE_MEMORY else None

    # Step 1: Planning
    tasks = planner.plan("Launch AI newsletter")

    # Step 2: Delegation
    assignments = delegator.delegate(tasks)

    # Step 3: Execution
    results = []
    for name, task in assignments.items():
        worker = WorkerAgent(name)
        result = worker.work(task)
        results.append(result)
        if memory:
            memory.store(result)

    # Step 4: Feedback
    feedback.review(results)

    if memory:
        print("\n🧠 Memory Summary:")
        for m in memory.get_all():
            print(m)

if __name__ == "__main__":
    main()
