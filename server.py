users_db = {}

from flask import Flask, request, jsonify, render_template, send_from_directory
from services.audio_service import compare_voices, get_embedding
import os
import numpy as np

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VOICE_DIR = os.path.join(BASE_DIR, "voice_input")

os.makedirs(VOICE_DIR, exist_ok=True)


@app.route("/stylesheet/<path:filename>")
def styles(filename):
    return send_from_directory("templates/stylesheet", filename)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/compare", methods=["POST"])
def compare_voice():
    try:
        file1 = request.files.get("file1")
        file2 = request.files.get("file2")

        if not file1 or not file2:
            return jsonify({"error": "Both audio files are required"}), 400

        f1_path = os.path.join(VOICE_DIR, "voice1_input.wav")
        f2_path = os.path.join(VOICE_DIR, "voice2_input.wav")

        file1.save(f1_path)
        file2.save(f2_path)

        result = compare_voices(f1_path, f2_path)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/register", methods=["POST"])
def register():
    try:
        username = request.form.get("username")
        file = request.files.get("file")

        if not username or not file:
            return jsonify({"error": "username and voice file required"}), 400

        file_path = os.path.join(VOICE_DIR, f"{username}.wav")
        file.save(file_path)

        embedding = compare_voembedding = get_embedding(file_path)

        # store user voice profile
        users_db[username] = embedding.tolist()

        return jsonify(
            {"message": "User registered successfully", "username": username}
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/login", methods=["POST"])
def login():
    try:
        username = request.form.get("username")
        file = request.files.get("file")

        if not username or not file:
            return jsonify({"error": "username and voice file required"}), 400

        if username not in users_db:
            return jsonify({"error": "user not found"}), 404

        temp_path = os.path.join(VOICE_DIR, "login_temp.wav")
        file.save(temp_path)

        # ✅ FIX: correct function usage
        new_embedding = get_embedding(temp_path)
        stored_embedding = np.array(users_db[username])

        # distance calculation
        distance = np.linalg.norm(new_embedding - stored_embedding)

        # ✅ FIX: realistic threshold for MFCC distance
        threshold = 50

        authenticated = bool(distance < threshold)

        return jsonify(
            {
                "username": username,
                "distance": float(distance),
                "threshold": threshold,
                "authenticated": authenticated,
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
