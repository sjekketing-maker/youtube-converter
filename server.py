import os
import requests
from flask import Flask, request, send_file, abort
from io import BytesIO

app = Flask(__name__)

RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.environ.get("RAPIDAPI_HOST")

@app.route("/")
def index():
    return """
    <form method="POST" action="/download">
        <input name="url" placeholder="Lim inn YouTube-lenke" required>
        <button type="submit">Last ned MP3</button>
    </form>
    """

@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url")
    if not url:
        return abort(400, "Ingen URL oppgitt")

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    try:
        resp = requests.get(
            f"https://{RAPIDAPI_HOST}/get-url",
            params={"url": url},
            headers=headers,
            timeout=60
        )
    except Exception as e:
        print("API error:", e)
        return abort(500, "Feil ved API-kall")

    if resp.status_code != 200:
        print("API response:", resp.status_code, resp.text)
        return abort(500, "API returnerte feil")

    data = resp.json()
    download_url = data.get("link")
    if not download_url:
        return abort(500, "Ingen nedlastingslenke fra API")

    file_resp = requests.get(download_url)
    file_bytes = BytesIO(file_resp.content)

    return send_file(file_bytes, as_attachment=True, download_name="youtube.mp3")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
