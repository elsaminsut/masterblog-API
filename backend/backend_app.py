import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL="/api/docs"
API_URL="/static/masterblog.json"

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes - cross origin resource sharing

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Masterblog API'
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post.", "author": "Alice", "date": datetime.date.fromisoformat("2026-03-24").isoformat()},
    {"id": 2, "title": "Second post", "content": "This is the second post.", "author": "Bob", "date": datetime.date.fromisoformat("2026-03-20").isoformat()},
]

def find_post_by_id(id):
    if isinstance(id, int):
        post = next((post for post in POSTS if post["id"] == id), None)
        return post
    return jsonify({"error": f"invalid type for post id: {id}"}), 400


@app.route('/api/posts', methods=['GET'])
def get_posts():
    sort = request.args.get("sort", "")
    direction_param = request.args.get("direction", "")
    direction_dict = {
        "asc": False,
        "desc": True
    }
    if sort:
        if sort not in ["title", "content", "author", "date"]:
            return jsonify({"error": "invalid sort parameter"}), 400
        if direction_param and direction_param not in ["asc", "desc"]:
            return jsonify({"error": "invalid direction parameter"}), 400
        direction = direction_dict.get(direction_param, False)
        sorted_posts = sorted(POSTS, key=lambda x: x[sort], reverse=direction)
        return jsonify(sorted_posts)
    if not sort and direction_param:
        return jsonify({"error": "empty sort parameter"}), 400

    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()
    required_fields = ["title", "content", "author"]
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"{field} field cannot be empty"}), 400
    new_post = {
        "id": len(POSTS) + 1,
        "title": data["title"],
        "content": data["content"],
        "author": data["author"],
        "date": data.get("date") if data.get("date") else datetime.date.today().isoformat()
    }
    POSTS.append(new_post)
    return jsonify(POSTS), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = find_post_by_id(post_id)
    if not post:
        return jsonify({"error": f"post with id {post_id} not found"}), 404
    POSTS.remove(post)
    return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.get_json()
    post = find_post_by_id(post_id)
    if not post:
        return jsonify({"error": f"post with id {post_id} not found"}), 404
    post["title"] = data.get("title") if data.get("title") else post["title"]
    post["content"] = data.get("content") if data.get("content") else post["content"]
    post["author"] = data.get("author") if data.get("author") else post["author"]
    post["date"] = data.get("date") if data.get("date") else post["date"]
    return jsonify(post), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    search_key = request.args.get("key", "")
    match = []
    for post in POSTS:
        for field in post.values():
            if search_key in str(field):
                match.append(post)
                break # prevents a post from being added twice
    return jsonify(match)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
