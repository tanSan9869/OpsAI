from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    question: str = Field(..., description="Operational question or analysis request in natural language", example="Show delayed orders.")
    conversation_id: Optional[str] = Field(None, description="Optional conversation context identifier")

class ChatResponse(BaseModel):
    question: str = Field(..., description="Original user question")
    sql_query: str = Field(..., description="Generated safe SELECT SQL query")
    query_results: List[Dict[str, Any]] = Field(default_factory=list, description="Executed SQL query output rows")
    row_count: int = Field(0, description="Total number of rows returned")
    summary: str = Field(..., description="Concise operational summary of findings")
    analysis: str = Field(..., description="Detailed operational analysis of the data")
    insights: List[str] = Field(default_factory=list, description="Key operational insights extracted")
    recommendations: List[str] = Field(default_factory=list, description="Actionable business recommendations")
    reasoning_steps: List[str] = Field(default_factory=list, description="Step-by-step AI Agent reasoning chain")
    execution_time_ms: float = Field(0.0, description="Total execution time in milliseconds")
