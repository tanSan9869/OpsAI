from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class NL2SQLRequest(BaseModel):
    question: str = Field(
        ...,
        description="Natural language operational query",
        example="Show top 5 customers by total order spend"
    )
    explain: bool = Field(
        True,
        description="Whether to return a plain-English explanation of the generated SQL query"
    )

class NL2SQLResponse(BaseModel):
    question: str = Field(..., description="Original natural language user prompt")
    sql_query: str = Field(..., description="Generated safe SELECT SQL query")
    explanation: str = Field(..., description="Human-readable plain English explanation of the SQL query")
    query_results: List[Dict[str, Any]] = Field(default_factory=list, description="Raw rows returned by database execution")
    column_names: List[str] = Field(default_factory=list, description="Column names returned in the query result")
    row_count: int = Field(0, description="Total number of rows returned")
    source: str = Field("openai", description="Source of SQL generation ('openai' or 'fallback')")
    is_safe: bool = Field(True, description="Indicates if the query passed SQLGuard security rules")
    execution_time_ms: float = Field(0.0, description="Total execution time in milliseconds")
