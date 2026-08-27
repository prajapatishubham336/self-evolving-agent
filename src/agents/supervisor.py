import os
from src.agents.thought_generator import ThoughtGenerator
from src.agents.evaluator import Evaluator
from src.agents.selector import Selector
from src.agents.reflexion import ReflexionAgent
from src.memory.episodic_memory import EpisodicMemory
from src.state import AgentState
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

class SupervisorAgent:
    def __init__(self):
        self.thought_generator = ThoughtGenerator()
        self.evaluator = Evaluator()
        self.selector = Selector()
        self.reflexion = ReflexionAgent()
        self.memory = EpisodicMemory()

    def run(self, state: AgentState):
        print("🧠 Supervisor: Starting Self-Evolving Agent...")
        
        query = state["query"]
        num_paths = state.get("num_paths", 4)
        max_iterations = state.get("max_iterations", 3)
        
        past_lessons = self.memory.get_lessons()
        lesson_text = "\n".join([l["lesson"] for l in past_lessons])
        past_mistakes = self.memory.get_past_mistakes()
        mistake_text = "\n".join([m["feedback"] for m in past_mistakes])
        
        final_answer = ""
        
        for iteration in range(max_iterations):
            print(f"🔄 Iteration {iteration+1}/{max_iterations}")
            
            paths = self.thought_generator.generate_paths(
                query, num_paths, lesson_text
            )
            state["thought_paths"] = paths
            
            scores = []
            for path in paths:
                result = self.evaluator.evaluate_path(query, path)
                scores.append(result["score"])
            state["scores"] = scores
            
            best_path = self.selector.select_best_path(paths, scores)
            state["best_path"] = best_path
            
            final_answer = best_path["answer"]
            state["final_answer"] = final_answer
            
            if iteration < max_iterations - 1:
                print("🔄 Reflexion: Learning from this attempt...")
                reflexion = self.reflexion.reflect(
                    query, best_path, mistake_text, final_answer
                )
                state["reflexion_feedback"] = reflexion
                
                if "Lesson:" in reflexion:
                    lesson = reflexion.split("Lesson:")[1].strip().split("\n")[0]
                    self.memory.add_lesson(lesson)
                    lesson_text += "\n" + lesson
        
        state["final_answer"] = final_answer
        state["iteration"] = max_iterations
        self.memory.add_success(query, final_answer)
        
        print("✅ Self-Evolving Agent complete!")
        return state

    def generate_final_report(self):
        # 🔥 Yeh function ab use nahi ho raha, but agar ho toh model change karo
        llm = ChatGroq(
            model="groq/compound-mini",  # 🔥 FIXED
            temperature=0.2,
            api_key=os.getenv("GROQ_API_KEY")
        )
        response = llm.invoke([HumanMessage(content="Generate report")])
        return response.content