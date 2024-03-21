from app import db
from app.model.user_models import StartupCompany


def get_startup_company_by_id(startup_company_id):
    return db.session.query(StartupCompany).filter(StartupCompany.id == startup_company_id).first()

