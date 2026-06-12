import time
from .base_strategy import BaseReasoningStrategy, AgentTrace
from llm_client import call_solver_llm

class TreeOfThoughtsStrategy(BaseReasoningStrategy):
    def __init__(self, calculator_tool):
        super().__init__(calculator_tool)
        self.name = "Tree-of-Thoughts"
        self.branch_num = 2   # 每步至少2个分支
        self.max_depth = 3    # 思考树最大深度

    def solve(self, problem: str, problem_id: str, ground_truth: str) -> AgentTrace:
        start_ts = time.time()
        steps = []
        total_in = 0
        total_out = 0
        # 节点结构: {"content":思考内容, "score":分数, "depth":深度}
        current_nodes = [{"content": problem, "score": 1.0, "depth": 0}]

        for depth in range(self.max_depth):
            new_nodes = []
            for node in current_nodes:
                # 生成分支思路
                branch_prompt = f"针对题目，给出{self.branch_num}种不同解题思路：{node['content']}"
                branch_res, it1, ot1, lat1 = call_solver_llm(branch_prompt)
                total_in += it1
                total_out += ot1
                steps.append({
                    "step_type": f"tot_branch_d{depth}",
                    "input": branch_prompt,
                    "output": branch_res,
                    "tokens_in": it1,
                    "tokens_out": ot1,
                    "latency": lat1
                })

                # 对每个分支打分
                branches = [b.strip() for b in branch_res.split("\n") if b.strip()]
                for branch in branches[:self.branch_num]:
                    score_prompt = f"给这条解题思路打分(0~1)：{branch}"
                    score_res, it2, ot2, lat2 = call_solver_llm(score_prompt)
                    total_in += it2
                    total_out += ot2
                    steps.append({
                        "step_type": "tot_score",
                        "input": score_prompt,
                        "output": score_res,
                        "tokens_in": it2,
                        "tokens_out": ot2,
                        "latency": lat2
                    })
                    # 解析分数
                    try:
                        score = float(score_res)
                    except:
                        score = 0.0
                    new_nodes.append({
                        "content": branch,
                        "score": score,
                        "depth": depth + 1
                    })
            # 保留分数最高的节点
            current_nodes = sorted(new_nodes, key=lambda x: x["score"], reverse=True)[:4]

        # 取最优分支作为最终答案
        best_node = current_nodes[0] if current_nodes else {"content": "无答案"}
        final_ans = best_node["content"]
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