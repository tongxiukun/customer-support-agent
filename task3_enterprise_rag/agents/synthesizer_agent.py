import os
from langchain_ollama import OllamaLLM
from agents.schemas import SynthesisRequest, SynthesisResult

class SynthesizerAgent:
    def __init__(self):
        self.llm = OllamaLLM(model=os.getenv("GEN_LLM"))

    def generate(self, req: SynthesisRequest) -> SynthesisResult:
        source_text = "\n".join([f"[{c.chunk_id}] {c.content}" for c in req.chunks])
        prompt = f"""仅使用提供文档作答，必须标注chunk编号，无相关内容回复：I don't have enough information on X
知识库：{source_text}
用户问题：{req.question}"""
        ans = self.llm.invoke(prompt)
        cite_list = [cid.chunk_id for cid in req.chunks if cid.chunk_id in ans]
        return SynthesisResult(answer=ans, citations=cite_list)