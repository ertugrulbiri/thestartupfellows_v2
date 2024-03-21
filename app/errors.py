import traceback

from flask import jsonify, current_app
from flask import request
from flask_limiter import RequestLimit
from werkzeug.http import HTTP_STATUS_CODES


def error_response(status_code, error_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    if error_code:
        payload['error_code'] = error_code
    response = jsonify(payload)
    response.status_code = status_code
    return response


def bad_request(message, error_code=400):
    return error_response(400, error_code, message)


def bad_request_auto_loan(n, message):
    return error_response(n, message)


def default_error_responder(request_limit: RequestLimit):
    resp = jsonify(message="Kullanım Aşıldı", request_ip=request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
                   request_endpoint=request_limit.request_args[1])
    resp.status_code = 429
    # slack.send_slack_error_message(str(resp.json))
    return resp
