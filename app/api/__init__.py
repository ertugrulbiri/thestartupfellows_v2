from flask import Blueprint

bp = Blueprint('api', __name__)
from app.api import \
    (auth_routes,
     operator_routes,
     investor_routes,
     start_up_routes)


