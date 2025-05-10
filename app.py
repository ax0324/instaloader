from flask import Flask, request, jsonify
import instaloader

app = Flask(__name__)
L = instaloader.Instaloader()

@app.route("/")
def home():
    return "Welcome to Instaloader Render API!"

@app.route("/download", methods=["POST"])
def download_profile():
    data = request.json
    username = data.get("username")
    if not username:
        return jsonify({"error": "Missing 'username' field"}), 400
    try:
        L.download_profile(username, profile_pic_only=True)
        return jsonify({"message": f"Downloaded profile picture for {username}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500