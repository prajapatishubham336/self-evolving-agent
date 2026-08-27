import json
import os
from datetime import datetime

class EpisodicMemory:
    def __init__(self, memory_path="data/memory.json"):
        self.memory_path = memory_path
        os.makedirs(os.path.dirname(memory_path), exist_ok=True)
        self.memory = self._load_memory()

    def _load_memory(self):
        if os.path.exists(self.memory_path):
            with open(self.memory_path, 'r') as f:
                return json.load(f)
        return {"mistakes": [], "lessons": [], "successes": []}

    def _save_memory(self):
        with open(self.memory_path, 'w') as f:
            json.dump(self.memory, f, indent=2)

    def add_mistake(self, query, wrong_answer, correct_answer, feedback):
        self.memory["mistakes"].append({
            "query": query,
            "wrong_answer": wrong_answer,
            "correct_answer": correct_answer,
            "feedback": feedback,
            "timestamp": str(datetime.now())
        })
        self._save_memory()

    def add_lesson(self, lesson):
        self.memory["lessons"].append({
            "lesson": lesson,
            "timestamp": str(datetime.now())
        })
        self._save_memory()

    def add_success(self, query, answer):
        self.memory["successes"].append({
            "query": query,
            "answer": answer,
            "timestamp": str(datetime.now())
        })
        self._save_memory()

    def get_past_mistakes(self, limit=5):
        return self.memory["mistakes"][-limit:]

    def get_lessons(self, limit=5):
        return self.memory["lessons"][-limit:]