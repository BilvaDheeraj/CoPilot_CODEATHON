from typing import Dict, Optional
import uuid
import os
import json
import redis
from app.schemas.interview import InterviewSession

class MemoryStore:
    def __init__(self):
        self._sessions: Dict[str, InterviewSession] = {}
        self.redis_url = os.getenv("REDIS_URL")
        self.redis_client = None
        if self.redis_url:
            try:
                self.redis_client = redis.from_url(self.redis_url)
                print(f"Connected to Redis at {self.redis_url}")
            except Exception as e:
                print(f"Failed to connect to Redis: {e}. Falling back to in-memory.")

    def create_session(self, candidate_name: str) -> InterviewSession:
        session_id = str(uuid.uuid4())
        session = InterviewSession(session_id=session_id, candidate_name=candidate_name)
        self._save_session(session)
        return session

    def get_session(self, session_id: str) -> Optional[InterviewSession]:
        if self.redis_client:
            data = self.redis_client.get(session_id)
            if data:
                return InterviewSession.model_validate_json(data)
            return None
        return self._sessions.get(session_id)

    def update_session(self, session: InterviewSession):
        self._save_session(session)

    def _save_session(self, session: InterviewSession):
        if self.redis_client:
            self.redis_client.set(session.session_id, session.model_dump_json())
        else:
            self._sessions[session.session_id] = session
