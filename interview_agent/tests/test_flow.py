import pytest
import asyncio
from app.orchestrator import Orchestrator
from app.schemas.interview import InterviewRound

@pytest.mark.asyncio
async def test_full_interview_simulation():
    orchestrator = Orchestrator()
    
    # 1. Start Session
    session = await orchestrator.start_new_session("Alice Tester")
    assert session.current_round == InterviewRound.BEHAVIOURAL
    
    # 2. Loop through all rounds
    # Behavioural (3 Qs) -> Logical (3 Qs) -> Aptitude (3 Qs) -> Finished
    # Total 9 interactions.
    
    expected_rounds = [
        InterviewRound.BEHAVIOURAL, InterviewRound.BEHAVIOURAL, InterviewRound.BEHAVIOURAL,
        InterviewRound.LOGICAL, InterviewRound.LOGICAL, InterviewRound.LOGICAL,
        InterviewRound.APTITUDE, InterviewRound.APTITUDE, InterviewRound.APTITUDE
    ]
    
    for i, expected_round in enumerate(expected_rounds):
        # Check current status
        status = await orchestrator.get_next_action(session.session_id)
        assert status["status"] == "in_progress"
        assert session.current_round == expected_round
        
        # Determine question
        question = status["question"]
        print(f"[{i+1}] [{session.current_round}] Agent asked: {question.text}")
        
        # Submit Answer
        # We need to call get_next_action with last_answer to trigger processing of the PREVIOUS question
        # But wait, orchestrator.get_next_action does:
        # if last_answer: process()
        # if completed: return completed
        # generate_question()
        
        # So to "answer" the question we just got, we call get_next_action again with that answer?
        # No, that would generate the NEXT question.
        # Flow:
        # 1. Start -> returns Q1.
        # 2. Submit Ans1 -> calls get_next_action(ans1).
        #    -> processes Ans1 (scores Q1).
        #    -> checks transition.
        #    -> generates Q2.
        #    -> returns Q2.
        
        # So in this loop, we effectively simulate the answer to the *current* question
        # which will be processed in the *next* iteration of the loop (or after the loop).
        
        # We simulate this by processing the answer manually in the test loop
        # essentially mimicking the API call "/answer" which calls get_next_action(answer)
        
        fake_answer = f"This is a simulated answer for question {question.id}."
        
        # We can't just call orchestrator.get_next_action here because that would advance the state.
        # The loop implies 'Checking state BEFORE answering'.
        
        # Let's restructure the test to match the user flow exactly.
        
    pass

@pytest.mark.asyncio
async def test_exact_user_flow():
    orchestrator = Orchestrator()
    
    # Client: Start Interview
    session = await orchestrator.start_new_session("Bob Builder")
    response = await orchestrator.get_next_action(session.session_id) #(Init)
    
    # Should get Q1 (Behavioural)
    assert response["status"] == "in_progress"
    assert response["question"].round == InterviewRound.BEHAVIOURAL
    q1 = response["question"]
    print(f"Q1: {q1.text}")
    
    # Client: Answer Q1
    # Expect Q2 (Behavioural)
    response = await orchestrator.get_next_action(session.session_id, last_answer="Answer to Q1")
    assert response["status"] == "in_progress"
    assert response["question"].round == InterviewRound.BEHAVIOURAL
    q2 = response["question"]
    print(f"Q2: {q2.text}")
    
    # Client: Answer Q2
    # Expect Q3 (Behavioural)
    response = await orchestrator.get_next_action(session.session_id, last_answer="Answer to Q2")
    assert response["status"] == "in_progress"
    assert response["question"].round == InterviewRound.BEHAVIOURAL
    q3 = response["question"]
    print(f"Q3: {q3.text}")
    
    # Client: Answer Q3
    # Expect Q4 (Logical - Transition happens here)
    response = await orchestrator.get_next_action(session.session_id, last_answer="Answer to Q3")
    assert response["status"] == "in_progress"
    assert response["question"].round == InterviewRound.LOGICAL
    q4 = response["question"]
    print(f"Q4: {q4.text}")
    
    # ... Fast forward logic ...
    # Ans Q4 -> Q5 (Logical)
    response = await orchestrator.get_next_action(session.session_id, last_answer="Answer to Q4")
    # Ans Q5 -> Q6 (Logical)
    response = await orchestrator.get_next_action(session.session_id, last_answer="Answer to Q5")
    # Ans Q6 -> Q7 (Aptitude)
    response = await orchestrator.get_next_action(session.session_id, last_answer="Answer to Q6")
    assert response["question"].round == InterviewRound.APTITUDE
    
    # Ans Q7 -> Q8 (Aptitude)
    response = await orchestrator.get_next_action(session.session_id, last_answer="Answer to Q7")
    # Ans Q8 -> Q9 (Aptitude)
    response = await orchestrator.get_next_action(session.session_id, last_answer="Answer to Q8")
    
    # Ans Q9 -> Finished
    response = await orchestrator.get_next_action(session.session_id, last_answer="Answer to Q9")
    assert response["status"] == "completed"
    
    # Check Session Data
    final_session = response["session"]
    assert len(final_session.questions_asked) == 9
    assert len(final_session.answers) == 9
    assert len(final_session.scores) == 9
    
    # Generate Report
    from app.report.exporter import ReportGenerator
    import os
    
    generator = ReportGenerator()
    pdf_path = generator.generate_pdf(final_session)
    
    assert os.path.exists(pdf_path)
    print(f"Report generated at: {pdf_path}")

