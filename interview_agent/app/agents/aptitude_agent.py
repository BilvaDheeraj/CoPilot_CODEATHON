from app.agents.base_agent import BaseAgent
from app.schemas.interview import InterviewSession

class AptitudeAgent(BaseAgent):
    async def generate_question(self, session: InterviewSession) -> str:
        prompt = "Generate a quantitative aptitude question (e.g., time & work, percentages, probability)."
        context = f"Candidate Name: {session.candidate_name}. Difficulty: Medium."
        return await self.llm.generate_response(prompt, context)

    async def evaluate_answer(self, question: str, answer: str) -> dict:
        prompt = """
        Evaluate the aptitude answer.
        Return a JSON object with the following structure:
        {
            "accuracy": <0-5 score>,
            "methodology": <0-5 score>,
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
             return {"feedback": response, "accuracy": 0, "methodology": 0}
