from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .users import User
from .preferences import Preferences
from .availability import Availability

