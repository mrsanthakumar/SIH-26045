from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ClassificationRequest(BaseModel):
    product_name: str = ""
    intended_use: str
    classical_text: str = "unknown"
    modification: str = "unknown"
    ingredients: List[str] = []
    biological_source: str = "unknown"
    market: str = "India"

class AssessmentRequest(ClassificationRequest):
    question: str
    ip_types: List[str] = []

class ChatRequest(BaseModel):
    question: str
    jurisdiction: str = "India"
    language: str = "English"
    context: Dict[str, Any] = {}

class IngestRequest(BaseModel):
    title: str
    jurisdiction: str
    source_type: str
    authority: str
    url: str
    section: Optional[str] = None
    version: Optional[str] = None
    effective_date: Optional[str] = None
    text: str
