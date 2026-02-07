from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum

class InterviewRound(str, Enum):
    BEHAVIOURAL = "behavioural"
    LOGICAL = "logical"
    APTITUDE = "aptitude"
    FINISHED = "finished"

class Question(BaseModel):
    id: str
    text: str
    round: InterviewRound
    difficulty: Optional[int] = 1

class Answer(BaseModel):
    question_id: str
    text: str
    timestamp: float

class Evaluation(BaseModel):
    score: float
    feedback: str
    criteria_breakdown: Dict[str, float]

class InterviewSession(BaseModel):
    session_id: str
    candidate_name: Optional[str] = None
    current_round: InterviewRound = InterviewRound.BEHAVIOURAL
    questions_asked: List[Question] = []
    answers: List[Answer] = []
    scores: Dict[str, Evaluation] = {}
    is_completed: bool = False
