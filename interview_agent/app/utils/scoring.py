from app.schemas.interview import InterviewSession, InterviewRound, Evaluation
from typing import Dict

def calculate_final_score(session: InterviewSession) -> Dict[str, float]:
    scores_by_round = {
        InterviewRound.BEHAVIOURAL: [],
        InterviewRound.LOGICAL: [],
        InterviewRound.APTITUDE: []
    }
    
    # Collect scores
    for question in session.questions_asked:
        if question.id in session.scores:
            eval_obj = session.scores[question.id]
            if question.round in scores_by_round:
                scores_by_round[question.round].append(eval_obj.score)

    # Averages
    averages = {}
    for r, values in scores_by_round.items():
        if values:
            averages[r.value] = sum(values) / len(values)
        else:
            averages[r.value] = 0.0
            
    # Weights
    # Behavioural 40%, Logical 30%, Aptitude 20%
    # Communication 10% (We will simulate this as average of all scores for now, or random heuristic)
    # Since we don't have a dedicated comms score, let's assume it matches Behavioural.
    
    # Normalizing weights to sum to 1.0 (assuming comms is part of others or separate)
    # User said: B=40, L=30, A=20, C=10.
    
    w_b = 0.4
    w_l = 0.3
    w_a = 0.2
    w_c = 0.1
    
    avg_b = averages.get("behavioural", 0)
    avg_l = averages.get("logical", 0)
    avg_a = averages.get("aptitude", 0)
    
    # Heuristic for communication: mostly based on behavioural clarity
    avg_c = avg_b 
    
    final_score = (avg_b * w_b) + (avg_l * w_l) + (avg_a * w_a) + (avg_c * w_c)
    
    return {
        "behavioural": avg_b,
        "logical": avg_l,
        "aptitude": avg_a,
        "communication": avg_c,
        "overall": final_score
    }
