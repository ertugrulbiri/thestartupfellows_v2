
import jwt
from flask import make_response, jsonify, current_app, abort

import functools
from flask import request, make_response, jsonify, abort


from app import redis_client, db
from app.errors import bad_request


# import validators

def validate_startup_onboard_info(f):
    @functools.wraps(f)
    def decorated_function(user, req):
        startup_register_data = req.get_json()
        if not isinstance(startup_register_data, dict):
            return bad_request("BAD FORMAT")
        for op_data in operator_list:
            for field_name in operator_log_messages.OPERATOR_REQUIRED_FIELDS:
                if field_name not in op_data:
                    return bad_request(operator_log_messages.MISSING_FIELD_ERROR_MESSAGE % field_name)
                operator_utils.validate_operator_data_types(field_name, op_data)

        return f(user, operator_list, request)

    return decorated_function
