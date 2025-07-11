from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Load Firebase Admin credentials (this file stays on the server!)
cred = credentials.Certificate("securitykey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route("/get_offer/<user_id>", methods=["GET"])
def get_offer(user_id):
    doc = db.collection("signals").document(user_id).get()
    if doc.exists:
        data = doc.to_dict()
        return jsonify({"offer": data.get("offer")})
    return jsonify({})

@app.route("/send_answer", methods=["POST"])
def send_answer():
    data = request.get_json()
    to_id = data["to"]
    answer = data["answer"]
    db.collection("signals").document(to_id).update({"answer": answer})
    return jsonify({"status": "Answer stored"})

@app.route("/send_offer", methods=["POST"])
def send_offer():
    data = request.get_json()
    to_id = data["to"]
    offer = data["offer"]
    db.collection("signals").document(to_id).set({"offer": offer})
    return jsonify({"status": "Offer stored"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
