def load_prompt(name: str) -> str:
    with open(f"prompts/{name}.md", "r", encoding="utf-8") as f:
        return f.read()