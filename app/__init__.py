from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from .config import Config
from .auth import auth
from .models import UserModel
from decouple import config
import json

login_manger = LoginManager()
login_manger.login_view = 'auth.login'


@login_manger.user_loader
def load_user(username):
    return UserModel.query(username)


def create_app():
    app = Flask(__name__)

    credentials_dict = {
        "type": "",
        "project_id": "",
        "private_key": "",
        "client_email": "",
        "token_uri": ""
    }

    for key in credentials_dict:
        if key == "private_key":
            credentials_dict[key] = config(key).replace('\\n', '\n')
        else:
            credentials_dict[key] = config(key)

    with open('google_credentials.json', 'w') as file:
        json.dump(credentials_dict, file, indent=2)

    bootstrap = Bootstrap(app)

    app.config.from_object(Config)

    login_manger.init_app(app)

    app.register_blueprint(auth)

    return app
