from flask import Blueprint

api = Blueprint(
    "api",
    __name__,
    url_prefix="/api/v1"
)

from .dashboard import *
from .profile import *
from .projects import *
from .announcements import *
from .meetings import *
from .notifications import *
from .chat import *
from .ai import *