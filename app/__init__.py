from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)


db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = "login" # Tells the login message if login required
login.login_message = "You must login to make this change"
login.login_message_category = "danger"

CORS(app)

from app.blueprint.api import api
app.register_blueprint(api)

from app.blueprint.user import user
app.register_blueprint(user)

from app.blueprint.auth import auth
app.register_blueprint(auth)

from . import models, routes