"""
FastAPI application exposing SQLBot functionality over HTTP.

The API defines two endpoints:

* **POST /chat** – Accepts a JSON payload with ``user`` and ``message``
  keys.  Returns a JSON object containing the bot’s reply.  The
  conversation is stored in the database as with the CLI.
* **GET /conversations** – Returns recent conversation history.  You can
  pass an optional ``limit`` query parameter to restrict the number of
  messages returned (default: 20).

Start the server with::

    uvicorn api:app --reload

"""

from datetime import timezone
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator

from models import SessionLocal, Message
from llm_client import call_llm
from db_setup import create_tables


app = FastAPI(title="SQLBot API", version="0.1.0")


class ChatRequest(BaseModel):
    user: str
    message: str

    @validator("user")
    def user_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("user must not be empty")
        return v

    @validator("message")
    def message_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("message must not be empty")
        return v


class ChatResponse(BaseModel):
    response: str


class ConversationEntry(BaseModel):
    id: int
    user: str
    message: str
    response: str
    timestamp: str


@app.on_event("startup")
def startup_event() -> None:
    """Ensure the database tables exist when the application starts."""
    create_tables()


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest) -> ChatResponse:
    """Handle incoming chat messages and return the bot’s reply."""
    session = SessionLocal()
    try:
        reply = call_llm(req.message)
        msg = Message(user=req.user, message=req.message, response=reply)
        session.add(msg)
        session.commit()
        return ChatResponse(response=reply)
    finally:
        session.close()


@app.get("/conversations", response_model=List[ConversationEntry])
def conversations_endpoint(limit: int = 20) -> List[ConversationEntry]:
    """Return recent conversation entries, most recent last."""
    if limit <= 0:
        raise HTTPException(status_code=400, detail="limit must be positive")
    session = SessionLocal()
    try:
        rows = (
            session.query(Message)
            .order_by(Message.timestamp.desc())
            .limit(limit)
            .all()
        )
        out: List[ConversationEntry] = []
        for m in reversed(rows):
            ts = m.timestamp.replace(tzinfo=timezone.utc).isoformat()
            out.append(
                ConversationEntry(
                    id=m.id,
                    user=m.user,
                    message=m.message,
                    response=m.response,
                    timestamp=ts,
                )
            )
        return out
    finally:
        session.close()