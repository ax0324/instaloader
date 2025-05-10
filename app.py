from flask import Flask, request, jsonify
import instaloader

app = Flask(__name__)

# Initialize Instaloader
L = instaloader.Instaloader()

@app.route('/download', methods=['GET'])
def download_content():
    url = request.args.get('url')
    if not url:
        return jsonify({"success": False, "message": "No URL provided"}), 400

    try:
        # Handle different types of URLs (profile, post, etc.)
        if 'instagram.com' in url:
            # Attempt to load Instagram post or profile based on URL
            post = instaloader.Post.from_shortcode(L.context, url.split("/")[-2])
            
            # For simplicity, we return images only (you can expand it to include videos)
            content = [{"url": edge.display_url} for edge in post.get_sidecar_nodes()]
            
            return jsonify({"success": True, "content": content})

        else:
            return jsonify({"success": False, "message": "Invalid URL"}), 400

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
