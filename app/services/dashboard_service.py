from sqlalchemy import func

from app.extensions import db
from app.models.user import User
from app.models.project import Project
from app.models.team import Team
from app.models.announcement import Announcement

# Import Meeting only if your project has it
try:
    from app.models.meeting import Meeting
except ImportError:
    Meeting = None


class DashboardService:

    @staticmethod
    def get_dashboard(user):

        stats = DashboardService.get_statistics(user)

        return {

            "stats": stats,

            "projects": DashboardService.latest_projects(user),

            "announcements": DashboardService.latest_announcements(),

            "meetings": DashboardService.upcoming_meetings(),

            "completion": DashboardService.profile_completion(user)

        }

    @staticmethod
    def get_statistics(user):

        data = {

            "projects": 0,

            "teams": 0,

            "announcements": 0,

            "meetings": 0

        }

        if hasattr(Project, "owner_id"):

            data["projects"] = Project.query.filter_by(
                owner_id=user.id
            ).count()

        elif hasattr(Project, "user_id"):

            data["projects"] = Project.query.filter_by(
                user_id=user.id
            ).count()

        if hasattr(Team, "owner_id"):

            data["teams"] = Team.query.filter_by(
                owner_id=user.id
            ).count()

        elif hasattr(user, "team") and user.team:

            data["teams"] = 1

        data["announcements"] = Announcement.query.count()

        if Meeting:

            data["meetings"] = Meeting.query.count()

        return data

    @staticmethod
    def latest_projects(user):

        query = Project.query

        if hasattr(Project, "owner_id"):

            query = query.filter_by(owner_id=user.id)

        elif hasattr(Project, "user_id"):

            query = query.filter_by(user_id=user.id)

        if hasattr(Project, "created_at"):

            query = query.order_by(Project.created_at.desc())

        return query.limit(5).all()

    @staticmethod
    def latest_announcements():

        query = Announcement.query

        if hasattr(Announcement, "created_at"):

            query = query.order_by(
                Announcement.created_at.desc()
            )

        return query.limit(5).all()

    @staticmethod
    def upcoming_meetings():

        if not Meeting:

            return []

        query = Meeting.query

        if hasattr(Meeting, "meeting_date"):

            query = query.order_by(Meeting.meeting_date.asc())

        elif hasattr(Meeting, "date"):

            query = query.order_by(Meeting.date.asc())

        return query.limit(5).all()

    @staticmethod
    def profile_completion(user):

        fields = [

            "profile_image",

            "bio",

            "phone",

            "location",

            "skills",

            "github",

            "linkedin",

            "portfolio",

            "job_title",

            "company"

        ]

        completed = 0

        for field in fields:

            if hasattr(user, field):

                value = getattr(user, field)

                if value:

                    completed += 1

        return round((completed / len(fields)) * 100)