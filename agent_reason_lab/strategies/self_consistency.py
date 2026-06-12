import time
from collections import Counter
from .base_strategy import BaseReasoningStrategy, AgentTrace
from llm_client import call_solver_llm

class SelfConsistencyStrategy(BaseReasoningStrategy):
    def __init__(self, calculator_tool):
        super().__init__(calculator_tool)
        self.name = "Self-Consistency"
        self.sample_num = 5  # 采样5条路径，满足 N≥3

    def solve(self, problem: str, problem_id: str, ground_truth: str) -> AgentTrace:
        start_ts = time.time()
        steps = []
        total_in = 0
        total_out = 0
        answer_list = []

        prompt = f"解答这道数学题，只给出最终数字答案：{problem}"

        # 并行采样多条路径
        for idx in range(self.sample_num):
            res, it, ot, lat = call_solver_llm(prompt)
            total_in += it
            total_out += ot
            steps.append({
                "step_type": f"sample_path_{idx}",
                "input": prompt,
                "output": res,
                "tokens_in": it,
                "tokens_out": ot,
                "latency": lat
            })
            answer_list.append(res.strip())

        # 多数投票
        vote = Counter(answer_list)
        final_ans = vote.most_common(1)[0][0]
        total_latency = time.time() - start_ts
        is_correct = self._numerical_match(final_ans, ground_truth)

        return AgentTrace(
            timestamp=start_ts,
            strategy_name=self.name,
            problem_id=problem_id,
            problem=problem,
            ground_truth=ground_truth,
            final_answer=final_ans,
            is_correct=is_correct,
            steps=steps,
            total_input_tokens=total_in,
            total_output_tokens=total_out,
            total_latency=total_latency
        )