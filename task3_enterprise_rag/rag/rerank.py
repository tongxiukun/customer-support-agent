from transformers import AutoTokenizer,AutoModelForSequenceClassification
import torch
from agents.schemas import DocumentChunk

rerank_model_name = "cross-encoder/ms-marco-MiniLM-L-6-v2"
tokenizer = AutoTokenizer.from_pretrained(rerank_model_name)
model = AutoModelForSequenceClassification.from_pretrained(rerank_model_name)

def rerank(query:str,chunks:list[DocumentChunk]):
    if not chunks:
        return []
    query_doc_pairs = [[query,c.content] for c in chunks]
    inputs = tokenizer(query_doc_pairs,padding=True,truncation=True,return_tensors="pt")
    with torch.no_grad():
        scores = model(**inputs).logits.squeeze()
    for idx,c in enumerate(chunks):
        c.rerank_score = float(scores[idx])
    return sorted(chunks,key=lambda x:x.rerank_score,reverse=True)[:5]