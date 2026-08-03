import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def search_web(query):
    try:
        url = f"https://html.duckduckgo.com/html/?q={query}"

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15
        )

        soup = BeautifulSoup(response.text, "html.parser")

        results = soup.select(".result")

        if not results:
            return "No search results found."

        text = ""

        for i, result in enumerate(results[:5], 1):

            title = result.select_one(".result__title")

            snippet = result.select_one(".result__snippet")

            if title:
                text += f"{i}. {title.get_text(strip=True)}\n"

            if snippet:
                text += snippet.get_text(" ", strip=True)

            text += "\n\n"

        return text.strip()

    except Exception as e:
        return f"Search Error: {e}"
