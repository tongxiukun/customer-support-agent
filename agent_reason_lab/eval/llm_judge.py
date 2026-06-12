from llm_client import call_judge_llm

def judge_answer(problem: str, pred: str, gt: str) -> str:
    """LLM裁判判断答案是否正确，返回 正确/错误"""
    prompt = f"""题目：{problem}
标准答案：{gt}
模型答案：{pred}
请判断模型答案是否正确，只回复“正确”或“错误”。"""
    return call_judge_llm(prompt)

def calc_judge_human_agreement(judge_res: list, human_res: list) -> float:
    """计算裁判与人工标注的一致率"""
    total = len(judge_res)
    match = sum(1 for j, h in zip(judge_res, human_res) if j == h)
    return match / total if total > 0 else 0.0