import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '1111111'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'silicon_squad.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mail configuration
    MAIL_SERVER = "smtp.qq.com"  # QQ email is used in the project
    MAIL_PORT = "465"
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = True
    MAIL_USERNAME = "1193058357@qq.com"
    MAIL_PASSWORD = "eednzbwjcibyjiac"
    MAIL_DEFAULT_SENDER = "1193058357@qq.com"
    LANGUAGE = "ENG"
