import os
import requests
from flask import Flask, request, render_template_string, send_file, abort

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>YouTube Converter (API)</title>
</head>
<body>
    <h1>YouTube Converter (Cloud API Hub)</h1>
    <form method="POST" action="/download">
        <input type="text" name="url" placeholder="YouTube URL" required>
        <select name="type">
            <option value="video">Video</option>
            <option value="audio">Audio</option>
        </select>
        <button type="submit">Download</button>
    </form>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url")
    type_ = request.form.get("type")

    if not url:
        return abort(400, "No URL provided")

    # Ekstraher video-ID fra URL (alt etter v=)
    if "v=" in url:
        video_id = url.split("v=")[-1].split("&")[0]
    else:
        # Kort-URL eller annen variant
        video_id = url.rsplit("/", 1)[-1]

    api_url = "https://cloud-api-hub-youtube-downloader.p.rapidapi.com/download"
    params = {
        "id": video_id,
        "filter": "audioandvideo",
        "quality": "lowest"
    }

    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-host": "cloud-api-hub-youtube-downloader.p.rapidapi.com",
        "x-rapidapi-key": os.environ.get("RAPIDAPI_KEY")
    }

    if not headers["x-rapidapi-key"]:
        return abort(500, "RAPIDAPI_KEY is not set")

    r = requests.get(api_url, headers=headers, params=params)
    if r.status_code != 200:
        return abort(500, "API error")

    data = r.json()

    # API-et returnerer direkte URL i feltet "url"
    if "url" not in data:
        return abort(500, "No download URL in API response")

    download_url = data["url"]

    # Velg filnavn basert på type
    if type_ == "video":
        filename = "download.mp4"
    else:
        filename = "download.mp3"

    os.makedirs("downloads", exist_ok=True)
    file_path = os.path.join("downloads", filename)

    file_data = requests.get(download_url)
    if file_data.status_code != 200:
        return abort(500, "Failed to download file from API URL")

    with open(file_path, "wb") as f:
        f.write(file_data.content)

    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
