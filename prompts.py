# --------------------------
# Prompt Chaining Prompts
# --------------------------
PREPROCESS = """
Clean and normalize this user support message:
1. Fix typos and spelling errors
2. Expand common abbreviations (e.g., "ASAP" → "as soon as possible")
3. Remove emojis, special symbols, and extra whitespace
4. Standardize the format to a clear, professional sentence
Output ONLY the cleaned text, NO extra explanations, NO comments.

User Message: {msg}
"""

CLASSIFY = """
Classify this support ticket into EXACTLY ONE category from the list: technical, billing, inquiry, complaint.
Also extract the following entities:
- product: the product the user is referring to (e.g., "mobile app", "subscription")
- issue: a brief description of the user's problem
- urgency: the urgency level (high/medium/low)
Output ONLY a valid JSON object, NO extra text, NO explanations, in this format:
{"category":"...", "product":"...", "issue":"...", "urgency":"..."}

Ticket Text: {text}
"""

DRAFT_REPLY = """
Write a polite, professional draft reply to the customer based on the following information:
- Category: {cat}
- Product: {prod}
- Issue: {issue}
- Urgency: {urgency}
The reply should acknowledge the user's issue, be empathetic, and offer a clear next step.
"""

# --------------------------
# Routing Prompts (4 branches)
# --------------------------
ROUTE_TECHNICAL = """
Provide clear, step-by-step troubleshooting steps for the following technical issue:
{text}
The steps should be easy to follow for a non-technical user.
"""

ROUTE_BILLING = """
Explain the company's refund/billing policy for the following issue, and check if the user is eligible for a refund:
{text}
Be clear, transparent, and professional.
"""

ROUTE_INQUIRY = """
Answer the following general customer inquiry clearly and concisely:
{text}
Provide accurate, helpful information in a friendly tone.
"""

ROUTE_COMPLAINT = """
Write an empathetic apology to the customer for their complaint, acknowledge their frustration, and offer to escalate the issue to a support team:
{text}
The tone should be sincere and reassuring.
"""

# --------------------------
# Parallelization Prompts (2 tasks)
# --------------------------
PARALLEL_SENTIMENT = """
Analyze the sentiment of the following customer support message.
Output ONLY ONE word: positive, negative, or neutral.

Message: {text}
"""

PARALLEL_KEYWORDS = """
Extract 3-5 relevant keywords from the following customer support message, separated by commas.
Output ONLY the keywords, NO extra text.

Message: {text}
"""

# --------------------------
# Reflection Prompts (self-evaluation + improvement)
# --------------------------
REFLECT_EVALUATE = """
Evaluate this customer support reply based on the following criteria:
1. Tone: Is it polite, empathetic, and professional?
2. Completeness: Does it address the user's issue fully?
3. Accuracy: Is the information correct and relevant?
4. Clarity: Is it easy to understand?

Output ONLY a valid JSON object, NO extra text, in this format:
{"score": 1-10, "suggestions": ["list 2-3 specific, actionable improvements"]}

Reply to evaluate: {reply}
User Sentiment: {sentiment}
Relevant Keywords: {keywords}
"""

REFLECT_IMPROVE = """
Improve the following customer support reply using the evaluation suggestions provided.
Make the tone more empathetic, the content more complete, and the language clearer.
Output ONLY the improved reply, NO extra text, NO explanations.

Original Reply: {old_reply}
Evaluation Suggestions: {evaluation}
"""
