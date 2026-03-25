from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes - cross origin resource sharing

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)

@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()

    if not data.get("title") and not data.get("content"):
        return jsonify({"error": "body fields cannot be empty"}), 400
    
    if not data.get("title"):
        return jsonify({"error": "title field cannot be empty"}), 400

    if not data.get("content"):
        return jsonify({"error": "content field cannot be empty"}), 400


    new_post = {
        "id": len(POSTS) + 1,
        "title": data["title"],
        "content": data["content"]
    }

    POSTS.append(new_post)
    return jsonify(POSTS), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
