import os
import re
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

class Evaluator:
    def __init__(self, model="openai/gpt-oss-20b"):  
        self.llm = ChatGroq(
            model=model,
            temperature=0.2,
            api_key=os.getenv("GROQ_API_KEY")
        )

    def evaluate_path(self, query, path):
        prompt = f"""
        Evaluate this reasoning path for the query.

        Query: {query}
        Reasoning: {path['reasoning']}
        Steps: {path['steps']}
        Answer: {path['answer']}

        Score this path on:
        1. Relevance (0-10): How relevant is the reasoning to the query?
        2. Coherence (0-10): Is the reasoning logical and coherent?
        3. Completeness (0-10): Does it fully answer the query?
        4. Accuracy (0-10): Is the answer likely correct?

        Return a score out of 100 and a brief justification.
        Format: "Score: XX/100, Justification: ..."
        """

        messages = [HumanMessage(content=prompt)]
        response = self.llm.invoke(messages)
        
        try:
            score_match = re.search(r'Score:\s*(\d+)/100', response.content)
            if score_match:
                score = int(score_match.group(1))
            else:
                score = 70
        except:
            score = 70
        
        return {
            "score": score,
            "feedback": response.content
        }