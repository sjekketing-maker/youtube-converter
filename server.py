from flask import Flask, request, render_template_string, redirect, abort
from pytube import YouTube

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

    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        return redirect(stream.url)
    except Exception as e:
        print("Feil:", e)
        return abort(500, "Feil ved nedlasting")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
