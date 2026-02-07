from app.agents.base_agent import BaseAgent
from app.utils.llm_client import LLMClient
from app.utils.offline_engine import OfflineEngine

class BehaviouralAgent(BaseAgent):
    def __init__(self, llm_client: LLMClient):
        super().__init__(llm_client)

    async def generate_question(self, session) -> str:
        # Use Offline Engine for instant start (no LLM latency)
        return OfflineEngine.generate_behavioural_question()

    async def evaluate_answer(self, question: str, answer: str) -> dict:
        # Use deterministic keyword analysis
        return OfflineEngine.evaluate_behavioural(answer)
