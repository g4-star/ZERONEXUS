from app.api.v1 import api


def register_api(app):

    app.register_blueprint(api)