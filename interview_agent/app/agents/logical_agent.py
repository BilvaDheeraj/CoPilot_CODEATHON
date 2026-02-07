from app.agents.base_agent import BaseAgent
from app.schemas.interview import InterviewSession

class LogicalAgent(BaseAgent):
    async def generate_question(self, session: InterviewSession) -> str:
        prompt = "Generate a logical reasoning question (e.g., puzzles, sequence completion, or deductive reasoning)."
        context = f"Candidate Name: {session.candidate_name}. Difficulty: Medium."
        return await self.llm.generate_response(prompt, context)

    async def evaluate_answer(self, question: str, answer: str) -> dict:
        prompt = """
        Evaluate the logical reasoning.
        Return a JSON object with the following structure:
        {
            "correctness": <0-5 score>,
            "logic_quality": <0-5 score>,
            "feedback": "<concise feedback string>"
        }
        """
        content = f"Question: {question}\nAnswer: {answer}"
        response = await self.llm.generate_response(prompt, content)
        import json
        try:
            cleaned = response.replace("```json", "").replace("```", "").strip()
            return json.loads(cleaned)
        except:
             return {"feedback": response, "correctness": 0, "logic_quality": 0}
