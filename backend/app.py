
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_session import Session
import numpy as np
import pandas as pd
import tensorflow as tf
import os
from datetime import timedelta


app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Use a strong key in production

# Session config
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # ⬅️ Add here

# Enable sessions
Session(app)

# Enable CORS for frontend (important for cookies to work)
CORS(app, supports_credentials=True)

# Dummy user store (replace with DB in real app)
users = {
    "admin": "password123"
}

# Global CSV state
stored_input = None
stored_actual = None

# Load trained model
model = tf.keras.models.load_model("model/model.h5", compile=False)

# ----------------------- AUTH ROUTES -----------------------

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"success": False, "message": "Username and password required"}), 400

    if username in users:
        return jsonify({"success": False, "message": "Username already exists"}), 409

    users[username] = password
    return jsonify({"success": True, "message": "Registered successfully"})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if users.get(username) == password:
        session['user'] = username
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({"message": "Logged out"})

@app.route('/check_session', methods=['GET'])
def check_session():
    if 'user' in session:
        return jsonify({"logged_in": True})
    return jsonify({"logged_in": False}), 401

# ----------------------- PREDICTION ROUTES -----------------------

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    global stored_input, stored_actual

    if 'user' not in session:
        return jsonify({"error": "Unauthorized"}), 403

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        df = pd.read_csv(file)

        if df.shape[1] < 8:
            return jsonify({"error": "CSV must have at least 8 columns"}), 400

        df = df.dropna().apply(pd.to_numeric, errors='coerce').dropna()

        stored_input = df.iloc[:10, :8].values.tolist()
        stored_actual = df.iloc[:10, 8].values.tolist() if df.shape[1] >= 9 else []

        return jsonify({"message": "CSV uploaded", "actual": stored_actual})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict():
    global stored_input, stored_actual

    if 'user' not in session:
        return jsonify({"error": "Unauthorized"}), 403

    if stored_input is None:
        return jsonify({"error": "No data uploaded yet"}), 400

    data = request.get_json()
    steps = int(data.get("steps", 1))

    try:
        input_array = np.array(stored_input).astype(np.float32)
        input_array = input_array.reshape(1, input_array.shape[0], input_array.shape[1])

        predictions = []
        current_input = input_array

        for _ in range(steps):
            pred = model.predict(current_input)
            predictions.append(pred[0].tolist())
            current_input = np.append(current_input[:, 1:, :], [[stored_input[-1]]], axis=1)

        return jsonify({
            "predictions": predictions,
            "actual": stored_actual[:steps]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ----------------------- MAIN ENTRY -----------------------

if __name__ == '__main__':
    app.run(debug=True)
