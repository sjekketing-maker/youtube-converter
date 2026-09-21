import requests
from flask import Flask, request, render_template_string, redirect, abort

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>YouTube Downloader</title>
</head>
<body>
    <h1>YouTube Downloader</h1>
    <form method="POST" action="/download">
        <input type="text" name="url" placeholder="Lim inn YouTube-lenke" required>
        <button type="submit">Last ned</button>
    </form>
</body>
</html>
"""

def extract_video_id(url):
    if "v=" in url:
        return url.split("v=")[-1].split("&")[0]
    return url.rsplit("/", 1)[-1]

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url")
    if not url:
        return abort(400, "Ingen URL oppgitt")

    video_id = extract_video_id(url)

    # Hent manifest fra YouTube
    manifest_url = f"https://www.youtube.com/get_video_info?video_id={video_id}"
    r = requests.get(manifest_url)

    if r.status_code != 200:
        return abort(500, "Kunne ikke hente manifest")

    data = r.text

    # Finn første videostrøm
    if "url=" not in data:
        return abort(500, "Ingen videostrøm funnet")

    stream_url = data.split("url=")[1].split("&")[0]
    stream_url = requests.utils.unquote(stream_url)

    return redirect(stream_url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
