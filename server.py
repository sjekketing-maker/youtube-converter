from flask import Flask, request, render_template_string, send_file
import subprocess
import os

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
            "--user-agent", "Mozilla/5.0 (Linux; Android 10)"
        ]

     

       if type_ == "video":
           cmd = base + ["-f", "best", "--no-mtime", url]
       else:
           cmd = base + ["-f", "bestaudio", "--no-mtime", url]

        # Kjør yt-dlp
        subprocess.run(cmd)

        # Finn siste nedlastede fil
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        latest = max(files, key=os.path.getctime)

        # Send filen til brukeren
        return send_file(latest, as_attachment=True)

    return render_template_string(HTML, message=None)

app.run(host="0.0.0.0", port=5000)
