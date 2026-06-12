import time
from .base_strategy import BaseReasoningStrategy, AgentTrace
from llm_client import call_solver_llm

class ReActStrategy(BaseReasoningStrategy):
    def __init__(self, calculator_tool):
        super().__init__(calculator_tool)
        self.name = "ReAct"
        self.max_loop = 8  # 最大循环步数，防止死循环

    def solve(self, problem: str, problem_id: str, ground_truth: str) -> AgentTrace:
        start_ts = time.time()
        steps = []
        total_in_tok = 0
        total_out_tok = 0
        current_prompt = f"""请一步步解决数学题。
遇到计算请使用格式：CALC(数学表达式)
题目：{problem}
"""
        final_ans = "无答案"

        for _ in range(self.max_loop):
            # 1. 调用LLM推理
            llm_out, in_tok, out_tok, lat = call_solver_llm(current_prompt)
            total_in_tok += in_tok
            total_out_tok += out_tok

            steps.append({
                "step_type": "llm_reason",
                "input": current_prompt,
                "output": llm_out,
                "tokens_in": in_tok,
                "tokens_out": out_tok,
                "latency": lat
            })

            # 2. 检测工具调用
            if "CALC(" in llm_out:
                expr = llm_out.split("CALC(")[-1].split(")")[0].strip()
                tool_res = self.calculator.run(expr)
                steps.append({
                    "step_type": "tool_calculator",
                    "input": expr,
                    "output": tool_res,
                    "latency": time.time() - start_ts
                })
                # 3. 观察结果，拼接进入下一轮
                current_prompt += f"\n工具返回结果：{tool_res}"
                continue

            # 检测最终答案
            if "最终答案" in llm_out:
                final_ans = llm_out.split("最终答案")[-1].strip()
                break

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
            total_input_tokens=total_in_tok,
            total_output_tokens=total_out_tok,
            total_latency=total_latency
        )