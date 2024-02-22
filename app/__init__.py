from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)
jwt = JWTManager(app)


login_manager = LoginManager(app)
login_manager.login_view = 'auth.sign_in'
login_manager.login_message = 'Please log in, before continuing'
login_manager.login_message_category = 'warning'

from app.blueprints.API import bp as api
app.register_blueprint(api)

from app import models