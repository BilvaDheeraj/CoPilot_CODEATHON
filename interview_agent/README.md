# Advanced Interview AI Agent

## Overview
This is a comprehensive AI Agent designed to conduct multi-round interviews, covering Behavioural, Logical, and Aptitude domains. It features a FastAPI backend and a Next.js frontend, with Redis-backed session management.

## Features
- **Multi-Round Interviews**: Automatically transitions between Behavioural, Logical, and Aptitude rounds.
- **STAR Method Evaluation**: Evaluates behavioural answers using the STAR framework.
- **Real-Time Scoring**: Scores answers on the fly.
- **Report Generation**: Exports detailed PDF reports with scores and transcripts.
- **Redis Memory**: Persists interview sessions (optional, falls back to in-memory).

## Tech Stack
- **Backend**: Python, FastAPI, LangChain
- **Frontend**: Next.js, React, TailwindCSS
- **AI**: OpenAI GPT-4o
- **Database**: Redis (for session storage)

## Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- Redis (optional)
- OpenAI API Key

### Backend
1. Navigate to `interview_agent`
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   python -m uvicorn app.main:app --reload
   ```

### Frontend
1. Navigate to `interview_agent/frontend`
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the dev server:
   ```bash
   npm run dev
   ```

## Environment Variables
Create a `.env` file in `interview_agent`:
```
OPENAI_API_KEY=sk-...
REDIS_URL=redis://localhost:6379
```
