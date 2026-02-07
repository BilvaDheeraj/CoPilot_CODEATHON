from app.utils.llm_client import LLMClient
from app.schemas.interview import InterviewSession

class BaseAgent:
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    async def generate_question(self, session: InterviewSession) -> str:
        raise NotImplementedError

    async def evaluate_answer(self, question: str, answer: str) -> dict:
        raise NotImplementedError
