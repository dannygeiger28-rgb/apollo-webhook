"""
Apollo.io Webhook Listener — Render.com Deploy
"""

from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

CONTACTS_FILE = "contacts.json"


def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "r") as f:
            return json.load(f)
    return []


def save_contact(contact):
    contacts = load_contacts()
    contacts.append(contact)
    with open(CONTACTS_FILE, "w") as f:
        json.dump(contacts, f, indent=2)


@app.route("/webhook", methods=["POST"])
def apollo_webhook():
    try:
        payload = request.get_json(force=True)
        if not payload:
            return jsonify({"error": "Empty payload"}), 400

        events = payload if isinstance(payload, list) else [payload]
        saved = []

        for event in events:
            contact = {
                "received_at": datetime.utcnow().isoformat() + "Z",
                "first_name":  event.get("first_name", ""),
                "last_name":   event.get("last_name", ""),
                "email":       event.get("email", ""),
                "phone":       event.get("phone_numbers", [{}])[0].get("sanitized_number", "") if event.get("phone_numbers") else "",
                "title":       event.get("title", ""),
                "company":     event.get("organization_name", ""),
                "linkedin":    event.get("linkedin_url", ""),
                "city":        event.get("city", ""),
                "country":     event.get("country", ""),
                "raw":         event,
            }
            save_contact(contact)
            saved.append(f"{contact['first_name']} {contact['last_name']} <{contact['email']}>")
            print(f"[{contact['received_at']}] Saved: {saved[-1]}")

        return jsonify({"status": "ok", "saved": saved}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/contacts", methods=["GET"])
def get_contacts():
    contacts = load_contacts()
    return jsonify({"total": len(contacts), "contacts": contacts}), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "running", "time": datetime.utcnow().isoformat() + "Z"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
