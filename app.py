from flask import Flask, jsonify, request
from fall_detection import predict_fall_and_alert
import os

app = Flask(__name__)

# Security token for basic GET access
API_SECRET_TOKEN = os.environ.get("API_SECRET_TOKEN", "mysecrettoken123")

@app.route('/')
def home():
    return jsonify({"message": "✅ Fall Detection API is up and running!"})

@app.route('/run-prediction', methods=['GET'])
def run_prediction():
    token = request.args.get('token')

    if token != API_SECRET_TOKEN:
        return jsonify({'error': 'Unauthorized ❌'}), 401

    result = predict_fall_and_alert()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=False)
