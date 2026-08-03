from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func

from app.models.user import User
from app.models.team import Team
from app.models.project import Project
from app.models.meeting import Meeting
from app.models.announcement import Announcement
from app.models.notification import Notification
from app.models.presence import UserPresence
from app.models.chat import ChatMessage


dashboard_api = Blueprint(
    "dashboard_api",
    __name__,
    url_prefix="/api/dashboard"
)


# =====================================================
# DASHBOARD STATS
# =====================================================

@dashboard_api.route("/stats")
@login_required
def stats():

    team = current_user.team

    if not team:
        return jsonify({
            "success": False,
            "message": "No team assigned."
        }), 403

    return jsonify({

        "success": True,

        "stats": {

            "members": len(team.users),

            "projects": Project.query.filter_by(
                team_id=team.id
            ).count(),

            "meetings": Meeting.query.filter_by(
                team_id=team.id
            ).count(),

            "announcements": Announcement.query.filter_by(
                team_id=team.id
            ).count(),

            "channels": len(team.channels),

            "messages": ChatMessage.query.join(
                ChatMessage.channel
            ).filter_by(
                team_id=team.id
            ).count()
        }
    })


# =====================================================
# ONLINE MEMBERS
# =====================================================

@dashboard_api.route("/online")
@login_required
def online():

    if not current_user.team:
        return jsonify([])

    online = UserPresence.query.filter_by(
        online=True
    ).all()

    members = []

    for presence in online:

        if presence.user.team_id == current_user.team_id:

            members.append({

                "id": presence.user.id,

                "username": presence.user.username,

                "profile_image": presence.user.profile_image,

                "role": presence.user.role,

                "last_seen": presence.last_seen.strftime(
                    "%Y-%m-%d %H:%M"
                )

            })

    return jsonify({

        "success": True,

        "online": members

    })


# =====================================================
# UNREAD NOTIFICATIONS
# =====================================================

@dashboard_api.route("/notifications")
@login_required
def notifications():

    notifications = Notification.query.filter_by(

        user_id=current_user.id,

        is_read=False

    ).order_by(

        Notification.created_at.desc()

    ).all()

    return jsonify({

        "success": True,

        "notifications": [

            {

                "id": n.id,

                "title": n.title,

                "message": n.message,

                "type": n.type,

                "link": n.link,

                "created_at": n.created_at.strftime(
                    "%Y-%m-%d %H:%M"
                )

            }

            for n in notifications

        ]

    })


# =====================================================
# RECENT CHAT
# =====================================================

@dashboard_api.route("/recent")
@login_required
def recent():

    messages = ChatMessage.query.join(

        ChatMessage.channel

    ).filter_by(

        team_id=current_user.team_id

    ).order_by(

        ChatMessage.created_at.desc()

    ).limit(10).all()

    return jsonify({

        "success": True,

        "messages": [

            {

                "id": m.id,

                "sender": m.sender.username,

                "content": m.content,

                "created_at": m.created_at.strftime(
                    "%H:%M"
                )

            }

            for m in messages

        ]

    })


# =====================================================
# ACTIVITY FEED
# =====================================================

@dashboard_api.route("/activity")
@login_required
def activity():

    activity = []

    meetings = Meeting.query.filter_by(
        team_id=current_user.team_id
    ).all()

    for meeting in meetings:

        activity.append({

            "type": "meeting",

            "title": meeting.title,

            "time": meeting.created_at.strftime(
                "%Y-%m-%d %H:%M"
            )

        })

    announcements = Announcement.query.filter_by(
        team_id=current_user.team_id
    ).all()

    for announcement in announcements:

        activity.append({

            "type": "announcement",

            "title": announcement.title,

            "time": announcement.created_at.strftime(
                "%Y-%m-%d %H:%M"
            )

        })

    activity.sort(
        key=lambda x: x["time"],
        reverse=True
    )

    return jsonify({

        "success": True,

        "activity": activity[:20]

    })