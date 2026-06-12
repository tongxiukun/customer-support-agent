import numpy as np
from scipy import stats

def calc_accuracy(correct_list: list) -> float:
    """计算准确率"""
    total = len(correct_list)
    correct = sum(correct_list)
    return correct / total if total > 0 else 0.0

def bootstrap_95ci(correct_list: list, n_samples: int = 1000) -> tuple[float, float]:
    """Bootstrap 计算95%置信区间"""
    arr = np.array(correct_list)
    n = len(arr)
    samples = []
    for _ in range(n_samples):
        idx = np.random.randint(0, n, n)
        sample = arr[idx]
        samples.append(sample.mean())
    samples = np.array(samples)
    lower = np.percentile(samples, 2.5)
    upper = np.percentile(samples, 97.5)
    return round(lower, 4), round(upper, 4)

def build_win_matrix(strategy_names: list, results: dict) -> np.ndarray:
    """构建策略两两胜负矩阵"""
    n = len(strategy_names)
    win_mat = np.zeros((n, n), dtype=int)
    for pid in results:
        res = results[pid]
        for i, s1 in enumerate(strategy_names):
            for j, s2 in enumerate(strategy_names):
                if i == j:
                    continue
                if res[s1] > res[s2]:
                    win_mat[i][j] += 1
    return win_mat