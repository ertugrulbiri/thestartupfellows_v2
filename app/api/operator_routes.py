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


@bp.route('/getAllStartUps', methods=['GET'])
@token_required_v2
def get_all_startups(user):
    """
    Send otp for registration of Client to given phone number
    :return: message in Response
    """
    return operator_controller.get_all_startups_controller(user)

@bp.route('/getPartners', methods=['GET'])
@token_required_v2
def get_all_partners(user):
    """
    Send otp for registration of Client to given phone number
    :return: message in Response
    """
    return operator_controller.get_all_partners_controller(user)

@bp.route('/getAllUsers', methods=['GET'])
@token_required_v2
def get_all_users(user):
    """
    Send otp for registration of Client to given phone number
    :return: message in Response
    """
    return operator_controller.get_all_users_controller(user)


@bp.route('/addPartner', methods=['POST'])
@token_required_v2
def add_partner(user):
    """
    Send otp for registration of Client to given phone number
    :return: message in Response
    """
    return operator_controller.add_partner_controller(user, request)


@bp.route('/addAdmin', methods=['POST'])
@token_required_v2
def add_admin(user):
    """
    Send otp for registration of Client to given phone number
    :return: message in Response
    """
    return operator_controller.add_partner_controller(user, request)


@bp.route('/addCoFounder', methods=['POST'])
@token_required_v2
def add_co_founder(user):
    """
    Send otp for registration of Client to given phone number
    :return: message in Response
    """
    return operator_controller.add_partner_controller(user, request)


@bp.route('/setMeeting', methods=['POST'])
@token_required_v2
def set_meeting(user):
    """
    Send otp for registration of Client to given phone number
    :return: message in Response
    """
    return operator_controller.set_meeting_controller(user, request)


@bp.route('/getAllMeetingsOfClient', methods=['GET'])
@token_required_v2
def get_meetings_of_client(user):
    """
    Send otp for registration of Client to given phone number
    :return: message in Response
    """
    return operator_controller.get_all_meetings_of_users(user)


@bp.route('/addMeetingNote', methods=['GET'])
@token_required_v2
def add_meeting_note(user):
    """
    Send otp for registration of Client to given phone number
    :return: message in Response
    """
    return operator_controller.add_note_to_meeting(user, request)

@bp.route('/partners/addMeetingSlot', methods=['GET'])
@token_required_v2
def add_meeting_slot(user):
    """
    Send otp for registration of Client to given phone number
    :return: message in Response
    """
    return operator_controller.add_meeting_slot_controller(user, request)