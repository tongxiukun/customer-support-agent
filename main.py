import os
import asyncio
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# Stable free model with minimal rate limits
MODEL = "nvidia/nemotron-3-super-120b-a12b:free"

# ================================
# 1. Prompt Chaining (Sequential Pipeline)
# ================================
class SupportTicketChain:
    def __init__(self):
        self.context = {}

    def run(self, step_name, prompt):
        print(f"\n=== Executing Step: {step_name} ===")
        filled = prompt.format(**self.context)
        res = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": filled}],
            temperature=0.1
        ).choices[0].message.content.strip()
        self.context[step_name] = res
        print(res)
        return res

# ================================
# 2. Routing (Dynamic Branching)
# ================================
def get_route(category):
    if "technical" in category.lower():
        return "technical"
    elif "billing" in category.lower() or "refund" in category.lower():
        return "billing"
    elif "complaint" in category.lower() or "escalate" in category.lower():
        return "complaint"
    else:
        return "general"

def run_route(route, info):
    prompts = {
        "technical": "Generate technical troubleshooting steps for this ticket:\n" + info,
        "billing": "Check refund eligibility and generate a customer response:\n" + info,
        "complaint": "Generate an empathetic response with escalation flag:\n" + info,
        "general": "Match FAQ and generate a clear informational response:\n" + info
    }
    return client.chat.completions.create(
        model=MODEL, messages=[{"role": "user", "content": prompts[route]}]
    ).choices[0].message.content.strip()

# ================================
# 3. Parallelization (Concurrent Sub-tasks)
# ================================
async def sentiment_analysis(text):
    return client.chat.completions.create(
        model=MODEL, messages=[{"role":"user","content":"Classify sentiment (positive/negative/neutral): "+text}]
    ).choices[0].message.content.strip()

async def keyword_extraction(text):
    return client.chat.completions.create(
        model=MODEL, messages=[{"role":"user","content":"Extract key entities and keywords: "+text}]
    ).choices[0].message.content.strip()

async def run_parallel_tasks(text):
    print("\n=== Starting Parallel Tasks ===")
    sentiment, keywords = await asyncio.gather(
        sentiment_analysis(text),
        keyword_extraction(text)
    )
    print(f"Sentiment: {sentiment}")
    print(f"Keywords: {keywords}")
    return {"sentiment": sentiment, "keywords": keywords}

# ================================
# 4. Reflection (Self-Improvement Loop)
# ================================
def reflection_loop(draft, ticket_info):
    print("\n=== Starting Reflection & Improvement Loop ===")
    current_response = draft

    for iteration in range(2):
        print(f"\n--- Iteration {iteration + 1} ---")
        # Step 1: Critique the draft response
        critique_prompt = f"""
        Evaluate this customer support response:
        Ticket Information: {ticket_info}
        Response: {current_response}
        Critique the tone, completeness, accuracy, and provide specific improvement suggestions.
        """
        critique = client.chat.completions.create(
            model=MODEL,
            messages=[{"role":"user","content": critique_prompt}]
        ).choices[0].message.content.strip()
        print("Critique:\n", critique)

        # Step 2: Improve the response based on critique
        improve_prompt = f"""
        Revise the customer support response to address all issues in the critique.
        Only output the final improved response, no extra text.
        Original Response: {current_response}
        Critique: {critique}
        """
        improved = client.chat.completions.create(
            model=MODEL,
            messages=[{"role":"user","content": improve_prompt}]
        ).choices[0].message.content.strip()
        print("Improved Response:\n", improved)
        current_response = improved

    return current_response

# ================================
# Main Pipeline
# ================================
async def process_ticket(raw_text):
    print("=" * 60)
    print("Automated Customer Support Ticket Processor")
    print("Input Ticket:", raw_text)
    print("=" * 60)

    # 1. Prompt Chaining
    chain = SupportTicketChain()
    chain.context["input"] = raw_text
    chain.run("preprocess", "Clean and normalize the text, fix typos, expand abbreviations: {input}")
    chain.run("classify", "Classify the ticket, extract product, issue type, urgency, output JSON: {preprocess}")
    chain.run("draft", "Generate a draft customer response based on the structured data: {classify}")

    # 2. Routing
    route = get_route(chain.context["classify"])
    print(f"\nRouting Decision: {route} branch")
    route_result = run_route(route, chain.context["classify"])
    print("Branch Processing Result:\n", route_result)

    # 3. Parallelization
    parallel_results = await run_parallel_tasks(raw_text)

    # 4. Reflection
    full_ticket_info = chain.context["classify"] + "\n" + str(parallel_results)
    final_response = reflection_loop(chain.context["draft"], full_ticket_info)

    print("\n" + "=" * 60)
    print("✅ Final Customer Response")
    print("=" * 60)
    print(final_response)

# ================================
# Test Cases
# ================================
if __name__ == "__main__":
    test_ticket = "My app crashes when I open the camera."
    asyncio.run(process_ticket(test_ticket))
