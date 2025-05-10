from flask import Flask, request, jsonify
import instaloader
import os

app = Flask(__name__)

@app.route('/api/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "Missing URL"}), 400

    try:
        shortcode = url.strip("/").split("/")[-1]
        loader = instaloader.Instaloader(dirname_pattern="downloads", save_metadata=False)
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        loader.download_post(post, target=shortcode)
        return jsonify({"message": f"Downloaded {shortcode}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return '''
    <h1>Instagram Downloader</h1>
    <form method="post" action="/api/download" onsubmit="submitForm(event)">
      <input type="text" id="url" placeholder="Enter Instagram Post URL" required>
      <button type="submit">Download</button>
    </form>
    <pre id="result"></pre>
    <script>
    async function submitForm(event) {
        event.preventDefault();
        const url = document.getElementById("url").value;
        const res = await fetch("/api/download", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ url })
        });
        const data = await res.json();
        document.getElementById("result").innerText = JSON.stringify(data, null, 2);
    }
    </script>
    '''