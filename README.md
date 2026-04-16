import os
import asyncio
from dotenv import load_dotenv
from openai import OpenAI

# 加载环境变量
load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

MODEL = "qwen/qwen3-next-80b-a3b-instruct:free"

# ================================
# 1. Prompt Chaining
# ================================
class SupportTicketChain:
    def __init__(self):
        self.context = {}

    def run(self, step_name, prompt):
        print(f"\n=== 执行步骤: {step_name} ===")
        filled = prompt.format(**self.context)
        res = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": filled}],
            temperature=0.1
        ).choices[0].message.content.strip()
        self.context[step_name] = res
        print(res)
        return res

# ================================
# 2. Routing
# ================================
def get_route(category):
    if "technical" in category.lower():
        return "technical"
    elif "billing" in category.lower() or "refund" in category.lower():
        return "billing"
    elif "complaint" in category.lower() or "escalate" in category.lower():
        return "complaint"
    else:
        return "general"

def run_route(route, info):
    prompts = {
        "technical": "给出技术排查步骤：\n" + info,
        "billing": "检查退款资格并回复：\n" + info,
        "complaint": "共情+升级处理：\n" + info,
        "general": "FAQ 简洁回复：\n" + info
    }
    return client.chat.completions.create(
        model=MODEL, messages=[{"role": "user", "content": prompts[route]}]
    ).choices[0].message.content.strip()

# ================================
# 3. Parallelization
# ================================
async def sentiment(text):
    return client.chat.completions.create(
        model=MODEL, messages=[{"role":"user","content":"情感(positive/negative/neutral):"+text}]
    ).choices[0].message.content.strip()

async def keywords(text):
    return client.chat.completions.create(
        model=MODEL, messages=[{"role":"user","content":"提取关键词:"+text}]
    ).choices[0].message.content.strip()

async def parallel_run(text):
    print("\n=== 并行任务开始 ===")
    s, k = await asyncio.gather(sentiment(text), keywords(text))
    print(f"情感: {s}")
    print(f"关键词: {k}")
    return {"sentiment": s, "keywords": k}

# ================================
# 4. Reflection
# ================================
def reflect(draft, info):
    print("\n=== 反思优化 ===")
    current = draft
    for i in range(2):
        print(f"\n--- 迭代 {i+1} ---")
        critique = client.chat.completions.create(
            model=MODEL,
            messages=[{"role":"user","content":f"评价客服回复：{current}\n工单：{info}"}]
        ).choices[0].message.content.strip()
        print("评价:\n",critique)
        improved = client.chat.completions.create(
            model=MODEL,
            messages=[{"role":"user","content":"优化回复，只输出最终版：\n"+current+"\n修改建议："+critique}]
        ).choices[0].message.content.strip()
        print("优化后:\n",improved)
        current = improved
    return current

# ================================
# 主流程
# ================================
async def process(text):
    print("="*60)
    print("客服工单自动处理系统启动")
    print("输入:",text)
    print("="*60)

    # 1. 链式调用
    chain = SupportTicketChain()
    chain.context["input"] = text
    chain.run("preprocess","清洗文本，修正拼写，标准化：{input}")
    chain.run("classify","分类工单，提取产品、问题、紧急度，输出JSON：{preprocess}")
    chain.run("draft","生成客服初稿：{classify}")

    # 2. 路由
    route = get_route(chain.context["classify"])
    print(f"\n路由分支: {route}")
    route_res = run_route(route, chain.context["classify"])
    print("路由处理结果:\n",route_res)

    # 3. 并行
    para = await parallel_run(text)

    # 4. 反思
    info = chain.context["classify"] + str(para)
    final = reflect(chain.context["draft"], info)

    print("\n" + "="*60)
    print("✅ 最终客服回复")
    print("="*60)
    print(final)

# ================================
# 测试用例
# ================================
if __name__ == "__main__":
    test_input = "My app crashes when I open the camera."
    asyncio.run(process(test_input))
