from . import api
from flask import jsonify, request
from app.models import Post
from flask_httpauth import HTTPTokenAuth
from app.models import User
from datetime import datetime

token_auth = HTTPTokenAuth()

@token_auth.verify_token
def verify(token):
    user = User.query.filter_by(token=token).first()
    now = datetime.utcnow()
    if user is not None and user.token_expiration > now:
        return user

@api.route('/')
def index():
    names = ['Brian', 'Tatyana', 'Nate', 'Sam']
    return jsonify(names)


@api.route('/posts')
@token_auth.login_required
def get_posts():
    posts = Post.query.filter(Post.user_id==token_auth.current_user().id).all()
    return jsonify([p.to_dict() for p in posts])


@api.route('/posts/<post_id>')
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_dict())


@api.route('/posts', methods=["POST"])
@token_auth.login_required
def create_post():
    if not request.is_json:
        return jsonify({'error': 'Your request content-type must be application/json'}), 400

    data = request.json

    for field in ['title', 'body']:
        if field not in data:

            return jsonify({'error': f"'{field}' must be in request body"}), 400
    
    print("tooooken ",token_auth.current_user().id)
    title = data.get('title')
    body = data.get('body')
    # user_id = token_auth.current_user().id

    new_post = Post(title=title, body=body, user_id=token_auth.current_user().id)
    return jsonify(new_post.to_dict()), 201