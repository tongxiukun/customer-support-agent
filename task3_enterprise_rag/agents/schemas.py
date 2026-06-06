from pydantic import BaseModel
from typing import List, Optional, Dict

class DocumentChunk(BaseModel):
    chunk_id: str
    content: str
    metadata: Dict
    dense_score: Optional[float] = None
    bm25_score: Optional[float] = None
    rerank_score: Optional[float] = None

class RetrievalRequest(BaseModel):
    query: str
    user_role: str = "intern"

class RetrievalResult(BaseModel):
    chunks: List[DocumentChunk]

class SynthesisRequest(BaseModel):
    question: str
    chunks: List[DocumentChunk]

class SynthesisResult(BaseModel):
    answer: str
    citations: List[str]

class SafetyVerdict(BaseModel):
    approved: bool
    feedback: Optional[str] = None
    final_answer: Optional[str] = None