from flask import Blueprint

availability_bp = Blueprint("availability", __name__, url_prefix="/availability")


from .healthcheck import healthcheck
from .add_availability import add_availability
from .view_slots import list_slots
from .get_availability import get_availability_via_user_id  