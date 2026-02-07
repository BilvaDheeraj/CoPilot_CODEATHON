import logging
import uuid
from app.schemas.interview import InterviewSession, InterviewRound, Question, Answer
from app.memory import MemoryStore
from app.utils.llm_client import LLMClient
from app.agents.behavioural_agent import BehaviouralAgent
from app.agents.logical_agent import LogicalAgent
from app.agents.aptitude_agent import AptitudeAgent

logger = logging.getLogger(__name__)

class Orchestrator:
    def __init__(self):
        self.memory = MemoryStore()
        self.llm_client = LLMClient()
        self.agents = {
            InterviewRound.BEHAVIOURAL: BehaviouralAgent(self.llm_client),
            InterviewRound.LOGICAL: LogicalAgent(self.llm_client),
            InterviewRound.APTITUDE: AptitudeAgent(self.llm_client)
        }

    async def start_new_session(self, candidate_name: str) -> InterviewSession:
        return self.memory.create_session(candidate_name)

    async def get_next_action(self, session_id: str, last_answer: str = None):
        session = self.memory.get_session(session_id)
        if not session:
            return {"error": "Session not found"}

        last_evaluation = None
        if last_answer:
            last_evaluation = await self.process_answer(session, last_answer)

        if session.is_completed:
            return {"status": "completed", "message": "Interview finished. Thank you!", "session": session, "feedback": last_evaluation}

        # Check if we need to switch rounds (Simple logic: 3 questions per round)
        # In a real app, this would be more dynamic
        current_round_questions = [q for q in session.questions_asked if q.round == session.current_round]
        if len(current_round_questions) >= 3:
            self._transition_round(session)
            if session.is_completed:
                return {"status": "completed", "message": "Interview finished. Thank you!", "session": session, "feedback": last_evaluation}

        # Generate next question with duplicate check
        max_retries = 3
        question = None
        
        existing_questions = {q.text.strip().lower() for q in session.questions_asked}
        
        for _ in range(max_retries):
            q_candidate = await self.generate_question(session)
            if q_candidate.text.strip().lower() not in existing_questions:
                question = q_candidate
                break
        
        if not question:
            # If all retries fail (unlikely), use the last generated one
            question = q_candidate

        # Store question in session
        session.questions_asked.append(question)
        self.memory.update_session(session)
        
        return {"status": "in_progress", "question": question, "round": session.current_round, "feedback": last_evaluation}

    def _transition_round(self, session: InterviewSession):
        if session.current_round == InterviewRound.BEHAVIOURAL:
            session.current_round = InterviewRound.LOGICAL
        elif session.current_round == InterviewRound.LOGICAL:
            session.current_round = InterviewRound.APTITUDE
        elif session.current_round == InterviewRound.APTITUDE:
            session.current_round = InterviewRound.FINISHED
            session.is_completed = True
        
        self.memory.update_session(session)

    async def process_answer(self, session: InterviewSession, answer_text: str):
        # Find the last question asked
        if not session.questions_asked:
            return # Should not happen

        last_question = session.questions_asked[-1]
        
        # Create answer object
        answer = Answer(
            question_id=last_question.id,
            text=answer_text,
            timestamp=0.0 # TODO: meaningful timestamp
        )
        session.answers.append(answer)

        # Evaluate answer
        agent = self.agents.get(session.current_round)
        evaluation = None
        if agent:
            raw_eval = await agent.evaluate_answer(last_question.text, answer_text)
            
            # Calculate score and map to Evaluation schema
            score = 0.0
            feedback = raw_eval.get("feedback", "No feedback provided.")
            breakdown = {k: v for k, v in raw_eval.items() if k != "feedback" and isinstance(v, (int, float))}
            
            if breakdown:
                score = sum(breakdown.values()) / len(breakdown)
            
            from app.schemas.interview import Evaluation
            evaluation = Evaluation(
                score=score,
                feedback=feedback,
                criteria_breakdown=breakdown
            )
            
            session.scores[last_question.id] = evaluation
        
        self.memory.update_session(session)
        return evaluation

    async def generate_question(self, session: InterviewSession) -> Question:
        agent = self.agents.get(session.current_round)
        if not agent:
             return Question(id=str(uuid.uuid4()), text="Error: No agent for this round.", round=session.current_round)
        
        question_text = await agent.generate_question(session)
        
        # If it's a mock response (dict), extract text, otherwise use string
        if isinstance(question_text, dict): 
            # This shouldn't happen with current base_agent but good for safety
            question_text = str(question_text)

        return Question(
            id=str(uuid.uuid4()),
            text=question_text,
            round=session.current_round
        )
