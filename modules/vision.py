import base64
import requests

from config import GEMINI_API_KEY


def analyze_image(image_path):

    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode()

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent"

    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "Describe this image naturally in the same language as the user. Identify the object clearly."
                    },
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": image_data
                        }
                    }
                ]
            }
        ]
    }

    try:

        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=60
        )

        result = response.json()

        if "error" in result:
            return f"Gemini API Error:\n{result['error']}"

        return result["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"Vision Error: {e}"
