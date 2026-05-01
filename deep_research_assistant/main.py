import asyncio
from router.domain_router import DomainRouter
from parallel.map_reduce import MapReduce
from reflection.producer_critic import ProducerCritic
from eval.eval_set import EVAL_SET
from eval.evaluator import calculate_accuracy

async def main():
    router = DomainRouter()
    # 先注释掉路由测评，避免报错
    # print("===== 开始路由准确率测评 =====")
    # acc, df = await calculate_accuracy(router, EVAL_SET)
    # print(f"整体路由准确率：{acc*100:.2f}%")
    # print(df,"\n")

    user_q = input("请输入你的研究问题：")

    print("\n===== 领域路由判断 =====")
    domain, conf, reason = await router.route(user_q)
    print(f"识别领域：{domain} | 置信度：{conf:.2f} | 依据：{reason}")

    if domain == "fallback":
        print("❌ 当前问题无法回答/存在风险，已拦截")
        return

    print("\n===== 并行MapReduce + Best-of-N 执行中 =====")
    mr = MapReduce()
    mr_res, t_parallel, t_seq = await mr.run(user_q, domain)
    print(f"并行耗时：{t_parallel:.2f} s")
    print(f"顺序耗时：{t_seq:.2f} s")
    print(f"并行加速比：{t_seq/t_parallel:.2f} 倍")

    print("\n===== 生产者-评论家 多轮反射优化 =====")
    reflect = ProducerCritic()
    final_report, score_list, draft_history = await reflect.run(user_q, domain, mr_res["summary"])

    print("\n===== 最终研究简报（作业成品）=====")
    print(final_report)

if __name__ == "__main__":
    asyncio.run(main())