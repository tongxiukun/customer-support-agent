from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any

# 单条推理运行的完整追踪日志结构体
@dataclass
class AgentTrace:
    timestamp: float               # 运行时间戳
    strategy_name: str             # 策略名称
    problem_id: str                 # 题目ID
    problem: str                    # 题目内容
    ground_truth: str               # 标准答案
    final_answer: str               # 模型最终答案
    is_correct: bool                # 是否答对
    steps: List[Dict[str, Any]]     # 每一步日志(LLM调用/工具调用)
    total_input_tokens: int         # 总输入Token
    total_output_tokens: int        # 总输出Token
    total_latency: float            # 总耗时(秒)


# 所有推理策略的统一抽象基类
class BaseReasoningStrategy(ABC):
    def __init__(self, calculator_tool):
        self.calculator = calculator_tool  # 注入共享计算器
        self.name = "base"

    @abstractmethod
    def solve(self, problem: str, problem_id: str, ground_truth: str) -> AgentTrace:
        """统一解题入口，必须被子类实现"""
        pass

    def _numerical_match(self, pred: str, gt: str) -> bool:
        """数学题数值匹配（允许微小浮点误差）"""
        try:
            pred_num = float(pred.strip())
            gt_num = float(gt.strip())
            return abs(pred_num - gt_num) < 1e-3
        except:
            return False