import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '../.env'), override=True)


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'what_do_you_think'
    POSTGRESQL_USER = os.environ.get("POSTGRESQL_USER")
    POSTGRESQL_PASSWORD = os.environ.get("POSTGRESQL_PASSWORD")
    POSTGRESQL_DB_NAME = os.environ.get("POSTGRESQL_DB_NAME")
    ENC_KEY = os.environ.get("ENC_KEY")
    uri = os.environ.get("DATABASE_URL")  # or other relevant config var
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = uri
    JSON_SORT_KEYS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = 'LOG_TO_FILE'
    # COMPRESS_REGISTER = False
    COMPRESS_MIN_SIZE = 0
    COMPRESS_ALGORITHM = ['gzip']
    # SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = os.environ.get("MAIL_PORT")
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_FROM = os.environ.get("MAIL_FROM")
    OPERATOR_SECRET_KEY = os.environ.get("OPERATOR_SECRET_KEY")
    MAIL_DEBUG = 0
    #CORS_SUPPORTS_CREDENTIALS = True
    ADMINS = ['biriertugrulhakan@gmail.com']
    #SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    # Email Confirmation, not sure about what value it should has
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")

