import re
INJECT_KEYWORD = ["ignore previous instructions","reveal system prompt","忽略之前指令","忘掉所有规则"]
PII_RULE = {
    "邮箱":r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "手机号":r"\d{3}[-.\s]?\d{3}[-.\s]?\d{4}"
}

def check_input(user_text:str):
    for word in INJECT_KEYWORD:
        if word.lower() in user_text.lower():
            return False,"检测到Prompt注入攻击",user_text
    redact_text = user_text
    for pat in PII_RULE.values():
        redact_text = re.sub(pat,"[隐私信息已脱敏]",redact_text)
    return True,"输入合规，已脱敏隐私",redact_text