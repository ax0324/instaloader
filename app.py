from flask import Flask, request, jsonify
import instaloader
import os

app = Flask(__name__)

# 从环境变量中获取 Instagram 账号和密码
IG_USERNAME = os.getenv("IG_USERNAME")
IG_PASSWORD = os.getenv("IG_PASSWORD")

@app.route('/api/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'Missing URL'}), 400

    try:
        loader = instaloader.Instaloader()

        # 登录 Instagram 账号
        if IG_USERNAME and IG_PASSWORD:
            loader.login(IG_USERNAME, IG_PASSWORD)
        else:
            return jsonify({'error': 'Instagram credentials not set'}), 500

        # 提取短码
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
