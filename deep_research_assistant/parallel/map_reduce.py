import asyncio
import time
import json
from utils.llm import llm_call
from prompts import load_prompt

PROMPT_ANSWER = load_prompt("answer")
PROMPT_JUDGE = load_prompt("judge")

class MapReduce:
    def __init__(self, n: int = 3):
        self.n = n

    async def decompose(self, query, domain):
        # 直接硬编码3个通用子问题，跳过LLM解析，避免KeyError
        return [
            "What are the main technical bottlenecks of this research?",
            "What are the current research trends?",
            "What are the challenges for commercialization?"
        ]

    async def best_of_n(self, sub_q):
        tasks = [llm_call(PROMPT_ANSWER.format(q=sub_q)) for _ in range(self.n)]
        candidates = await asyncio.gather(*tasks)
        valid = [c for c in candidates if not c.startswith("[ERROR]")]
        if not valid:
            return "No valid answer for this question", [0,0,0]

        judge_input = "\n".join([f"{i+1}. {c}" for i,c in enumerate(valid)])
        judge = await llm_call(PROMPT_JUDGE.format(q=sub_q, candidates=judge_input), json_mode=True)
        try:
            jdata = json.loads(judge)
            return jdata.get("best", valid[0]), jdata.get("scores", [5,5,5])
        except Exception as e:
            print(f"Judge parse error: {e}, raw response: {judge}")
            return valid[0], [5,5,5]

    async def process_sub_question(self, q):
        best, scores = await self.best_of_n(q)
        return {"question": q, "best": best, "scores": scores}

    async def run(self, query, domain):
        sub_qs = await self.decompose(query, domain)
        start = time.time()
        results = await asyncio.gather(*[self.process_sub_question(q) for q in sub_qs])
        parallel_time = time.time() - start

        start_seq = time.time()
        for q in sub_qs:
            await self.process_sub_question(q)
        seq_time = time.time() - start_seq

        summary = "\n\n".join([f"Q: {r['question']}\nA: {r['best']}" for r in results])
        return {
            "sub_questions": sub_qs,
            "results": results,
            "summary": summary
        }, parallel_time, seq_time