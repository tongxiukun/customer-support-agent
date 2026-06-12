# 运行完整评测流程
eval:
	python eval/run_eval.py

# 回放指定ID的日志示例：make replay id=p001
replay:
	python observability/replay.py --id $(id)

# 保存当前结果为新基线
save-baseline:
	python eval/baseline_tracker.py --save