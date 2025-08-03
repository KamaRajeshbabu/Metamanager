import streamlit as st
import pandas as pd
import plotly.express as px
from agents.planner import PlanningAgent
from agents.delegator import DelegationAgent
from agents.worker import WorkerAgent
from agents.feedback import FeedbackAgent
from memory.vector_store import VectorStore

# --- Page Config ---
st.set_page_config(page_title="MetaManager", page_icon="🧠", layout="wide")

# --- Stylish Typing Title & Subtitle ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@600&display=swap" rel="stylesheet">

<style>
html, body, [class*="css"] {
    background-color: #0E1117 !important;
    color: #FAFAFA !important;
}

@keyframes typing {
  from { width: 0 }
  to { width: 100% }
}
@keyframes blink {
  50% { border-color: transparent }
}
@keyframes fadeIn {
  from { opacity: 0 }
  to { opacity: 1 }
}

.typing-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 40px;
    flex-direction: column;
}

.title-typing {
    font-family: 'Inter', sans-serif;
    font-size: 3.2rem;
    font-weight: 600;
    white-space: nowrap;
    overflow: hidden;
    border-right: 3px solid #7DD3FC;
    animation: typing 3s steps(20, end), blink 0.8s step-end infinite;
    background: linear-gradient(90deg, #7DD3FC, #34D399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}

.subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 1.2rem;
    color: #9ca3af;
    animation: fadeIn 2s ease-in-out;
}
</style>

<div class="typing-wrapper">
    <div class="title-typing">MetaManager</div>
    <div class="subtitle">AI-Powered Agent Workspace</div>
</div>
""", unsafe_allow_html=True)

# --- Intro ---
st.markdown("### Replace traditional managers with autonomous agents.")
st.markdown("*Built with Python 🐍, LangChain 🔗, and persistent memory 🧠.*")

# --- Task Input ---
st.subheader("🎯 Choose Agent & Input Task")
agent_choice = st.selectbox("Select Agent", ["PlanningAgent", "DelegationAgent", "WorkerAgent", "FeedbackAgent"])
task_input = st.text_input("What should the agent do?", value="Launch AI newsletter")

# --- Init Memory & Logs ---
memory = VectorStore()
task_logs = []

# --- Main Execution ---
if st.button("🚀 Run Agent Task"):
    result = ""
    tasks = []
    assignments = {}

    if agent_choice == "PlanningAgent":
        agent = PlanningAgent()
        tasks = agent.plan(task_input)
        task_logs = [{"Agent": "Planner", "Task": t, "Status": "Planned"} for t in tasks]
        result = f"Planned Tasks: {tasks}"

    elif agent_choice == "DelegationAgent":
        planner = PlanningAgent()
        tasks = planner.plan(task_input)
        delegator = DelegationAgent()
        assignments = delegator.delegate(tasks)
        task_logs = [{"Agent": k, "Task": v, "Status": "Assigned"} for k, v in assignments.items()]
        result = f"Assigned: {assignments}"

    elif agent_choice == "WorkerAgent":
        planner = PlanningAgent()
        tasks = planner.plan(task_input)
        delegator = DelegationAgent()
        assignments = delegator.delegate(tasks)
        for name, task in assignments.items():
            worker = WorkerAgent(name)
            output = worker.work(task)
            memory.store(output)
            task_logs.append({"Agent": name, "Task": task, "Status": "Completed"})
        result = f"Memory Log: {memory.get_all()}"

    elif agent_choice == "FeedbackAgent":
        planner = PlanningAgent()
        tasks = planner.plan(task_input)
        delegator = DelegationAgent()
        assignments = delegator.delegate(tasks)
        for name, task in assignments.items():
            worker = WorkerAgent(name)
            output = worker.work(task)
            memory.store(output)
            task_logs.append({"Agent": name, "Task": task, "Status": "Completed"})
        feedback = FeedbackAgent()
        feedback.review(memory.get_all())
        result = "Feedback complete."

    st.success("✅ Task Completed")

    with st.expander("📦 Raw Output"):
        st.code(result, language="json")

    if task_logs:
        df = pd.DataFrame(task_logs)

        st.subheader("🧾 Task Breakdown Table")
        st.dataframe(df, use_container_width=True)

        # --- Dashboard Grid Layout ---
        col1, col2 = st.columns(2)

        with col1:
            status_count = df["Status"].value_counts().reset_index()
            status_count.columns = ["Status", "Count"]
            pie_fig = px.pie(
                status_count,
                names="Status",
                values="Count",
                color_discrete_sequence=px.colors.sequential.RdBu,
                title="Task Status Distribution"
            )
            st.plotly_chart(pie_fig, use_container_width=True)

        with col2:
            st.markdown("#### 📋 Summary")
            total_tasks = len(df)
            completed = df[df['Status'] == 'Completed'].shape[0]
            planned = df[df['Status'] == 'Planned'].shape[0]
            assigned = df[df['Status'] == 'Assigned'].shape[0]
            completion_rate = round((completed / total_tasks) * 100, 2) if total_tasks else 0

            st.metric("Total Tasks", total_tasks)
            st.metric("Completed", completed)
            st.metric("Completion Rate", f"{completion_rate}%")
            st.metric("Planned", planned)
            st.metric("Assigned", assigned)

        # --- Export Logs ---
        st.subheader("📤 Export Data")
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download Task Logs (CSV)", csv_data, "task_logs.csv", "text/csv")

# --- Memory Viewer ---
st.subheader("🧠 Memory Logs")
logs = memory.get_all()
if logs:
    for idx, entry in enumerate(logs, 1):
        st.markdown(f"**Log {idx}**")
        st.code(entry)

    all_log_text = "\n\n".join(logs)
    st.download_button("⬇️ Download Memory Logs (TXT)", all_log_text, "memory_logs.txt")
else:
    st.info("No memory logs yet. Run the agent to generate logs.")

# --- Footer ---
st.markdown("---")
st.markdown("<center style='color: #ccc;'>Built with ❤️ by Kama Rajeshbabu</center>", unsafe_allow_html=True)
