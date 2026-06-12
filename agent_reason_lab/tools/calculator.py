import os
import time
from dotenv import load_dotenv

load_dotenv()
TIMEOUT = int(os.getenv("CALCULATOR_TIMEOUT", 5))

class CalculatorTool:
    def __init__(self):
        self.timeout = TIMEOUT

    def run(self, expression: str) -> str:
        """
        安全计算器，执行数学表达式
        :param expression: 数学公式字符串
        :return: 计算结果 / 错误提示
        """
        try:
            start = time.time()
            # 限制内置函数，保证安全
            result = str(eval(expression, {"__builtins__": None}, {}))
            if time.time() - start > self.timeout:
                return "Error: 计算超时"
            return result
        except Exception as e:
            return f"Error: 计算失败 -> {str(e)}"