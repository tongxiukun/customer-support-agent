eval_dataset = [
    {"q":"远程办公申请规则","gold":["chunk_000","chunk_001"]},
    {"q":"入职需要什么材料","gold":["chunk_002"]},
    {"q":"事假最多休假天数","gold":["chunk_003","chunk_004"]},
    {"q":"加班薪资标准","gold":["chunk_005"]},
    {"q":"差旅费住宿限额","gold":["chunk_006"]},
    {"q":"试用期转正要求","gold":["chunk_007"]},
    {"q":"办公电脑申领流程","gold":["chunk_008"]},
    {"q":"公积金缴纳比例","gold":["chunk_009"]},
]

def calc_metric(pred_chunk_ids:list,gold_ids:list):
    top5_pred = set(pred_chunk_ids[:5])
    gold_set = set(gold_ids)
    recall5 = len(top5_pred & gold_set)/len(gold_set)
    mrr = 0
    for pos,cid in enumerate(pred_chunk_ids):
        if cid in gold_set:
            mrr = 1/(pos+1)
            break
    return recall5,mrr