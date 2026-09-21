import os
import requests
from flask import Flask, request, render_template_string, send_file, abort

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>YouTube Converter</title>
</head>
<body>
    <h1>YouTube Converter (API)</h1>
    <form method="POST" action="/download">
        <input type="text" name="url" placeholder="YouTube URL" required>
        <select name="type">
            <option value="video">Video (MP4)</option>
            <option value="audio">Audio (MP3)</option>
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

    # RapidAPI endpoint
    api_url = "https://youtube-video-download-info.p.rapidapi.com/dl"
    params = {"id": url.split("v=")[-1]}

    headers = {
        "x-rapidapi-key": os.environ.get("RAPIDAPI_KEY"),
        "x-rapidapi-host": "youtube-video-download-info.p.rapidapi.com"
    }

    r = requests.get(api_url, headers=headers, params=params)
    if r.status_code != 200:
        return abort(500, "API error")

    data = r.json()

    # Velg riktig format
    if type_ == "video":
        download_url = data["link"]["mp4"]
        filename = "video.mp4"
    else:
        download_url = data["link"]["mp3"]
        filename = "audio.mp3"

    # Last ned filen
    file_path = f"downloads/{filename}"
    os.makedirs("downloads", exist_ok=True)

    file_data = requests.get(download_url)
    with open(file_path, "wb") as f:
        f.write(file_data.content)

    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
