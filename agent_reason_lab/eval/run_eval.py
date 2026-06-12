import json
import os
from tqdm import tqdm
from dotenv import load_dotenv

# 导入自有模块
from tools.calculator import CalculatorTool
from strategies.react import ReActStrategy
from strategies.plan_execute import PlanExecuteStrategy
from strategies.self_consistency import SelfConsistencyStrategy
from strategies.tree_of_thought import TreeOfThoughtsStrategy
from eval.golden_loader import load_golden_dataset
from eval.metrics import calc_accuracy, bootstrap_95ci, build_win_matrix
from eval.baseline_tracker import load_baseline, save_baseline
from observability.tracer import TraceLogger

load_dotenv()
BOOTSTRAP_SAMPLES = int(os.getenv("BOOTSTRAP_SAMPLES"))

def main():
    # 1. 初始化共享工具
    calc = CalculatorTool()
    # 2. 初始化所有策略
    strategies = [
        ReActStrategy(calc),
        PlanExecuteStrategy(calc),
        SelfConsistencyStrategy(calc),
        TreeOfThoughtsStrategy(calc)
    ]
    strat_names = [s.name for s in strategies]
    # 3. 加载数据集
    dataset = load_golden_dataset()
    # 4. 初始化日志器
    tracer = TraceLogger()

    # 存储结果
    all_results = {name: [] for name in strat_names}
    per_problem_result = {}

    # 遍历所有题目
    for item in tqdm(dataset, desc="评测进度"):
        pid = item["problem_id"]
        prob = item["problem"]
        gt = item["ground_truth"]
        per_problem_result[pid] = {}

        for strat in strategies:
            trace = strat.solve(prob, pid, gt)
            # 写入追踪日志
            tracer.write_trace(trace)
            # 记录正误
            all_results[strat.name].append(int(trace.is_correct))
            per_problem_result[pid][strat.name] = int(trace.is_correct)

    # 5. 计算指标
    report = {}
    print("\n===== 各策略准确率 & 95%置信区间 =====")
    for name in strat_names:
        corr_list = all_results[name]
        acc = calc_accuracy(corr_list)
        ci_low, ci_high = bootstrap_95ci(corr_list, BOOTSTRAP_SAMPLES)
        report[name] = {
            "accuracy": round(acc, 4),
            "ci_95": [ci_low, ci_high]
        }
        print(f"{name} | 准确率: {acc:.2%} | 95%CI: [{ci_low:.2%}, {ci_high:.2%}]")

    # 6. 生成胜负矩阵
    win_mat = build_win_matrix(strat_names, per_problem_result)
    print("\n===== 两两胜负矩阵 =====")
    print("行=胜者，列=负者")
    print(strat_names)
    print(win_mat)

    # 7. 对比基线
    baseline = load_baseline()
    print("\n===== 与历史基线对比 =====")
    for name in strat_names:
        curr_acc = report[name]["accuracy"]
        base_acc = baseline.get(name, {}).get("accuracy", 0.0)
        delta = curr_acc - base_acc
        print(f"{name} | 当前:{curr_acc:.2%} | 基线:{base_acc:.2%} | 变化:{delta:.2%}")

    # 8. 保存本次结果为新基线
    save_baseline(report)
    print("\n✅ 评测完成，结果已保存为新基线")

if __name__ == "__main__":
    main()