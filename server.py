from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from modules.ai import ask_ai

app = Flask(__name__)
CORS(app)

# ==========================
# WEBSITE
# ==========================

@app.route("/")
def index():
    return send_from_directory("NyraWeb", "index.html")


@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("NyraWeb", path)


# ==========================
# AI CHAT API
# ==========================

@app.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "reply": "No data received."
            })

        message = data.get("message", "").strip()

        if message == "":
            return jsonify({
                "reply": "Please type something."
            })

        reply = ask_ai(message)

        return jsonify({
            "reply": reply
        })

    except Exception as e:

        return jsonify({
            "reply": f"Server Error: {e}"
        })


# ==========================
# START SERVER
# ==========================

if __name__ == "__main__":

    print("===================================")
    print("NYRA AI SERVER STARTED")
    print("Open:")
    print("http://127.0.0.1:5000")
    print("===================================")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
