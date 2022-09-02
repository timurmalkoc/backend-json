from . import user
from flask import jsonify, request
from app.models import User

# @user.route('/login', methods=['POST'])
# def user_login():
#     if not request.is_json:
#         return jsonify({'error':'Your request content-type must be application/json'}), 400

#     data = request.json

#     for field in {'username','password'}:
#         if field not in data:
#             return jsonify({'error':f"'{field}' must be in resquest body"}),400

#     user = User.query.filter_by(username=data["username"]).first()
#     if user and user.check_password(data["password"]):
#         return jsonify({"success":"Authenticated"}),200
#     else:
#         return jsonify({"error":"INVALID_USERNAME OR PASSWORD"}),400


@user.route('/<user_id>')
def user_getById(user_id):
    user = User.query.get_or_404(user_id)
    if user:
        return user.to_dict()


@user.route('/signup', methods=['POST'])
def user_signup():
    if not request.is_json:
        return jsonify({'error':'Your request content-type must be application/json'}), 400

    data = request.json

    for field in {'username','email','password'}:
        if field not in data:
            return jsonify({'error':f"'{field}' must be in resquest body"}),400

    exist_user = User.query.filter(User.email == data.get("email") or User.username == data.get("username")).all()

    if exist_user:
        return jsonify({'error':"Username is token"}),400


    User(email=data['email'], username=data['username'], password=data['password'])
    return jsonify({"success":"New user is created successfully !"}),201