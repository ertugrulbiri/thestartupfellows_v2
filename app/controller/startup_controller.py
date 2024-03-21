import datetime

from dateutil.relativedelta import relativedelta
from flask import jsonify
from sqlalchemy import or_

from app import db
from app.decorator import startup_decorator
from app.errors import bad_request
from app.model.user_models import StartupCompany, User, StartupUser, MonthlyReport, KPI
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
    # user = user.get_start_up()
    data = request.get_json()
    if 'startup_id' not in data:
        return bad_request("Missing required field: startup_id")

    start_up = startup_service.get_info_of_start_up_service(data['startup_id'])
    if start_up:
        return jsonify(start_up.to_dict())
    return bad_request("Start Up Not Found")


def apply_program_controller(request):
    return None


def send_monthly_controller(user, request):
    user = user.get_start_up()
    if not user:
        return bad_request("User is not a Start Up")
    kpi_list = request.get_json()
    report = MonthlyReport.query.filter_by(startup_company_id=user.startup_company_id).filter(
        MonthlyReport.created_at >= datetime.date.today().replace(day=1)).first()

    if report:
        db.session.delete(report)

    # if not report:
    #     report = MonthlyReport()
    report = MonthlyReport()
    report.startup_company_id = user.startup_company_id

    db.session.add(report)
    db.session.commit()
    kpi_obj_list = []
    for item in kpi_list:
        kpi = KPI()
        kpi.from_dict(item)
        kpi.monthly_report_id = report.id
        kpi_obj_list.append(kpi)
    db.session.bulk_save_objects(kpi_obj_list)
    db.session.commit()

    return 'Report Sent'


def get_start_up_reports_by_start_up_id_controller(user, request):
    data = request.get_json()
    if "startup_id" not in data:
        return bad_request("Missing startup_id field")
    reports = MonthlyReport.query.filter_by(startup_company_id=data["startup_id"]).all()
    return jsonify([report.to_dict() for report in reports])


def get_startup_report_by_report_id_controller(user, request):
    data = request.get_json()
    if 'report_id' not in data:
        return bad_request("Missing report_id field")

    report = MonthlyReport.query.filter_by(id=data['report_id']).first()
    if not report:
        return bad_request("Report Not Found")
    return jsonify(report.to_dict())


def compare_two_reports_of_start_up_controller(user, request):
    data = request.get_json()

    if 'startup_id' not in data:
        return bad_request("Missing startup_id field")
    if not startup_service.get_startup_by_id_service(data['startup_id']):
        return bad_request("Start up not found")
    if "ranges" not in data:
        start_date = datetime.datetime.now().replace(day=1)
        end_date = start_date - datetime.timedelta(days=1)
        end_date = end_date.replace(day=1)
    else:
        ranges = data.get("ranges")
        start_date = datetime.datetime.fromtimestamp(ranges[0]).replace(day=1)
        end_date = datetime.datetime.fromtimestamp(ranges[1]).replace(day=1)

    # I need to get Report for same month with start_date only same month not day or else
    report1 = MonthlyReport.query.filter(
        MonthlyReport.startup_company_id == data['startup_id'],
        MonthlyReport.created_at >= start_date.replace(day=1),
        MonthlyReport.created_at < start_date.replace(day=1) + relativedelta(months=1)
    ).first()

    report2 = MonthlyReport.query.filter(
        MonthlyReport.startup_company_id == data['startup_id'],
        MonthlyReport.created_at >= end_date.replace(day=1),
        MonthlyReport.created_at < end_date.replace(day=1) + relativedelta(months=1)
    ).first()

    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")
    return jsonify({
        start_date: report1.to_dict() if report1 else None,
        end_date: report2.to_dict() if report2 else None
    })
