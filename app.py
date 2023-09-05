from flask import Flask, render_template, request
from pytube import YouTube
from youtubesearchpython import VideosSearch
import os
from pathlib import Path

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    thumbnail_url = None
    error_message = None

    if request.method == 'POST':
        video_url = request.form.get('video_url')
        action = request.form.get('action')

        if action == 'download':
            try:
                yt = YouTube(video_url)
                video_stream = yt.streams.get_highest_resolution()
                download_path = str(Path.home() / "Downloads")
                os.makedirs(download_path, exist_ok=True)
                video_stream.download(output_path=download_path)
            except Exception as e:
                error_message = str(e)
        elif action == 'search':
            try:
                videosSearch = VideosSearch(video_url, limit=1)
                results = videosSearch.result()
                video_info = results['result'][0]
                thumbnail_url = video_info['thumbnails'][0]['url']
            except Exception as e:
                error_message = str(e)

    return render_template('index.html', thumbnail_url=thumbnail_url, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
