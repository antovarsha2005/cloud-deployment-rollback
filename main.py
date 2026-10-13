import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>Cloud Deployment & Rollback Demo</h1>
    <h2>Application Version: 1.0</h2>
    <p>Status: Healthy</p>
    <p>Running on Google Cloud Run</p>
    """

@app.route("/health")
def health():
    return "Simulated health-check failure", 500

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080))
    )
