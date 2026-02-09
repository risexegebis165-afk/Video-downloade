from flask import Flask, render_template, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch', methods=['POST'])
def fetch_video():
    url = request.form.get('url')
    if not url:
        return jsonify({"error": "Link missing"}), 400

    ydl_opts = {'quiet': True, 'noplaylist': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = []
            for f in info.get('formats', []):
                if f.get('url'):
                    formats.append({
                        'url': f['url'],
                        'ext': f.get('ext', 'mp4'),
                        'quality': f.get('height', 'audio'),
                        'type': 'Video' if f.get('vcodec') != 'none' else 'Audio'
                    })
            return jsonify({
                'title': info.get('title', 'Video'),
                'thumbnail': info.get('thumbnail', ''),
                'video_preview': info.get('url', ''),
                'formats': formats
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
