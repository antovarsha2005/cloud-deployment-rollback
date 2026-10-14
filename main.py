import os
from flask import Flask

app = Flask(__name__)

# True = unhealthy candidate for the rollback demonstration
# False = healthy Version 2 for the successful deployment demonstration
SIMULATE_FAILURE = False


@app.route("/")
def home():
    if SIMULATE_FAILURE:
        status_text = "UNHEALTHY CANDIDATE"
        status_color = "#b91c1c"
        detail_text = (
            "This is a deliberate failure test. "
            "Production should remain on Version 1."
        )
    else:
        status_text = "Healthy"
        status_color = "#15803d"
        detail_text = (
            "Health check passed. "
            "Version 2 is ready for production."
        )

    page = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Cloud Deployment Demo - Version 2</title>
        <style>
            * { box-sizing: border-box; }

            body {
                margin: 0;
                padding: 30px 16px;
                min-height: 100vh;
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #dbeafe, #eef2ff);
                color: #172554;
                display: flex;
                justify-content: center;
                align-items: center;
            }

            .container {
                max-width: 780px;
                width: 100%;
                background: white;
                border-radius: 20px;
                overflow: hidden;
                box-shadow: 0 18px 50px rgba(30, 64, 175, 0.15);
            }

            .header {
                padding: 32px;
                color: white;
                background: linear-gradient(120deg, #1d4ed8, #4338ca);
            }

            .label {
                font-size: 12px;
                font-weight: bold;
                letter-spacing: 2px;
                text-transform: uppercase;
            }

            h1 {
                font-size: 30px;
                line-height: 1.2;
                margin: 14px 0;
            }

            .subtitle {
                line-height: 1.6;
                color: #e0e7ff;
            }

            .content {
                padding: 30px 32px;
            }

            .version {
                font-size: 36px;
                font-weight: bold;
                color: #1d4ed8;
                margin-bottom: 20px;
            }

            .status {
                padding: 15px;
                border-radius: 12px;
                background: #f8fafc;
                border: 1px solid #cbd5e1;
                font-weight: bold;
                margin-bottom: 22px;
            }

            .cards {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 12px;
            }

            .card {
                padding: 16px;
                border: 1px solid #e2e8f0;
                background: #f8fafc;
                border-radius: 12px;
            }

            .card h3 {
                font-size: 15px;
                margin: 8px 0;
            }

            .card p {
                color: #64748b;
                font-size: 12px;
                line-height: 1.5;
            }

            footer {
                padding: 18px;
                text-align: center;
                border-top: 1px solid #e2e8f0;
                color: #64748b;
                font-size: 12px;
            }

            @media (max-width: 600px) {
                .cards { grid-template-columns: 1fr; }
                .header, .content { padding: 22px; }
            }
        </style>
    </head>
    <body>
        <main class="container">
            <header class="header">
                <div class="label">Cloud Project Dashboard</div>
                <h1>Cloud Deployment &amp; Rollback Demo</h1>
                <p class="subtitle">
                    Version 2 introduces a redesigned deployment dashboard.
                </p>
            </header>

            <section class="content">
                <div class="version">Application Version: 2.0</div>

                <div class="status" style="color: STATUS_COLOR;">
                    Status: STATUS_TEXT
                </div>

                <p>DETAIL_TEXT</p>

                <div class="cards">
                    <div class="card">
                        <div>🚀</div>
                        <h3>Deployment</h3>
                        <p>Candidate revision created by Cloud Build.</p>
                    </div>

                    <div class="card">
                        <div>💚</div>
                        <h3>Health Check</h3>
                        <p>Test the application before production promotion.</p>
                    </div>

                    <div class="card">
                        <div>🛡️</div>
                        <h3>Rollback</h3>
                        <p>Keep production on the stable revision if testing fails.</p>
                    </div>
                </div>
            </section>

            <footer>
                Google Cloud Run · Deployment and Rollback Demo · Version 2.0
            </footer>
        </main>
    </body>
    </html>
    """

    return (
        page.replace("STATUS_COLOR", status_color)
            .replace("STATUS_TEXT", status_text)
            .replace("DETAIL_TEXT", detail_text)
    )


@app.route("/health")
def health():
    if SIMULATE_FAILURE:
        return "Simulated health-check failure", 500

    return "Healthy", 200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080))
    )
