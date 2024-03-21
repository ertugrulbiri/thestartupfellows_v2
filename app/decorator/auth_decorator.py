
import jwt
from flask import make_response, jsonify, current_app, abort


import functools
from flask import request, make_response, jsonify, abort

from app.model.user_models import User


def token_required_v2(f):
    @functools.wraps(f)
    def decorator(*args, **kwargs):
        token = None
        # ensure the jwt-token is passed with the headers
        token = request.cookies.get('user-session')
        if not token:  # throw error if no token provided
            return make_response(jsonify({"message": "A valid token is missing!"}), 401)
        try:
            # decode the token to obtain user public_id
            data = jwt.decode(token, current_app.config['OPERATOR_SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.filter_by(id=data['user_id']).first()

            if not current_user:
                response = make_response("Auth Error", 401)
                response.set_cookie('user-session', '', expires=0)
                return response
        except Exception as e:
            print(e)
            response = make_response("Auth Error", 401)
            response.set_cookie('user-session', '', expires=0)
            return response
        # Return the user information attached to the token
        return f(current_user, *args, **kwargs)

    return decorator