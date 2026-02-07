from fpdf import FPDF
from app.schemas.interview import InterviewSession

class ReportGenerator:
    def generate_pdf(self, session: InterviewSession) -> str:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        pdf.cell(200, 10, txt=f"Interview Report for {session.candidate_name}", ln=1, align="C")
        pdf.ln(10)
        
        pdf.cell(200, 10, txt=f"Session ID: {session.session_id}", ln=1)
        pdf.ln(5)

        # Scorecard
        from app.utils.scoring import calculate_final_score
        scorecard = calculate_final_score(session)
        
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt="Final Scorecard", ln=1)
        pdf.set_font("Arial", '', 12)
        
        pdf.cell(100, 10, txt=f"Overall Score: {scorecard['overall']:.2f} / 5.0", ln=1)
        pdf.ln(5)
        
        pdf.cell(100, 10, txt=f"Behavioural (40%): {scorecard['behavioural']:.2f}", ln=1)
        pdf.cell(100, 10, txt=f"Logical (30%): {scorecard['logical']:.2f}", ln=1)
        pdf.cell(100, 10, txt=f"Aptitude (20%): {scorecard['aptitude']:.2f}", ln=1)
        pdf.cell(100, 10, txt=f"Communication (10%): {scorecard['communication']:.2f}", ln=1)
        
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt="Detailed Transcript", ln=1)
        pdf.ln(5)

        for i, question in enumerate(session.questions_asked):
            pdf.set_font("Arial", 'B', 12)
            pdf.multi_cell(0, 10, txt=f"Q{i+1}: {question.text} ({question.round})")
            
            # Find answer
            answer_text = "N/A"
            if i < len(session.answers):
                answer_text = session.answers[i].text
            
            pdf.set_font("Arial", '', 11)
            pdf.multi_cell(0, 10, txt=f"A: {answer_text}")
            
            # Show score for this question
            if question.id in session.scores:
                eval_obj = session.scores[question.id]
                pdf.set_font("Arial", 'I', 10)
                pdf.cell(0, 10, txt=f"Score: {eval_obj.score:.1f}/5 - {eval_obj.feedback}", ln=1)
            
            pdf.ln(5)

        filename = f"report_{session.session_id}.pdf"

        output_path = f"app/report/{filename}"
        pdf.output(output_path)
        return output_path
