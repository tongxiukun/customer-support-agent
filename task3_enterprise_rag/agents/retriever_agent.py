from agents.schemas import RetrievalRequest, RetrievalResult
from rag.retrieve import hybrid_retrieve
from rag.rerank import rerank

class RetrieverAgent:
    def execute(self, request: RetrievalRequest) -> RetrievalResult:
        raw_chunks = hybrid_retrieve(request.query, request.user_role)
        final_chunks = rerank(request.query, raw_chunks)
        return RetrievalResult(chunks=final_chunks)