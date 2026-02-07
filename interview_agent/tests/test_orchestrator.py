import pytest
import uuid
from app.orchestrator import Orchestrator
from app.schemas.interview import InterviewRound

@pytest.mark.asyncio
async def test_start_session():
    orchestrator = Orchestrator()
    session = await orchestrator.start_new_session("Test Candidate")
    assert session.candidate_name == "Test Candidate"
    assert session.current_round == InterviewRound.BEHAVIOURAL
    assert session.session_id is not None

@pytest.mark.asyncio
async def test_get_next_action_initial():
    orchestrator = Orchestrator()
    session = await orchestrator.start_new_session("Test Candidate")
    
    response = await orchestrator.get_next_action(session.session_id)
    assert response["status"] == "in_progress"
    assert "question" in response
    assert len(session.questions_asked) == 1

@pytest.mark.asyncio
async def test_round_transition():
    orchestrator = Orchestrator()
    session = await orchestrator.start_new_session("Test Candidate")
    
    # Simulate 3 questions for Behavioural
    for _ in range(3):
        await orchestrator.get_next_action(session.session_id, last_answer="Simulated Answer")
    
    # Next call should transition to LOGICAL
    response = await orchestrator.get_next_action(session.session_id, last_answer="Final Behavioural Answer")
    
    # Check session state directly
    updated_session = orchestrator.memory.get_session(session.session_id)
    assert updated_session.current_round == InterviewRound.LOGICAL
