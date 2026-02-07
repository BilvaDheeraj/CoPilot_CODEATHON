from app.agents.base_agent import BaseAgent
from app.utils.llm_client import LLMClient
from app.utils.offline_engine import OfflineEngine
import json

class AptitudeAgent(BaseAgent):
    def __init__(self, llm_client: LLMClient):
        super().__init__(llm_client)
        self.current_correct_answer = None # Store the answer to the last generated question

    async def generate_question(self, session) -> str:
        # Use Offline Engine for guaranteed unique math problems
        text, answer = OfflineEngine.generate_aptitude_question()
        self.current_correct_answer = answer
        return text

    async def evaluate_answer(self, question: str, answer: str) -> dict:
        # If we have the stored correct answer, use exact match
        if self.current_correct_answer:
            return OfflineEngine.evaluate_exact_match(answer, self.current_correct_answer)
        
        # Fallback (shouldn't really happen with this flow)
        return OfflineEngine.evaluate_exact_match(answer, "0")
