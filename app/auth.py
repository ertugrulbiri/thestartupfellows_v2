from urllib import response

import jwt
from flask import current_app, make_response
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.errors import error_response
from app.model.user_models import User

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user


@basic_auth.error_handler
def basic_auth_error(status):
    return error_response(status, 401)


@token_auth.verify_token
def verify_token(token):
    return User.check_token(token) if token else None


@token_auth.error_handler
def token_auth_error(status=401):
    return error_response(status, 401)


def generate_jwt_token(user_id, expire_time):
    return jwt.encode({'user_id': user_id, "exp": expire_time}, current_app.config['OPERATOR_SECRET_KEY'], 'HS256')


def generate_refresh_token(user_id, expire_time):
    return jwt.encode({'refresh_id': user_id, "exp": expire_time}, current_app.config['OPERATOR_SECRET_KEY'], 'HS256')


### OPERATOR ###
def generate_partner_jwt_token(user_id, expire_time):
    return jwt.encode({'user_id': user_id, "exp": expire_time}, current_app.config['OPERATOR_SECRET_KEY'], 'HS256')


def generate_operator_refresh_token(user_id, expire_time):
    return jwt.encode({'refresh_id': user_id, "exp": expire_time}, current_app.config['OPERATOR_SECRET_KEY'], 'HS256')


def logout():
    response = make_response("Auth Error", 401)
    response.set_cookie('user-session', '', expires=0)
    return response

