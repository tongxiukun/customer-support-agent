import os
from agents.schemas import RetrievalRequest
from agents.retriever_agent import RetrieverAgent
from agents.synthesizer_agent import SynthesizerAgent
from agents.safety_agent import SafetyAgent
from safety.input_guard import check_input

class Orchestrator:
    def __init__(self):
        self.retriever = RetrieverAgent()
        self.synth = SynthesizerAgent()
        self.safety = SafetyAgent()
        self.msg_trace = []
        self.max_retry = int(os.getenv("MAX_RETRIES"))

    def log_record(self, sender:str, receiver:str, info:str):
        self.msg_trace.append(f"{sender} → {receiver}: {info}")

    def run(self, user_query:str, user_role="intern"):
        self.log_record("用户","调度器",user_query)
        input_ok,_,safe_q = check_input(user_query)
        if not input_ok:
            return {"answer":"请求被安全护栏拦截","trace":self.msg_trace}
        self.log_record("调度器","检索Agent",safe_q)
        chunk_data = self.retriever.execute(RetrievalRequest(query=safe_q,user_role=user_role)).chunks
        retry_count = 0
        final_ans = None
        while retry_count < self.max_retry:
            self.log_record("调度器","生成Agent","发起答案生成")
            syn_out = self.synth.generate(SynthesisRequest(question=safe_q,chunks=chunk_data))
            self.log_record("生成Agent","安全审核Agent","提交答案校验")
            safety_out = self.safety.review(syn_out,chunk_data)
            if safety_out.approved:
                final_ans = safety_out.final_answer
                break
            retry_count +=1
            self.log_record("安全审核Agent","调度器",f"答案不合格，第{retry_count}次重生成")
        if not final_ans:
            final_ans = "多次生成不符合安全规范，无法回答"
        return {"answer":final_ans,"trace":self.msg_trace}