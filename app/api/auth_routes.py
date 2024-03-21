import os

from flask import request, make_response

from app import auth
from app.api import bp
from app.auth import generate_jwt_token
from app.decorator.auth_decorator import token_required_v2
from app.errors import bad_request
from app.service import user_service


@bp.route('/logout', methods=['POST'])
@token_required_v2
def logout():
    """
    Logout deletes user token
    ALL user sessions in other devices are logged out
    """
    return auth.logout()


@bp.route('/login')
def request_login_otp():
    """
    it goes deeper...>- _->
    """
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return bad_request("Auth Failed", 401)

    if "@" in auth.username:
        keyword = "email"
    else:
        keyword = "telephone"
    # Accepts both email and phone number as login username
    user = user_service.login_service(auth.username, auth.password, keyword)
    token = generate_jwt_token(user.id, 100000)
    result = {'id': user.id, 'token': token}
    if result:
        print("giriş yapıldı")
        response = make_response("success")
        # response.headers['Access-Control-Allow-Credentials'] = "true"

        if os.environ.get('APP_MODE') == 'prod' or os.environ.get('APP_MODE') == 'prep':
            response.set_cookie('user-session', result['token'], httponly=True, samesite="None", secure=True)
        else:
            response.set_cookie('user-session', result['token'], httponly=True, samesite="None", secure=False)
        return response

    return "Invalid Credentials"