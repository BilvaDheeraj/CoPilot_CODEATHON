from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.orchestrator import Orchestrator

app = FastAPI(title="Advanced Interview AI Agent")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = Orchestrator()

class StartInterviewRequest(BaseModel):
    candidate_name: str

class AnswerRequest(BaseModel):
    session_id: str
    answer: str

@app.post("/start-interview")
async def start_interview(request: StartInterviewRequest):
    session = await orchestrator.start_new_session(request.candidate_name)
    # Get the first question immediately
    response = await orchestrator.get_next_action(session.session_id)
    return {"session_id": session.session_id, "initial_action": response}

@app.post("/answer")
async def submit_answer(request: AnswerRequest):
    response = await orchestrator.get_next_action(request.session_id, request.answer)
    return response

@app.get("/")
async def root():
    return {"message": "Interview Agent API is running"}

@app.get("/export-report/{session_id}")
async def export_report(session_id: str):
    session = orchestrator.memory.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    from app.report.exporter import ReportGenerator
    from fastapi.responses import FileResponse
    
    generator = ReportGenerator()
    pdf_path = generator.generate_pdf(session)
    
    return FileResponse(pdf_path, media_type='application/pdf', filename=f"report_{session_id}.pdf")
