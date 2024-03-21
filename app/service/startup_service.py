from app.db import startup_db


def get_info_of_start_up_service(startup_company_id):
    return startup_db.get_startup_company_by_id(startup_company_id)