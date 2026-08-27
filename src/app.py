import streamlit as st
import os
import sys
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.supervisor import SupervisorAgent
from state import AgentState

st.set_page_config(page_title="🧠 Self-Evolving Agent", layout="wide")

st.title("🧠 Self-Evolving Agent")
st.markdown("*Tree of Thoughts + Reflexion + Episodic Memory*")

with st.sidebar:
    st.header("⚙️ Configuration")
    num_paths = st.slider("Number of Thought Paths", 2, 6, 4)
    max_iter = st.slider("Max Reflexion Iterations", 1, 5, 3)
    st.markdown("---")
    st.markdown("### 🧠 How it Works")
    st.markdown("🌳 Tree of Thoughts — Generates multiple reasoning paths")
    st.markdown("📊 Evaluation — Scores each path")
    st.markdown("✅ Selection — Chooses the best path")
    st.markdown("🔄 Reflexion — Learns from mistakes")
    st.markdown("🧠 Memory — Remembers past failures")
    st.markdown("---")
    st.caption("Built with LangGraph + Groq + Streamlit")

query = st.text_area("🔍 Ask a complex reasoning question", height=100)

if st.button("🚀 Run Self-Evolving Agent", type="primary"):
    if query:
        state = AgentState(
            query=query,
            thought_paths=[],
            num_paths=num_paths,
            best_path=None,
            scores=[],
            past_mistakes=[],
            reflexion_feedback="",
            improvement="",
            final_answer="",
            iteration=0,
            max_iterations=max_iter
        )
        
        with st.spinner("🧠 Agents are thinking..."):
            supervisor = SupervisorAgent()
            result = supervisor.run(state)
        
        st.success("✅ Reasoning Complete!")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🏆 Final Answer")
            st.markdown(f"**{result['final_answer']}**")
        with col2:
            st.subheader("📊 Best Path Score")
            if result.get("best_path") and result.get("scores"):
                st.metric("Score", f"{result['scores'][0]}/100")
        
        with st.expander("🌳 All Thought Paths"):
            for path in result.get("thought_paths", []):
                st.write(f"**Path {path['path_id']}:** {path['reasoning'][:100]}...")
                st.caption(f"Answer: {path['answer']}")
        
        with st.expander("🔄 Reflexion Feedback"):
            st.write(result.get("reflexion_feedback", "No reflexion yet"))
        
        with st.expander("🧠 Episodic Memory"):
            mistakes = supervisor.memory.get_past_mistakes()
            for m in mistakes:
                st.write(f"- {m['query']}: {m['feedback']}")
            lessons = supervisor.memory.get_lessons()
            for l in lessons:
                st.write(f"- {l['lesson']}")
    else:
        st.warning("Please enter a question")