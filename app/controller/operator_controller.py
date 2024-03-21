from flask import jsonify

from app.errors import bad_request


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