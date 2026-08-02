from app.extensions import db
from app.models.project import Project


class ProjectService:

    @staticmethod
    def all_projects():

        return (

            Project.query

            .order_by(Project.created_at.desc())

            .all()

        )

    @staticmethod
    def latest_projects(limit=5):

        query = Project.query

        if hasattr(Project, "created_at"):

            query = query.order_by(

                Project.created_at.desc()

            )

        return query.limit(limit).all()

    @staticmethod
    def user_projects(user):

        if hasattr(Project, "owner_id"):

            return (

                Project.query

                .filter_by(owner_id=user.id)

                .all()

            )

        elif hasattr(Project, "user_id"):

            return (

                Project.query

                .filter_by(user_id=user.id)

                .all()

            )

        return []

    @staticmethod
    def get_project(project_id):

        return Project.query.get_or_404(project_id)

    @staticmethod
    def create_project(data):

        project = Project(**data)

        db.session.add(project)

        db.session.commit()

        return project

    @staticmethod
    def update_project(project, data):

        for key, value in data.items():

            if hasattr(project, key):

                setattr(project, key, value)

        db.session.commit()

        return project

    @staticmethod
    def delete_project(project):

        db.session.delete(project)

        db.session.commit()

    @staticmethod
    def completion(project):

        completed = 0

        total = 5

        checks = [

            "title",

            "description",

            "image",

            "github_url",

            "live_url"

        ]

        for field in checks:

            if hasattr(project, field):

                value = getattr(project, field)

                if value:

                    completed += 1

        return round((completed / total) * 100)

    @staticmethod
    def statistics():

        return {

            "total": Project.query.count(),

            "featured":

                Project.query.filter_by(

                    featured=True

                ).count()

                if hasattr(Project, "featured")

                else 0

        }