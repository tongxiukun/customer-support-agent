import os
import time
from dotenv import load_dotenv
from openai import OpenAI

# 加载环境变量
load_dotenv()

# 初始化 求解模型 客户端
solver_client = OpenAI(
    api_key=os.getenv("SOLVER_API_KEY"),
    base_url=os.getenv("SOLVER_BASE_URL")
)
SOLVER_MODEL = os.getenv("SOLVER_MODEL")

# 初始化 裁判模型 客户端
judge_client = OpenAI(
    api_key=os.getenv("JUDGE_API_KEY"),
    base_url=os.getenv("JUDGE_BASE_URL")
)
JUDGE_MODEL = os.getenv("JUDGE_MODEL")


def call_solver_llm(prompt: str) -> tuple[str, int, int, float]:
    """
    调用推理求解模型
    :return: 模型回答, 输入token数, 输出token数, 耗时(秒)
    """
    start_time = time.time()
    response = solver_client.chat.completions.create(
        model=SOLVER_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=1024
    )
    cost_time = time.time() - start_time

    content = response.choices[0].message.content.strip()
    prompt_tokens = response.usage.prompt_tokens
    completion_tokens = response.usage.completion_tokens

    return content, prompt_tokens, completion_tokens, cost_time


def call_judge_llm(prompt: str) -> str:
    """调用裁判模型（LLM-as-Judge），仅返回判定结果"""
    response = judge_client.chat.completions.create(
        model=JUDGE_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )
    return response.choices[0].message.content.strip()