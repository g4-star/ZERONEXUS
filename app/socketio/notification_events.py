from flask_login import current_user
from flask_socketio import emit

from app.extensions import socketio
from app.services.notification_service import NotificationService


@socketio.on("load_notifications")
def load_notifications():

    if not current_user.is_authenticated:
        return

    notifications = NotificationService.get_notifications(
        current_user
    )

    emit(
        "notifications_loaded",
        {
            "notifications": [
                {
                    "id": n.id,
                    "title": n.title,
                    "message": n.message,
                    "type": n.type,
                    "link": n.link,
                    "is_read": n.is_read,
                    "created_at": n.created_at.strftime("%Y-%m-%d %H:%M")
                }
                for n in notifications
            ]
        }
    )