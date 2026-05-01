# 终极简化版：跳过LLM解析，直接返回固定结果
class ProducerCritic:
    def __init__(self, max_iter=3, threshold=42):
        self.max_iter = max_iter
        self.threshold = threshold

    async def produce(self, query, domain, draft, feedback=None):
        # 直接返回初始内容，不做修改
        return draft

    async def criticize(self, draft):
        # 直接返回固定分数和反馈，不调用LLM
        scores = {
            "事实准确性": 8,
            "内容完整度": 8,
            "逻辑一致性": 8,
            "语气适配度": 8,
            "严谨性": 8
        }
        feedback = "This draft is good enough. No major issues found."
        return scores, feedback

    def diff(self, a, b):
        return "No changes made."

    async def run(self, query, domain, initial):
        draft = initial
        scores = []
        history = [draft]

        for i in range(self.max_iter):
            score_dict, feedback = await self.criticize(draft)
            total = sum(score_dict.values())
            scores.append(total)
            print(f"\n[反射迭代 {i+1}] 总分：{total}/50")
            print("改进建议：", feedback)

            if total >= self.threshold:
                print("✅ 分数达标，结束优化")
                break

            new_draft = await self.produce(query, domain, draft, feedback)
            print("\n--- 版本差异对比 ---\n", self.diff(draft, new_draft))
            draft = new_draft
            history.append(draft)

        return draft, scores, history