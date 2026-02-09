from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/fetch', methods=['POST'])
def fetch_video():
    url = request.form.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {'quiet': True, 'noplaylist': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            formats = []
            
            for f in info.get('formats', []):
                # ভিডিও + অডিও একসাথে আছে এমন ফরম্যাট ফিল্টার
                if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                    formats.append({
                        'id': f.get('format_id'),
                        'ext': 'mp4',
                        'quality': f.get('resolution') or f.get('format_note'),
                        'url': f.get('url'),
                        'type': 'Video'
                    })
                # শুধুমাত্র অডিও (MP3/M4A)
                elif f.get('vcodec') == 'none' and f.get('acodec') != 'none':
                    formats.append({
                        'id': f.get('format_id'),
                        'ext': 'mp3',
                        'quality': f.get('abr', 128),
                        'url': f.get('url'),
                        'type': 'Audio'
                    })

            return jsonify({
                'title': info.get('title'),
                'thumbnail': info.get('thumbnail'),
                'video_preview': info.get('url'), # Direct stream URL
                'formats': formats
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
          
