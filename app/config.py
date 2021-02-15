import secrets


class Config:
    SECRET_KEY = secrets.token_hex(20)
    ENV = 'development'
