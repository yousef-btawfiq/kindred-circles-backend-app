from flask import Blueprint

topics_bp = Blueprint("topics", __name__, url_prefix="/topics")


from .healthcheck import healthcheck
from .topics import list_topics