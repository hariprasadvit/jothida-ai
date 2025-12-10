"""
AI Chat Router - Tamil Astrology Chatbot
Uses RAG with Tamil LLM
"""

from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import Optional, List
import json

router = APIRouter()

class ChatMessage(BaseModel):
    role: str  # user or assistant
    content: str
    timestamp: Optional[str] = None
    data: Optional[dict] = None  # For rich responses (charts, time slots)

class ChatRequest(BaseModel):
    message: str
    user_id: str
    conversation_id: Optional[str] = None
    context: Optional[dict] = None  # User's birth details for personalization

class ChatResponse(BaseModel):
    message: str
    data: Optional[dict] = None  # Rich data for UI cards
    insight: Optional[str] = None  # AI insight box
    action: Optional[dict] = None  # Suggested action button
    sources: Optional[List[str]] = None  # Knowledge base sources used

class QuickQuestion(BaseModel):
    icon: str
    text_tamil: str
    text_english: str
    category: str

@router.post("/message", response_model=ChatResponse)
async def send_message(request: Request, chat: ChatRequest):
    """
    Send a message to AI chatbot
    Supports Tamil and English
    Returns rich responses with visual data
    """
    from app.services.ai_chat import AIChatService

    # Get ephemeris from app state for panchangam integration
    ephemeris = getattr(request.app.state, 'ephemeris', None)
    chat_service = AIChatService(ephemeris=ephemeris)

    return await chat_service.process_message(
        message=chat.message,
        user_id=chat.user_id,
        conversation_id=chat.conversation_id,
        context=chat.context
    )

@router.get("/quick-questions")
async def get_quick_questions() -> List[QuickQuestion]:
    """Get suggested quick questions for the chat UI"""
    return [
        QuickQuestion(
            icon="clock",
            text_tamil="இன்று நல்ல நேரம் எப்போது?",
            text_english="What's the auspicious time today?",
            category="time"
        ),
        QuickQuestion(
            icon="calendar",
            text_tamil="இந்த வாரம் எப்படி இருக்கும்?",
            text_english="How will this week be?",
            category="prediction"
        ),
        QuickQuestion(
            icon="heart",
            text_tamil="என் காதல் வாழ்க்கை எப்படி?",
            text_english="How's my love life?",
            category="love"
        ),
        QuickQuestion(
            icon="briefcase",
            text_tamil="தொழில் முன்னேற்றம் உண்டா?",
            text_english="Will there be career growth?",
            category="career"
        ),
        QuickQuestion(
            icon="star",
            text_tamil="இன்றைய ராசிபலன்",
            text_english="Today's horoscope",
            category="horoscope"
        ),
        QuickQuestion(
            icon="alert",
            text_tamil="ராகு காலம் எப்போது?",
            text_english="When is Rahu Kalam?",
            category="time"
        ),
    ]

@router.websocket("/ws/{user_id}")
async def websocket_chat(websocket: WebSocket, user_id: str):
    """
    WebSocket for real-time chat
    Enables streaming responses and voice
    """
    await websocket.accept()

    from app.services.ai_chat import AIChatService

    # Get ephemeris from app state
    ephemeris = getattr(websocket.app.state, 'ephemeris', None)
    chat_service = AIChatService(ephemeris=ephemeris)

    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)

            # Process message
            response = await chat_service.process_message(
                message=message_data.get("message"),
                user_id=user_id,
                context=message_data.get("context")
            )

            await websocket.send_json(response)

    except WebSocketDisconnect:
        print(f"User {user_id} disconnected")

@router.get("/history/{user_id}")
async def get_chat_history(user_id: str, limit: int = 50):
    """Get chat history for a user"""
    from app.services.ai_chat import AIChatService
    
    chat_service = AIChatService()
    return chat_service.get_history(user_id, limit)
