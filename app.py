from datetime import datetime, timezone
import json
from pathlib import Path

from flask import Flask, jsonify, request


BASE_DIR = Path(__file__).resolve().parent
SUBMISSIONS_FILE = BASE_DIR / "submissions.jsonl"

app = Flask(__name__, static_folder=".", static_url_path="")


@app.get("/")
def home():
    return app.send_static_file("index.html")


@app.post("/api/contact")
def contact():
    payload = request.form if request.form else (request.get_json(silent=True) or {})

    name = str(payload.get("name", "")).strip()
    email = str(payload.get("email", "")).strip()
    message = str(payload.get("message", "")).strip()

    if not name or not email or not message:
        return jsonify(success=False, message="Please fill out all contact form fields."), 400

    entry = {
        "name": name,
        "email": email,
        "message": message,
        "submitted_at": datetime.now(timezone.utc).isoformat(),
    }

    with SUBMISSIONS_FILE.open("a", encoding="utf-8") as file_handle:
        file_handle.write(json.dumps(entry, ensure_ascii=True) + "\n")

    return jsonify(success=True, message="Thanks for reaching out. Your message was saved successfully."), 200


if __name__ == "__main__":
    app.run(debug=True)