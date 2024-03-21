from flask import request

from app.api import bp
from app.controller import startup_controller
from app.decorator.auth_decorator import token_required_v2


@bp.route('/startups/register', methods=['POST'])
def register_startup():
    """
    Send otp for registration of Client to given phone number
    :return: message in Response
    """
    return startup_controller.register_startup_controller(request)


@bp.route('/startups/getInfo', methods=['POST'])
@token_required_v2
def get_startup_info(user):
    """
    Send otp for registration of Client to given phone number
    :return: message in Response
    """
    return startup_controller.get_info_of_start_up_controller(user, request)


@bp.route('/startups/applyProgram', methods=['POST'])
@token_required_v2
def apply_startup_program():
    """
    Send otp for registration of Client to given phone number
    :return: message in Response
    """
    return startup_controller.apply_program_controller(request)


@bp.route('/startups/getAllMentors', methods=['POST'])
@token_required_v2
def get_all_mentors():
    """
    Send otp for registration of Client to given phone number
    :return: message in Response
    """
    return startup_controller.register_startup_controller(request)

@bp.route('/startups/setMeeting', methods=['POST'])
@token_required_v2
def set_meeting():
    """
    Send otp for registration of Client to given phone number
    :return: message in Response
    """
    return startup_controller.register_startup_controller(request)


@bp.route('/startups/sendMonthlyReport', methods=['POST'])
@token_required_v2
def send_monthly_report(user):
    """
    Send otp for registration of Client to given phone number
    :return: message in Response
    """
    return startup_controller.register_startup_controller(user, request)


@bp.route('/startups/changeGeneralInfo', methods=['POST'])
@token_required_v2
def change_general_info():
    """
    Send otp for registration of Client to given phone number
    :return: message in Response
    """
    return startup_controller.register_startup_controller(request)

@bp.route('/startups/getUserInfo', methods=['POST'])
@token_required_v2
def get_user_info():
    """
    Send otp for registration of Client to given phone number
    :return: message in Response
    """
    return startup_controller.register_startup_controller(request)

# @bp.route('/startups/sendReport', methods=['POST'])
# @token_required_v2
# def send_monthly_report(user):
#     """
#     Send otp for registration of Client to given phone number
#     :return: message in Response
#     """
#     return startup_controller.send_monthly_report(user, request)
