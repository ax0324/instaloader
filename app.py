import os
from flask import Flask, request, jsonify
import instaloader
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = Flask(__name__)

# 从环境变量中读取 Instagram 用户名和密码
INSTAGRAM_USERNAME = os.getenv("ig07.snap")  # 从环境变量读取 Instagram 用户名
INSTAGRAM_PASSWORD = os.getenv("Ax9657@.")  # 从环境变量读取 Instagram 密码

@app.route('/api/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'Missing URL'}), 400

    try:
        # 使用 Instaloader 登录 Instagram
        loader = instaloader.Instaloader()
        loader.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)  # 登录 Instagram

        # 获取 post shortcode
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
