import os
import json
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()
client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

async def llm_call(prompt: str, model: str = None, json_mode: bool = False):
    try:
        body = {
            "model": model or os.getenv("PRODUCER_MODEL"),
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3
        }
        if json_mode:
            body["response_format"] = {"type": "json_object"}

        response = await asyncio.wait_for(
            client.chat.completions.create(**body),
            timeout=int(os.getenv("TIMEOUT_SECONDS"))
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[ERROR] {str(e)}"