import json
import requests

from config import API_KEY
from modules.memory import remember

URL = "https://api.groq.com/openai/v1/chat/completions"


def smart_memory(user_text):

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
User said:

{user_text}

If this contains permanent personal information
(name, age, city, birthday, favourite things, goals etc.)

Reply ONLY like:

{{"save":true,"key":"city","value":"Delhi"}}

Otherwise reply:

{{"save":false}}
"""

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0
    }

    try:

        r = requests.post(
            URL,
            headers=headers,
            json=data
        )

        result = r.json()

        answer = result["choices"][0]["message"]["content"]

        obj = json.loads(answer)

        if obj["save"]:
            remember(obj["key"], obj["value"])
            return f"I'll remember your {obj['key']}."

    except:
        pass

    return None
