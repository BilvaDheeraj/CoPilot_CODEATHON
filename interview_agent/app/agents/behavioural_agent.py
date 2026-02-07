from app.agents.base_agent import BaseAgent
from app.schemas.interview import InterviewSession

class BehaviouralAgent(BaseAgent):
    async def generate_question(self, session: InterviewSession) -> str:
        # Check history to see what star components are missing or what new question to ask
        prompt = "You are a behavioural interview expert. Generate a question using the STAR method."
        context = f"Candidate Name: {session.candidate_name}. Previous questions: {len(session.questions_asked)}"
        return await self.llm.generate_response(prompt, context)

    async def evaluate_answer(self, question: str, answer: str) -> dict:
        prompt = """
        Evaluate the following answer using the STAR method. 
        Return a JSON object with the following structure:
        {
            "situation": <0-5 score>,
            "task": <0-5 score>,
            "action": <0-5 score>,
            "result": <0-5 score>,
            "feedback": "<concise feedback string>"
        }
        """
        content = f"Question: {question}\nAnswer: {answer}"
        response = await self.llm.generate_response(prompt, content)
        # Rudimentary JSON cleanup (in production use a robust parser)
        import json
        try:
            # removing code blocks if present
            cleaned = response.replace("```json", "").replace("```", "").strip()
            return json.loads(cleaned)
        except:
             return {"feedback": response, "situation": 0, "task": 0, "action": 0, "result": 0}
