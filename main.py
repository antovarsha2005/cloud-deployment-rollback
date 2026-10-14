```python
import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cloud Deployment & Rollback Demo</title>
    </head>
    <body>
        <h1>Cloud Deployment & Rollback Demo</h1>
        <h2>Application Version: 1.0</h2>
        <p>Status: Healthy</p>
        <p>Running on Google Cloud Run</p>
        <p>Version 1 is the stable production version.</p>
    </body>
    </html>
    """

@app.route("/health")
def health():
    return "Healthy", 200

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080))
    )
```
