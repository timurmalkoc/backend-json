from . import auth
from app.models import User
from flask_httpauth import HTTPBasicAuth
from flask import jsonify

basic_auth = HTTPBasicAuth()


@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user is not None and user.check_password(password):
        return user

@auth.route('/token')
@basic_auth.login_required
def get_token():
    user = basic_auth.current_user()
    token = user.get_token()
    print({'token': token, 'token_expiration': user.token_expiration})
    return jsonify({'token': token, 'token_expiration': user.token_expiration}) 