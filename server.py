import os
import requests
from flask import Flask, request, send_file, abort
from io import BytesIO

app = Flask(__name__)

API_BASE_URL = os.environ.get("YOUTUBE_API_URL")      # f.eks. https://api.example.com
API_KEY      = os.environ.get("YOUTUBE_API_KEY")      # din nøkkel

@app.route("/")
def index():
    return """
    <form method="POST" action="/download">
        <input name="url" placeholder="Lim inn YouTube-lenke" required>
        <select name="format">
            <option value="mp3">MP3</option>
            <option value="mp4">MP4</option>
        </select>
        <button type="submit">Last ned</button>
    </form>
    """

@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url")
    fmt = request.form.get("format", "mp3")

    if not url:
        return abort(400, "Ingen URL oppgitt")

    if not API_BASE_URL or not API_KEY:
        return abort(500, "API-konfigurasjon mangler")

    # Eksempel på API-kall – tilpass til leverandøren du velger
    try:
        resp = requests.get(
            f"{API_BASE_URL}/convert",
            params={"url": url, "format": fmt},
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=60,
        )
    except Exception as e:
        print("API error:", e)
        return abort(500, "Feil ved API-kall")

    if resp.status_code != 200:
        print("API response:", resp.status_code, resp.text)
        return abort(500, "API returnerte feil")

    # Anta at API-et returnerer selve filen (binary)
    file_bytes = BytesIO(resp.content)
    filename = f"download.{fmt}"

    return send_file(
        file_bytes,
        as_attachment=True,
        download_name=filename
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
