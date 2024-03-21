# -*- coding: UTF-8 -*-
import json
import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler
import redis
import app.db
# from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
# from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_compress import Compress
from flask_cors import CORS
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address

from config.config import Config
# from rq import Queue


db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
compress = Compress()
# csrf = CSRFProtect()
redis_client = redis.from_url(url=os.environ.get("REDIS_URL"), decode_responses=True)
# limiter = Limiter(key_func=get_remote_address, storage_uri=os.environ.get("REDIS_URL"), on_breach=default_error_responder)
# connection = redis.StrictRedis(host='redis', port=6379, db=0)
# task_queue = Queue('my-tasks', connection=redis_client)

def create_app(config_class=Config):
    # rest of connection code using the connection string `uri`
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.config.from_object(config_class)

    # limiter.init_app(app)
    db.init_app(app)
    MIGRATION_DIR = os.path.join('config', 'database_migrations_psql')
    migrate.init_app(app, db, directory=MIGRATION_DIR, compare_type=True)
    mail.init_app(app)
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    compress.init_app(app)

    if os.environ.get('APP_MODE') == 'prod':
        print('Production Mode On')
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='TeklifimGelsin Emergency Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)
    # slack_handler = SlackNotificationHandler(url=os.environ.get("slack_error_bot_url"))
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # slack_handler.setFormatter(formatter)
    # slack_handler.setLevel(logging.ERROR)
    # app.logger.addHandler(slack_handler)
    # app.logger.setLevel(logging.ERROR)


    if app.config['LOG_TO_STDOUT'] == 1:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)
    else:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/teklifimgelsinapp.log',
                                           maxBytes=10240, backupCount=10)

        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('App Started')

    return app

from app.model import user_models