import os
import requests
from flask import Flask, request, send_file, abort
from io import BytesIO

app = Flask(__name__)
app.debug = True

RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.environ.get("RAPIDAPI_HOST")  # skal være: youtube-media-downloader.p.rapidapi.com

@app.route("/")
def index():
    return """
    <form method="POST" action="/download">
        <input name="url" placeholder="Lim inn YouTube-lenke" required>
        <select name="format">
            <option value="audio">MP3</option>
            <option value="video">MP4</option>
        </select>
        <button type="submit">Last ned</button>
    </form>
    """

@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url")
    fmt = request.form.get("format", "audio")  # audio = MP3, video = MP4

    if not url:
        return abort(400, "Ingen URL oppgitt")

    if not RAPIDAPI_KEY or not RAPIDAPI_HOST:
        return abort(500, "API-konfigurasjon mangler")

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    # Velg riktig endpoint basert på format
    if fmt == "audio":
        endpoint = f"https://{RAPIDAPI_HOST}/api/v1/audio"
        filename = "youtube.mp3"
    else:
        endpoint = f"https://{RAPIDAPI_HOST}/api/v1/video"
        filename = "youtube.mp4"

    try:
        print("Kaller RapidAPI-endpoint:", endpoint)
        resp = requests.get(
            endpoint,
            params={"url": url},
            headers=headers,
            timeout=60
        )
   
       print("RapidAPI status:", resp.status_code)
       print("API raw response:", resp.text)
    except Exception as e:
    import traceback
    print("API exception:", e)
    traceback.print_exc()
    return abort(500, "Feil ved API-kall")

    print("API raw response:", resp.text)

    if resp.status_code != 200:
        print("API response:", resp.status_code, resp.text)
        return abort(500, "API returnerte feil")

    data = resp.json()
    download_url = data.get("url") or data.get("link") or data.get("download_url")
    if not download_url:
        print("API data:", data)
        return abort(500, "Ingen nedlastingslenke fra API")

    file_resp = requests.get(download_url)
    if file_resp.status_code != 200:
        print("File response:", file_resp.status_code)
        return abort(500, "Kunne ikke hente filen fra nedlastingslenken")

    file_bytes = BytesIO(file_resp.content)

    return send_file(file_bytes, as_attachment=True, download_name=filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
