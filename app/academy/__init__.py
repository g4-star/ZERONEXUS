from flask import Blueprint


academy = Blueprint(
    "academy",
    __name__,
    url_prefix="/academy"
)


from . import routes