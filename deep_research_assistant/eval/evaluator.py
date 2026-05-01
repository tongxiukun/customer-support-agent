import pandas as pd

async def calculate_accuracy(router, eval_set):
    correct = 0
    rows = []
    for q, true_label in eval_set:
        pred, conf, _ = await router.route(q)
        ok = 1 if pred == true_label else 0
        correct += ok
        rows.append([q, true_label, pred, ok])
    df = pd.DataFrame(rows, columns=["问题","真实分类","预测分类","是否正确"])
    return round(correct/len(eval_set),3), df