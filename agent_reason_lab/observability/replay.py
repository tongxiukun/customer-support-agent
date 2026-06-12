import json
import argparse
import os
from dotenv import load_dotenv

load_dotenv()
TRACE_DIR = os.getenv("TRACE_DIR")
TRACE_FILE = os.path.join(TRACE_DIR, "run_traces.jsonl")

def replay_trace(problem_id: str):
    """根据题目ID回放日志"""
    if not os.path.exists(TRACE_FILE):
        print("暂无日志文件")
        return
    with open(TRACE_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            item = json.loads(line)
            if item["problem_id"] == problem_id:
                print("===== 回放追踪日志 =====")
                print(json.dumps(item, ensure_ascii=False, indent=2))
                return
    print(f"未找到 ID = {problem_id} 的日志")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True, help="题目ID，例如 p001")
    args = parser.parse_args()
    replay_trace(args.id)