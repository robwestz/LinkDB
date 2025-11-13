"""
AI Routes for LinkDB Backend

Provides endpoints for:
- AI chat interface
- Automatic insights generation
- Smart recommendations
- Natural language queries
"""

import os
import sys
from typing import Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai.ai_service import ai_service

router = APIRouter(prefix="/api/ai", tags=["ai"])


# Pydantic models
class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    customer_id: Optional[int] = None


class NLQueryRequest(BaseModel):
    query: str
    customer_id: int


# Routes
@router.post("/chat")
async def chat(request: ChatRequest):
    """
    AI chat endpoint.

    Accepts a conversation history and returns AI response.
    Works with or without OpenAI API key (intelligent mock mode).
    """
    try:
        messages = [
            {"role": msg.role, "content": msg.content} for msg in request.messages
        ]
        response = await ai_service.chat(messages)

        return {
            "success": True,
            "data": {"response": response, "mock_mode": ai_service.use_mock},
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/insights/{customer_id}")
async def get_insights(customer_id: int):
    """
    Generate AI insights for a customer.

    Analyzes customer data and provides 5 key insights.
    """
    try:
        # Import here to avoid circular imports
        from services.analyzer_service import AnalyzerService

        # Get customer analysis data
        db_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "data",
            "output",
            "linkops_history.db",
        )
        analyzer_service = AnalyzerService(db_path=db_path)
        customer_data = analyzer_service.get_comprehensive_analysis(customer_id)

        # Generate insights
        insights = await ai_service.generate_insights(customer_data)

        return {
            "success": True,
            "data": {"insights": insights, "mock_mode": ai_service.use_mock},
        }
    except FileNotFoundError:
        # Fallback with mock data if database not found
        mock_insights = [
            "🌟 Länkprofilen visar god övergripande kvalitet",
            "✅ Balanserad fördelning av ankartexer minskar risk",
            "📈 Stabil länkbyggnadshastighet över tid",
            "🌐 Bra diversifiering av publiceringsdomäner",
            "💡 Fortsätt fokusera på naturlig länkbyggnad",
        ]
        return {"success": True, "data": {"insights": mock_insights, "mock_mode": True}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recommendations/{customer_id}")
async def get_recommendations(customer_id: int, target_url: Optional[str] = None):
    """
    Generate AI recommendations for next actions.

    Returns prioritized, actionable recommendations.
    """
    try:
        from services.analyzer_service import AnalyzerService

        db_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "data",
            "output",
            "linkops_history.db",
        )
        analyzer_service = AnalyzerService(db_path=db_path)
        customer_data = analyzer_service.get_comprehensive_analysis(customer_id)

        recommendations = await ai_service.generate_recommendations(
            customer_data, target_url
        )

        return {
            "success": True,
            "data": {
                "recommendations": recommendations,
                "mock_mode": ai_service.use_mock,
            },
        }
    except FileNotFoundError:
        # Fallback mock recommendations
        mock_recommendations = [
            {
                "priority": 1,
                "title": "Optimera ankartextfördelningen",
                "action": "Öka partial match-andelen till 60-70% i nästa kampanj",
                "reasoning": "Minskar risk för över-optimering",
                "impact": "high",
            },
            {
                "priority": 2,
                "title": "Jämna ut länkbyggnadstakten",
                "action": "Sikta på 4-6 länkar per månad med jämn fördelning",
                "reasoning": "Skapar mer naturligt mönster",
                "impact": "medium",
            },
            {
                "priority": 3,
                "title": "Diversifiera källor",
                "action": "Bygg länkar från fler unika domäner i relevanta nischer",
                "reasoning": "Stärker länkprofilens bredd och auktoritet",
                "impact": "medium",
            },
        ]
        return {
            "success": True,
            "data": {"recommendations": mock_recommendations, "mock_mode": True},
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query")
async def natural_language_query(request: NLQueryRequest):
    """
    Answer natural language questions about customer data.

    Example: "Hur många länkar byggde vi förra månaden?"
    """
    try:
        from services.analyzer_service import AnalyzerService

        db_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "data",
            "output",
            "linkops_history.db",
        )
        analyzer_service = AnalyzerService(db_path=db_path)
        customer_data = analyzer_service.get_comprehensive_analysis(request.customer_id)

        answer = await ai_service.natural_language_query(request.query, customer_data)

        return {
            "success": True,
            "data": {"answer": answer, "mock_mode": ai_service.use_mock},
        }
    except Exception as e:
        # Fallback response
        return {
            "success": True,
            "data": {
                "answer": "Jag kunde inte hitta specifik data för din fråga, men jag kan hjälpa dig med allmän analys av din länkprofil. Fråga gärna om övergripande hälsa, risker eller rekommendationer!",
                "mock_mode": True,
            },
        }
