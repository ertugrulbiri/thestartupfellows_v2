from flask import jsonify

from app import db
from app.errors import bad_request
from app.model.user_models import StartupCompany


def get_current_client_controller(user):
    if user.type == "StartUp":
        user= user.get_start_up()
    elif user.type == "AdminUser":
        user= user.admin_user()
    elif user.type == "PartnerUser":
        user = user.partner_user()

    if user:
        return jsonify(user.to_dict())
    return bad_request("User Type Not Found")


def get_all_startups_controller(user):
    startups = db.session.query(StartupCompany).all()
    startup_list = [startup.to_dict() for startup in startups]

    return startup_list


def add_partner_controller(user, request):
    data = request.get_json()

    return None