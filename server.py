import os
import subprocess
from flask import Flask, request, send_file, abort

app = Flask(__name__)

@app.route("/")
def index():
    return """
    <form method="POST" action="/download">
        <input name="url" placeholder="Lim inn YouTube-lenke" required>
        <button type="submit">Last ned</button>
    </form>
    """

@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url")
    if not url:
        return abort(400, "Ingen URL oppgitt")

    os.makedirs("/tmp/downloads", exist_ok=True)
    output_path = "/tmp/downloads/%(title)s.%(ext)s"

    try:
        subprocess.run(
            ["yt-dlp", "--no-playlist", "--no-warnings", "-o", output_path, url],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print("yt-dlp error:", e)
        return abort(500, "Feil ved nedlasting")

    files = sorted(os.listdir("/tmp/downloads"), key=lambda f: os.path.getmtime(os.path.join("/tmp/downloads", f)))
    latest_file = os.path.join("/tmp/downloads", files[-1])
    return send_file(latest_file, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
