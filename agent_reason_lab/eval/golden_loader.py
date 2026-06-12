import json
import os
from dotenv import load_dotenv

load_dotenv()
GOLDEN_PATH = os.getenv("GOLDEN_SET")

def load_golden_dataset() -> list:
    """加载黄金测试集"""
    with open(GOLDEN_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data