from flask_socketio import SocketIO

socketio = SocketIO(
    cors_allowed_origins="*"
)

from .events import register_socket_events


def init_socketio(app):

    socketio.init_app(app)

    register_socket_events(socketio)

    return socketio