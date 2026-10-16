import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

class ReflexionAgent:
    def __init__(self, model="openai/gpt-oss-20b"): 
        self.llm = ChatGroq(
            model=model,
            temperature=0.3,
            api_key=os.getenv("GROQ_API_KEY")
        )

    def reflect(self, query, selected_path, past_mistakes, final_answer):
        prompt = f"""
        You are a self-improvement agent. Analyze the following:

        Query: {query}
        Selected Reasoning: {selected_path['reasoning']}
        Selected Answer: {selected_path['answer']}
        Final Answer: {final_answer}
        Past Mistakes: {past_mistakes}

        Provide:
        1. What went well?
        2. What could be improved?
        3. What mistake should be avoided next time?
        4. One lesson to store in memory.

        Output format:
        - Went well: ...
        - Improvement: ...
        - Avoid mistake: ...
        - Lesson: ...
        """

        messages = [HumanMessage(content=prompt)]
        response = self.llm.invoke(messages)
        return response.content