from datetime import datetime, timedelta
from app import db, login
import os
import base64
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_password(kwargs['password'])
        db.session.add(self)
        db.session.commit()
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "date_created": self.date_created
        }
    
    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')  # genereate random token
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.commit()
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)
        db.session.commit()

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Post(db.Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key in {'title','body'}:
                setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "date_created": self.date_created,
            "user_id": self.user_id
        }        