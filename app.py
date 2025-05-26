
from flask import Flask, request, send_file, render_template_string
import yt_dlp
import os
import tempfile

app = Flask(__name__)

html = '''
<!doctype html>
<title>YouTube Video Downloader</title>
<h1>YouTube Video Downloader</h1>
<form method=post enctype=multipart/form-data>
  Enter YouTube URL:<br>
  <input type=text name=url size=50 required><br><br>
  Optional: Upload cookies.txt file:<br>
  <input type=file name=cookiefile accept=".txt"><br><br>
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
        cookie_file_path = None

        if 'cookiefile' in request.files:
            cookie_file = request.files['cookiefile']
            if cookie_file and cookie_file.filename.endswith('.txt'):
                temp_cookie = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
                cookie_file.save(temp_cookie.name)
                cookie_file_path = temp_cookie.name

        if url:
            try:
                with tempfile.TemporaryDirectory() as tmpdir:
                    ydl_opts = {
                        'format': 'best',
                        'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
                        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                    }
                    if cookie_file_path:
                        ydl_opts['cookiefile'] = cookie_file_path

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        filename = ydl.prepare_filename(info)

                    return send_file(filename, as_attachment=True)
            except Exception as e:
                return render_template_string(html, error=f"Error: {str(e)}")
            finally:
                if cookie_file_path and os.path.exists(cookie_file_path):
                    os.remove(cookie_file_path)
        else:
            return render_template_string(html, error="Please enter a valid URL.")

    return render_template_string(html)
