from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.nl_sql import NL2SQLRequest, NL2SQLResponse
from app.services.chat_service import ChatService
from app.services.nl_sql_service import NL2SQLService
from app.agents.sql_guard import SQLGuardError

router = APIRouter()

@router.post("", response_model=ChatResponse, summary="Operational AI Agent Analysis")
def chat_with_agent(

    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ChatResponse:
    """
    Agentic AI Assistant Endpoint for Operational Data Analysis & Business Recommendations.
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

@router.post("/nl2sql", response_model=NL2SQLResponse, summary="Natural Language to SQL Generation & Execution")
def generate_and_execute_nl2sql(
    request: NL2SQLRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> NL2SQLResponse:
    """
    Dedicated Natural Language -> SQL Endpoint.
    Translates operational question to SQL, validates query safety, explains logic, and executes query.
    """
    try:
        response = NL2SQLService.process_nl_query(db=db, request=request)
        return response
    except SQLGuardError as sge:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"SQL Security Violation: {str(sge)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"NL to SQL processing error: {str(e)}"
        )
