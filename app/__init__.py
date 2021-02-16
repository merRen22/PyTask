from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from .config import Config
from .auth import auth
from .models import UserModel
from firebase_admin import credentials, initialize_app
from decouple import config

login_manger = LoginManager()
login_manger.login_view = 'auth.login'


@login_manger.user_loader
def load_user(username):
    return UserModel.query(username)


def create_app():
    app = Flask(__name__)

    cred = credentials.Certificate(
        {
            'type': config('TYPE'),
            'private_key': config('PRIVATE_KEY').replace('\\n', '\n'),
            'client_email': config('CLIENT_EMAIL'),
            'token_uri': config('TOKEN_URI')
        }
    )

    initialize_app(
        name='py-task',
        credential=cred
    )

    bootstrap = Bootstrap(app)

    app.config.from_object(Config)

    login_manger.init_app(app)

    app.register_blueprint(auth)

    return app
