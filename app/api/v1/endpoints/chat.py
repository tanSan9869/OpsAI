from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from app.agents.sql_guard import SQLGuardError

router = APIRouter()

@router.post("", response_model=ChatResponse, summary="Operational AI Agent Analysis")
@router.post("/", response_model=ChatResponse, summary="Operational AI Agent Analysis")
def chat_with_agent(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ChatResponse:
    """
    Agentic AI Assistant Endpoint for Operational Data Analysis.
    
    Workflow:
    1. Understand user natural language question.
    2. Generate safe SELECT SQL query.
    3. Execute query on operational database.
    4. Analyze data & extract operational insights.
    5. Return prioritized business recommendations.
    """
    try:
        response = ChatService.process_chat_query(db=db, request=request)
        return response
    except SQLGuardError as sge:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Security Policy Violation: {str(sge)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI Agent Analysis failed: {str(e)}"
        )
