from flask import request

from app.api import bp
from app.controller import startup_controller, operator_controller
from app.decorator.auth_decorator import token_required_v2

@bp.route('/getCurrentClient', methods=['GET'])
@token_required_v2
def get_current_client(user):
    """
    Send otp for registration of Client to given phone number
    :return: message in Response
    """
    return operator_controller.get_current_client_controller(user)