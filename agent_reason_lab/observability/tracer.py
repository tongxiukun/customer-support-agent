import json
import os
import time
from dotenv import load_dotenv

load_dotenv()
TRACE_DIR = os.getenv("TRACE_DIR")
os.makedirs(TRACE_DIR, exist_ok=True)
TRACE_FILE = os.path.join(TRACE_DIR, "run_traces.jsonl")

class TraceLogger:
    def __init__(self):
        self.file_path = TRACE_FILE

    def write_trace(self, trace):
        """将单条运行日志写入JSONL"""
        data = {
            "timestamp": trace.timestamp,
            "strategy_name": trace.strategy_name,
            "problem_id": trace.problem_id,
            "problem": trace.problem,
            "ground_truth": trace.ground_truth,
            "final_answer": trace.final_answer,
            "is_correct": trace.is_correct,
            "steps": trace.steps,
            "total_input_tokens": trace.total_input_tokens,
            "total_output_tokens": trace.total_output_tokens,
            "total_latency": trace.total_latency
        }
        with open(self.file_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")