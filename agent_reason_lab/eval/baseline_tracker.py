import json
import os
import argparse
from dotenv import load_dotenv

load_dotenv()
BASE_FILE = os.getenv("BASELINE_FILE")

def save_baseline(data: dict):
    """保存当前结果为基线"""
    with open(BASE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_baseline() -> dict:
    """读取历史基线"""
    if not os.path.exists(BASE_FILE):
        return {}
    with open(BASE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--save", action="store_true", help="保存当前为基线")
    args = parser.parse_args()
    if args.save:
        print("请在 run_eval.py 执行完成后再保存基线")