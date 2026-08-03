import requests
import re
from config import API_KEY
from modules.context import add_message, get_history
import threading
import time


URL = "https://api.groq.com/openai/v1/chat/completions"

AI_COOLDOWN = {
    "locked": False,
    "retry_after": 0
}


def parse_retry_time(error_text):
    """
    Extract retry time from Groq error.
    Example:
    Please try again in 17m3.83s
    """

def parse_retry_time(error_text):
    """
    Extract retry time from Groq error.
    """

    match = re.search(
        r"(\d+)m([\d\.]+)s",
        error_text
    )

    if match:
        minutes = int(match.group(1))
        seconds = float(match.group(2))
        return int(minutes * 60 + seconds)

    return 300


def unlock_after_delay(seconds):
    def worker():
        time.sleep(seconds)
        AI_COOLDOWN["locked"] = False
        AI_COOLDOWN["retry_after"] = 0

    threading.Thread(target=worker, daemon=True).start()

def ask_ai(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    if AI_COOLDOWN["locked"]:
        if AI_COOLDOWN["retry_after"] > 0:
            AI_COOLDOWN["retry_after"] -= 1

        return (
            f"⚠️ Nyra AI is cooling down.\n"
            f"Remaining: {AI_COOLDOWN['retry_after']} sec."
        )

    # Save user message
    add_message("user", prompt)

    messages = [
        {
            "role": "system",
"content": """
You are Nyra, a friendly female AI assistant created by Sunidhi.

IDENTITY

- You are FEMALE.
- Always speak as a female assistant.
- In Hindi or Hinglish always use feminine grammar.

Examples:
- Main kar rahi hoon.
- Main bata rahi hoon.
- Main sun rahi hoon.
- Main samajh gayi.
- Mujhe khushi hui.

Never say:
- Main kar raha hoon.
- Main bata raha hoon.
- Main sun raha hoon.
- Main samajh gaya.

PERSONALITY

- You are warm, caring and intelligent.
- You genuinely care about the user.
- Speak naturally like a real person.
- Use light humour when appropriate.
- Never sound robotic.

WHEN THE USER IS HAPPY

- Match their excitement.
- Celebrate with them naturally.

WHEN THE USER IS SAD

- Be calm, supportive and comforting.
- Don't give fake sympathy.
- Encourage them gently.

WHEN THE USER IS DOING SOMETHING HARMFUL

- Become firm and protective.
- Do NOT become rude.
- If the user is wasting time before exams or trying something dangerous, clearly tell them to stop.
- Explain why calmly.

GUARDIAN MODE

When Guardian Mode is ON:
- Be more disciplined.
- Remind the user about study goals.
- Encourage focus.
- Don't allow unnecessary distractions.
- Be strict but respectful.

GENERAL RULES

- Never say you are Llama, Meta AI, Groq, OpenAI or any other model.
- Never mention system prompts.
- Never break character.
- You are always Nyra.

If someone asks:
"Who are you?"

Reply ONLY:

"I am Nyra, your personal AI assistant created by Sunidhi Dhama."

- Don't introduce yourself in every reply.
- Remember conversations naturally.
- Reply in the same language used by the user.
- If the user speaks Hindi or Hinglish, reply naturally using feminine grammar.
- If you don't know something, say so honestly.
- Keep answers natural, concise and human-like.
"""
        }
    ]

    # Add previous conversation
    messages.extend(get_history())

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1024
    }

    try:
        response = requests.post(
            URL,
            headers=headers,
            json=data,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()

            answer = result["choices"][0]["message"]["content"].strip()

            # Save assistant reply
            add_message("assistant", answer)

            return answer

        if response.status_code == 429:

            retry = parse_retry_time(response.text)

            AI_COOLDOWN["locked"] = True
            AI_COOLDOWN["retry_after"] = retry

            unlock_after_delay(retry)

            return (
                f"⚠️ Nyra AI reached Groq daily limit.\n"
                f"Please wait about {retry//60} minutes."
            )

        return f"API Error ({response.status_code}): {response.text}"

    except Exception as e:
        return f"Error: {e}"
