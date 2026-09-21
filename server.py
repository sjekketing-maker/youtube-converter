from flask import Flask, request, render_template_string
import subprocess

app = Flask(__name__)

HTML = """
<h2>YouTube Converter</h2>

<form method="POST">
    <label>Velg type:</label><br>
    <input type="radio" name="type" value="video" checked> Video<br>
    <input type="radio" name="type" value="audio"> Audio<br><br>

    <label>Lim inn YouTube-URL:</label><br>
    <input type="text" name="url" style="width:400px;"><br><br>

    <button type="submit">Konverter</button>
</form>

{% if message %}
<p><strong>{{ message }}</strong></p>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        type_ = request.form.get("type")

        base = [
            "yt-dlp",
            "--cookies-from-browser", "none",
            "--user-agent", "Mozilla/5.0 (Linux; Android 10)"
        ]

        if type_ == "video":
            cmd = base + ["-f", "bv*+ba/b", url]
        else:
            cmd = base + ["-x", "--audio-format", "m4a", url]

        subprocess.run(cmd)
        return render_template_string(HTML, message="Konvertering ferdig!")

    return render_template_string(HTML, message=None)

app.run(host="0.0.0.0", port=5000)
