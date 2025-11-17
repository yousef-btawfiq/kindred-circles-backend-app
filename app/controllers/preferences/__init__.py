from flask import Blueprint

preferences_bp = Blueprint("prefs", __name__, url_prefix="/prefs")


from .healthcheck import healthcheck
from .create_preferences import create_user_preferences
from .get_preferences import get_preferences_via_user_id