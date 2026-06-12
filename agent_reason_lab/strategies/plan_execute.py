import time
from .base_strategy import BaseReasoningStrategy, AgentTrace
from llm_client import call_solver_llm

class PlanExecuteStrategy(BaseReasoningStrategy):
    def __init__(self, calculator_tool):
        super().__init__(calculator_tool)
        self.name = "Plan-and-Execute"

    def solve(self, problem: str, problem_id: str, ground_truth: str) -> AgentTrace:
        start_ts = time.time()
        steps = []
        total_in = 0
        total_out = 0

        # 第一步：生成解题计划
        plan_prompt = f"请为这道数学题写出分步解题计划：{problem}"
        plan_res, i1, o1, lat1 = call_solver_llm(plan_prompt)
        total_in += i1
        total_out += o1
        steps.append({
            "step_type": "llm_planner",
            "input": plan_prompt,
            "output": plan_res,
            "tokens_in": i1,
            "tokens_out": o1,
            "latency": lat1
        })

        # 第二步：执行计划
        exec_prompt = f"""根据下面的计划解答题目，计算使用 CALC(表达式)
解题计划：{plan_res}
题目：{problem}
请给出最终答案。"""
        exec_res, i2, o2, lat2 = call_solver_llm(exec_prompt)
        total_in += i2
        total_out += o2
        steps.append({
            "step_type": "llm_executor",
            "input": exec_prompt,
            "output": exec_res,
            "tokens_in": i2,
            "tokens_out": o2,
            "latency": lat2
        })

        final_ans = exec_res.strip()
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