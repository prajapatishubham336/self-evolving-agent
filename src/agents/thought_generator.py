import os
import json
import re
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

class ThoughtGenerator:
    def __init__(self, model="openai/gpt-oss-20b"): 
        self.llm = ChatGroq(
            model=model,
            temperature=0.7,
            api_key=os.getenv("GROQ_API_KEY")
        )

    def generate_paths(self, query, num_paths=4, past_lessons=""):
        system_prompt = f"""
        You are a reasoning expert. Generate {num_paths} different reasoning paths for the given query.

        Each path should have:
        - A unique approach/angle
        - Step-by-step reasoning
        - A final answer

        Past lessons to consider (avoid these mistakes):
        {past_lessons}

        Return the paths as a JSON list with fields:
        - "path_id": 1, 2, 3, 4
        - "reasoning": "step by step reasoning"
        - "steps": ["step1", "step2", "step3"]
        - "answer": "final answer from this path"
        """

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Query: {query}")
        ]
        
        response = self.llm.invoke(messages)
        
        try:
            json_match = re.search(r'\[.*\]', response.content, re.DOTALL)
            if json_match:
                paths = json.loads(json_match.group())
                return paths
        except:
            pass
        
        # Fallback
        return [
            {
                "path_id": 1,
                "reasoning": "Direct approach: analyze query directly",
                "steps": ["Step 1", "Step 2"],
                "answer": "Answer from path 1"
            },
            {
                "path_id": 2,
                "reasoning": "Alternative approach: break down into sub-problems",
                "steps": ["Step A", "Step B", "Step C"],
                "answer": "Answer from path 2"
            }
        ]