from rank_bm25 import BM25Okapi
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from agents.schemas import DocumentChunk

def hybrid_retrieve(query:str,role="intern"):
    embed = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.load_local("faiss_index",embed,allow_dangerous_deserialization=True)
    dense_res = db.similarity_search_with_score(query,k=10)
    chunk_list = []
    for doc,score in dense_res:
        chunk_list.append(DocumentChunk(chunk_id=doc.metadata["chunk_id"],content=doc.page_content,metadata=doc.metadata,dense_score=float(score)))
    token_corpus = [c.content.split() for c in chunk_list]
    bm25 = BM25Okapi(token_corpus)
    bm_scores = bm25.get_scores(query.split())
    for idx,item in enumerate(chunk_list):
        item.bm25_score = float(bm_scores[idx])
    for pos,chunk in enumerate(chunk_list):
        chunk.rrf_score = 1/(pos+60)
    sorted_chunk = sorted(chunk_list,key=lambda x:x.rrf_score,reverse=True)
    filter_chunk = [c for c in sorted_chunk if c.metadata["min_role"]==role or role=="manager"]
    return filter_chunk[:10]