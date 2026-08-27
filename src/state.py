from typing import TypedDict, List, Dict, Any, Optional

class ThoughtPath(TypedDict):
    path_id: int
    reasoning: str
    score: float
    answer: str
    steps: List[str]

class AgentState(TypedDict):
    query: str
    thought_paths: List[ThoughtPath]
    num_paths: int
    best_path: Optional[ThoughtPath]
    scores: List[float]
    past_mistakes: List[str]
    reflexion_feedback: str
    improvement: str
    final_answer: str
    iteration: int
    max_iterations: int