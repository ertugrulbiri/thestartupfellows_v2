from flask import jsonify
from sqlalchemy import or_

from app import db
from app.decorator import startup_decorator
from app.errors import bad_request
from app.model.user_models import StartupCompany, User, StartupUser
from app.service import startup_service
from static import constants


def register_startup_controller(request):
    data = request.get_json()
    user_data = data.get("user_data")
    startup_data = data.get("startup_data")

    startup_company = StartupCompany()
    startup_company.from_dict(startup_data)

    for field in constants.START_UP_USER_MUST_FIELDS:
        if field not in user_data:
            print(f"{field} not found in user_data")
            return bad_request(f"Missing required field: {field}")

    for field in user_data:
        if not user_data[field]:
            print(f"{field} cannot be empty")
            return bad_request(f"Value for field {field} cannot be empty")

    # for field in constants.START_UP_COMPANY_MUST_FIELDS:
    #     if field not in startup_data:
    #         return bad_request(f"Missing required field: {field}")

    if db.session.query(StartupUser).filter(or_(
                StartupUser.email == user_data.get("email"),
                StartupUser.telephone == user_data.get("telephone")
            )).first():

        return bad_request("User already registered")

    user = StartupUser()
    user.set_password(user_data.get("password"))
    user.type = "StartUp"
    user.from_dict(user_data)

    startup_company.user = user

    db.session.add(startup_company)
    db.session.commit()

    user.startup_company_id = startup_company.id
    db.session.add(user)
    db.session.commit()

    return 'Success'


def get_info_of_start_up_controller(user, request):
    user = user.get_start_up()
    data = request.get_json()
    if 'startup_id' not in data:
        return bad_request("Missing required field: startup_id")

    start_up = startup_service.get_info_of_start_up_service(data['startup_id'])
    if start_up:
        return jsonify(start_up.to_dict())
    return bad_request("Start Up Not Found")


