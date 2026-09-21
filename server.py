import os
import subprocess
from flask import Flask, request, render_template_string, send_file

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>YouTube Converter</title>
</head>
<body>
    <h1>YouTube Converter</h1>
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

    # Sørg for at downloads-mappen finnes
    os.makedirs("downloads", exist_ok=True)

    # yt-dlp basekommando
    base = ["yt-dlp", "-o", "downloads/%(title)s.%(ext)s"]

    # Render støtter ikke ffmpeg → bruk fallback
    if type_ == "video":
        cmd = base + ["-f", "best", "--no-mtime", url]
    else:
        cmd = base + ["-f", "bestaudio", "--no-mtime", url]

    # Kjør yt-dlp
    subprocess.run(cmd)

    # Finn siste fil
    files = os.listdir("downloads")
    latest = max([f"downloads/" + f for f in files], key=os.path.getctime)

    return send_file(latest, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
