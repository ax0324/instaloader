from flask import Flask, request, jsonify
import instaloader

app = Flask(__name__)

@app.route('/api/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'Missing URL'}), 400

    try:
        loader = instaloader.Instaloader()
        shortcode = url.rstrip("/").split("/")[-1]
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        return jsonify({
            'author': post.owner_username,
            'caption': post.caption,
            'url': url
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return 'Instagram Downloader API is running.'