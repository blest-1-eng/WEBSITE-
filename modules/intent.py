import json
import requests
from config import API_KEY

URL = "https://api.groq.com/openai/v1/chat/completions"


SYSTEM_PROMPT = """
You are an intent classifier.

Return ONLY valid JSON.

Supported intents:

guardian_on
guardian_off
guardian_status

study_start
study_stop
study_status

battery
location
camera
browser
torch_on
torch_off

time
date

remember
recall
note
calculate
reminder

search

bye

chat

Examples:

User: ye kya hai
{"intent":"vision"}

User: isko dekh
{"intent":"vision"}

User: what is this
{"intent":"vision"}

User: can you identify this
{"intent":"vision"}

User: is photo me kya hai
{"intent":"vision"}

User: guardian mode on
{"intent":"guardian_on"}

User: turn on guardian
{"intent":"guardian_on"}

User: enable guardian
{"intent":"guardian_on"}

User: guardian mode off
{"intent":"guardian_off"}

User: battery percentage
{"intent":"battery"}

User: open browser
{"intent":"browser"}

User: turn on torch
{"intent":"torch_on"}

User: turn off torch
{"intent":"torch_off"}

User: latest ai news
{"intent":"search","query":"latest ai news"}

User: Delhi weather
{"intent":"search","query":"Delhi weather"}

User: Weather today
{"intent":"search","query":"Weather today"}

User: Who is Elon Musk
{"intent":"search","query":"Who is Elon Musk"}

User: CBSE result
{"intent":"search","query":"CBSE result"}

User: Python tutorial
{"intent":"search","query":"Python tutorial"}

User: Latest technology news
{"intent":"search","query":"Latest technology news"}

User: IPL points table
{"intent":"search","query":"IPL points table"}

User: ChatGPT updates
{"intent":"search","query":"ChatGPT updates"}

User: search latest ai news
{"intent":"search","query":"latest ai news"}

User: goodbye
{"intent":"bye"}

User: exit
{"intent":"bye"}

User: see you
{"intent":"bye"}

Everything else:

{"intent":"chat"}

Never explain.
Never use markdown.
Reply ONLY JSON.
"""
def detect_intent(user_input):

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        "temperature": 0,
        "max_tokens": 100
    }

    try:

        response = requests.post(
            URL,
            headers=headers,
            json=data,
            timeout=20
        )

        if response.status_code == 200:

            answer = response.json()["choices"][0]["message"]["content"].strip()

            return json.loads(answer)

    except Exception:
        pass

    return {
        "intent": "chat"
    }
