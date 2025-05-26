
from flask import Flask, request, send_file, render_template_string
import yt_dlp
import os
import tempfile

app = Flask(__name__)

html = '''
<!doctype html>
<title>YouTube Video Downloader</title>
<h1>YouTube Video Downloader</h1>
<form method=post>
  Enter YouTube URL:<br>
  <input type=text name=url size=50 required>
  <input type=submit value=Download>
</form>
{% if error %}
<p style="color:red;">{{ error }}</p>
{% endif %}
'''

@app.route('/', methods=['GET', 'POST'])
def download_video():
    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        if url:
            try:
                with tempfile.TemporaryDirectory() as tmpdir:
                    ydl_opts = {
                        'format': 'best',
                        'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
                        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        filename = ydl.prepare_filename(info)

                    return send_file(filename, as_attachment=True)
            except Exception as e:
                return render_template_string(html, error=f"Error: {str(e)}")
        else:
            return render_template_string(html, error="Please enter a valid URL.")

    return render_template_string(html)
