def check_grounding(answer:str,chunk_list):
    chunk_id_list = [c.chunk_id for c in chunk_list]
    if any(cid in answer for cid in chunk_id_list):
        return True,"答案已溯源合规"
    return False,"答案无知识库引用，疑似幻觉生成"