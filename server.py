import os
import subprocess
from flask import Flask, request, send_file, render_template_string, abort

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

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url")
    if not url:
        return abort(400, "Ingen URL oppgitt")

    os.makedirs("downloads", exist_ok=True)
    output_path = os.path.join("downloads", "%(title)s.%(ext)s")

    try:
        subprocess.run(
            ["yt-dlp", "-f", "best", "-o", output_path, url],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print("Feil ved yt-dlp:", e)
        return abort(500, "Feil ved nedlasting")

    files = sorted(
        os.listdir("downloads"),
        key=lambda f: os.path.getmtime(os.path.join("downloads", f))
    )
    if not files:
        return abort(500, "Ingen fil funnet")

    latest_file = os.path.join("downloads", files[-1])
    return send_file(latest_file, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
