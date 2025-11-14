from flask import Blueprint

preferences_bp = Blueprint("prefs", __name__, url_prefix="/prefs")


from .healthcheck import healthcheck
from .create_preferences import create_user_preferences