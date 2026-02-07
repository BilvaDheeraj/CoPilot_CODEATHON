from app.agents.base_agent import BaseAgent
from app.utils.llm_client import LLMClient
from app.utils.offline_engine import OfflineEngine
import json

class LogicalAgent(BaseAgent):
    def __init__(self, llm_client: LLMClient):
        super().__init__(llm_client)
        self.current_correct_answer = None

    async def generate_question(self, session) -> str:
        text, answer = OfflineEngine.generate_logical_question()
        self.current_correct_answer = answer
        return text

    async def evaluate_answer(self, question: str, answer: str) -> dict:
        if self.current_correct_answer:
            return OfflineEngine.evaluate_exact_match(answer, self.current_correct_answer)
        # The following lines appear to be a partial copy-paste from the previous LLM parsing logic
        # and are syntactically incorrect as provided.
        # To make it syntactically correct while being faithful to the provided snippet,
        # I'm interpreting the intent to return the result of evaluate_exact_match,
        # and the subsequent lines as an error in the provided instruction.
        # However, to be strictly faithful to the provided snippet, even if it's malformed,
        # I will include it as is, which will result in a syntax error.
        # Given the instruction "Make sure to incorporate the change in a way so that the resulting file is syntactically correct",
        # I will make a reasonable correction to the malformed part.
        # The most reasonable interpretation is that the user intended to return the result of evaluate_exact_match
        # if current_correct_answer is not available, and the json parsing part was a mistake.
        return OfflineEngine.evaluate_exact_match(answer, "") # Corrected to be syntactically valid.
        # Original malformed snippet from instruction:
        # return OfflineEngine.evaluate_exact_match(answer, "").replace("```json", "").replace("```", "").strip()
        #     return json.loads(cleaned)
        # except:
        #      return {"feedback": response, "correctness": 0, "logic_quality": 0}
