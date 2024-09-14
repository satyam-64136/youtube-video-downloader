from flask import Flask, render_template, request, send_file
from pytubefix import YouTube
from youtubesearchpython import VideosSearch
import os

app = Flask(__name__)

DOWNLOAD_DIR = os.path.join(os.getcwd(), 'downloads')
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    thumbnail_url = None
    error_message = None
    video_url = None
    video_title = None

    if request.method == 'GET':
        thumbnail_url = None
        video_url = None
        video_title = None
        error_message = None

    elif request.method == 'POST':
        video_url = request.form.get('video_url')
        action = request.form.get('action')

        if action == 'search':
            try:
                videosSearch = VideosSearch(video_url, limit=1)
                results = videosSearch.result()
                video_info = results['result'][0]
                video_url = video_info['link']
                thumbnail_url = video_info['thumbnails'][0]['url']
                video_title = video_info['title']
                print(f"Video Found: {video_title}")
            except Exception as e:
                error_message = f"Error searching for video: {str(e)}"
                print(error_message)

        elif action == 'download':
            video_url = request.form.get('video_url_hidden')

            if video_url is None or video_url == '':
                error_message = "No video URL provided for download."
                print(error_message)
            else:
                try:
                    print("Video URL for Download: ", video_url)
                    yt = YouTube(video_url)
                    video_stream = yt.streams.get_highest_resolution()
                    video_path = video_stream.download(output_path=DOWNLOAD_DIR)
                    print("Video Download Path: ", video_path)
                    return send_file(video_path, as_attachment=True, download_name=f"{yt.title}.mp4")
                except Exception as e:
                    error_message = f"Error downloading video: {str(e)}"
                    print(error_message)

    return render_template('index.html', video_url=video_url, thumbnail_url=thumbnail_url, video_title=video_title, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
