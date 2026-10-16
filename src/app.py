
import sys
import inspect
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(__file__).resolve().parent
sys.path.insert(0, str(SRC))
sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / ".env")

from agents.supervisor import SupervisorAgent
from state import AgentState

st.set_page_config(
    page_title="Self-Evolving Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background: #080d18;
    color: #e5e7eb;
    font-family: Inter, sans-serif;
}
.main .block-container {
    padding-top: 1rem !important;
    padding-bottom: 2rem;
    max-width: 1450px;
}
header[data-testid="stHeader"] {
    height: 0;
    background: transparent;
}
[data-testid="stSidebar"] {
    background: #0d1423;
    border-right: 1px solid #202b40;
}
h1, h2, h3 {
    color: #f8fafc !important;
}
p, label {
    color: #cbd5e1;
}
.hero, .profile-card {
    box-sizing: border-box;
    height: 148px;
    min-height: 148px;
    border: 1px solid #263850;
    border-radius: 15px;
    background: linear-gradient(120deg, #14213d, #111827 65%, #102c39);
}
.hero {
    padding: 23px 22px;
    overflow: hidden;
}
.eyebrow {
    color: #67e8f9;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.6px;
    margin-bottom: 10px;
}
.hero-title {
    color: #f8fafc;
    font-size: 25px;
    line-height: 1.25;
    font-weight: 800;
    margin-bottom: 10px;
}
.hero-sub {
    color: #a9b8cc;
    font-size: 12px;
    line-height: 1.5;
}
.profile-card {
    padding: 12px 8px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    overflow: hidden;
}
.profile-avatar {
    width: 34px;
    height: 34px;
    line-height: 34px;
    border-radius: 50%;
    background: #164e63;
    color: #67e8f9;
    font-size: 13px;
    font-weight: 800;
    margin-bottom: 7px;
}
.profile-label {
    color: #94a3b8;
    font-size: 8px;
    letter-spacing: 1px;
    margin-bottom: 5px;
}
.profile-name {
    color: #f8fafc;
    font-size: 12px;
    font-weight: 700;
    line-height: 1.35;
    overflow-wrap: anywhere;
}
.profile-status {
    color: #67e8f9;
    font-size: 10px;
    margin-top: 6px;
}
.metric {
    background: #111a2b;
    border: 1px solid #24334b;
    border-radius: 12px;
    padding: 17px;
    min-height: 90px;
}
.metric-label {
    color: #93a4bb;
    font-size: 10px;
}
.metric-value {
    color: #f8fafc;
    font-size: 23px;
    font-weight: 800;
    margin-top: 9px;
}
.stTextArea textarea {
    background: #0b1220 !important;
    color: #f8fafc !important;
    border: 1px solid #33445e !important;
    border-radius: 9px !important;
}
.stButton > button {
    border-radius: 8px;
    font-weight: 600;
    min-height: 40px;
}
div[data-testid="stExpander"] {
    background: #101827;
    border: 1px solid #24334b;
    border-radius: 10px;
}
hr {
    border-color: #24334b;
}
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "Overview"
if "runs" not in st.session_state:
    st.session_state.runs = 0
if "result" not in st.session_state:
    st.session_state.result = None
if "last_task" not in st.session_state:
    st.session_state.last_task = ""

with st.sidebar:
    st.markdown("## 🧠 Agent Studio")
    st.caption("SELF-EVOLVING AI PLATFORM")
    st.divider()

    page = st.radio(
        "NAVIGATION",
        ["Overview", "Run Agent", "Thought Paths", "Reflexion & Memory"],
        index=[
            "Overview", "Run Agent", "Thought Paths", "Reflexion & Memory"
        ].index(st.session_state.page),
    )
    st.session_state.page = page

    st.divider()
    st.markdown("### ⚙️ Agent Settings")
    num_paths = st.slider("Thought paths", 2, 5, 3)
    max_iterations = st.slider("Max iterations", 1, 5, 3)

    st.divider()
    st.caption("Tree of Thoughts")
    st.caption("Candidate Evaluation")
    st.caption("Reflexion & Episodic Memory")

# ONE header and ONE profile card only
left, right = st.columns([4.5, 1], gap="small")

with left:
    st.markdown("""
    <div class="hero">
        <div class="eyebrow">INTELLIGENT AGENT WORKSPACE</div>
        <div class="hero-title">Self-Evolving Agent</div>
        <div class="hero-sub">
            Explore solutions, evaluate possible paths, and improve results
            through reflection.
        </div>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="profile-card">
        <div class="profile-avatar">SP</div>
        <div class="profile-label">PROJECT OWNER</div>
        <div class="profile-name">Shubham Prajapati</div>
        <div class="profile-status">● AI Engineer</div>
    </div>
    """, unsafe_allow_html=True)

if page == "Overview":
    st.subheader("Dashboard Overview")

    a, b, c = st.columns(3)
    for col, label, value in [
        (a, "TOTAL RUNS", st.session_state.runs),
        (b, "THOUGHT PATHS", num_paths),
        (c, "MAX ITERATIONS", max_iterations),
    ]:
        with col:
            st.markdown(
                f'<div class="metric"><div class="metric-label">{label}'
                f'</div><div class="metric-value">{value}</div></div>',
                unsafe_allow_html=True,
            )

    st.subheader("Start a new task")
    st.caption("Give your agent a problem to solve and evaluate.")

    task = st.text_area(
        "Task",
        key="overview_task",
        height=115,
        label_visibility="collapsed",
        placeholder=(
            "Example: Build a spam email classifier. Compare Naive Bayes, "
            "Logistic Regression, and Random Forest. Evaluate accuracy, "
            "precision, recall, and F1-score, then recommend the best model."
        ),
    )

    if st.button("🚀 Run Agent", type="primary", use_container_width=True):
        if task.strip():
            st.session_state.run_task = task.strip()
            st.session_state.page = "Run Agent"
            st.rerun()
        else:
            st.warning("Please enter a task first.")

elif page == "Run Agent":
    st.subheader("🚀 Run Agent")

    task = st.text_area(
        "Enter your task",
        value=st.session_state.get("run_task", ""),
        height=130,
        placeholder="Example: Compare ML models for fraud detection and recommend a reliable solution.",
        key="run_task_input",
    )

    if st.button("Run Agent", type="primary", use_container_width=True):
        if not task.strip():
            st.warning("Please enter a task first.")
        else:
            try:
                with st.spinner("Agent is working..."):
                    fields = {
                        "query": task.strip(),
                        "task": task.strip(),
                        "input": task.strip(),
                        "thought_paths": [],
                        "scores": [],
                        "mistakes": [],
                        "num_paths": num_paths,
                        "max_iterations": max_iterations,
                    }

                    state = {
                        "query": task.strip(),
                        "thought_paths": [],
                        "scores": [],
                        "mistakes": [],
                        "num_paths": num_paths,
                        "max_iterations": max_iterations,
                    }

                    result = SupervisorAgent().run(state)

                    st.session_state.result = result
                    st.session_state.last_task = task.strip()
                    st.session_state.runs += 1
                    st.success("Agent run completed!")
            except Exception as e:
                st.error(f"Agent error: {e}")

result = st.session_state.result

if result is not None:
    if page == "Thought Paths":
        st.subheader("🌳 Thought Paths")
    elif page == "Reflexion & Memory":
        st.subheader("🔁 Reflexion & Memory")
    else:
        st.subheader("📌 Latest Result")

    st.caption(f"Task: {st.session_state.last_task}")

    if isinstance(result, dict):
        answer = (
            result.get("final_answer")
            or result.get("answer")
            or result.get("response")
            or result.get("output")
        )
        if answer:
            st.markdown("### Final Answer")
            st.write(answer)

        if page in ["Overview", "Run Agent", "Thought Paths"]:
            with st.expander("🌳 Thought Paths"):
                st.write(result.get("thought_paths", result.get("thoughts", [])))
            with st.expander("📊 Candidate Scores"):
                st.write(result.get("scores", result.get("evaluations", [])))

        if page in ["Overview", "Run Agent", "Reflexion & Memory"]:
            with st.expander("🔁 Reflexion & Mistakes"):
                st.write(result.get("mistakes", result.get("reflexion", [])))
            with st.expander("🧠 Episodic Memory"):
                st.write(result.get("memory", result.get("episodic_memory", [])))

        with st.expander("Full Agent Output"):
            st.json(result, expanded=False)
    else:
        st.write(result)

elif page in ["Thought Paths", "Reflexion & Memory"]:
    st.info("Run a task first to see these results.")
