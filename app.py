from flask import Flask, request, render_template_string
import yt_dlp

app = Flask(__name__)

html = '''
<!doctype html>
<title>YouTube Video Metadata Viewer</title>
<h1>YouTube Video Metadata Viewer</h1>
<form method=post>
  Enter YouTube URL:<br>
  <input type=text name=url size=50 required><br><br>
  <input type=submit value="Fetch Info">
</form>
{% if error %}
<p style="color:red;">Error: {{ error }}</p>
{% endif %}
{% if info %}
<h2>Video Info:</h2>
<ul>
  <li><strong>Title:</strong> {{ info.title }}</li>
  <li><strong>Uploader:</strong> {{ info.uploader }}</li>
  <li><strong>Duration:</strong> {{ info.duration }} seconds</li>
  <li><strong>Views:</strong> {{ info.view_count }}</li>
  <li><strong>Upload Date:</strong> {{ info.upload_date }}</li>
</ul>
{% endif %}
'''

@app.route('/', methods=['GET', 'POST'])
def metadata_viewer():
    info = None
    error = None

    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        if url:
            try:
                ydl_opts = {
                    'quiet': True,
                    'simulate': True,
                    'forcejson': True,
                    'skip_download': True,
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    data = ydl.extract_info(url, download=False)
                    info = type('VideoInfo', (object,), data)
            except Exception as e:
                error = str(e)
        else:
            error = "Please enter a valid URL."

    return render_template_string(html, info=info, error=error)
