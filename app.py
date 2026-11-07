import os
from flask import Flask, jsonify

app = Flask(__name__)

APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
SERVICE_NAME = os.getenv("SERVICE_NAME", "Python-Service")

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": SERVICE_NAME
    }), 200

@app.route("/version", methods=["GET"])
def version_check():
    return jsonify({
        "version": APP_VERSION,
        "service": SERVICE_NAME
    }), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)