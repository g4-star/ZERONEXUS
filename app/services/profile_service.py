from app.extensions import db
from app.models.user import User


class ProfileService:

    @staticmethod
    def get_profile(user):

        return {

            "completion": ProfileService.profile_completion(user),

            "level": ProfileService.calculate_level(user),

            "xp": ProfileService.calculate_xp(user),

            "next_level": ProfileService.next_level(user)

        }

    @staticmethod
    def update_profile(user, data):

        fields = [

            "username",
            "bio",
            "phone",
            "location",
            "job_title",
            "company",
            "skills",
            "github",
            "linkedin",
            "portfolio",
            "tryhackme",
            "hackthebox",
            "ctftime"

        ]

        for field in fields:

            if field in data:

                setattr(user, field, data[field])

        db.session.commit()

        return user

    @staticmethod
    def update_profile_image(user, image_url):

        user.profile_image = image_url

        db.session.commit()

        return user

    @staticmethod
    def profile_completion(user):

        fields = [

            "profile_image",
            "bio",
            "phone",
            "location",
            "job_title",
            "company",
            "skills",
            "github",
            "linkedin",
            "portfolio",
            "tryhackme",
            "hackthebox",
            "ctftime"

        ]

        completed = 0

        for field in fields:

            if hasattr(user, field):

                value = getattr(user, field)

                if value:

                    completed += 1

        return round(

            (completed / len(fields)) * 100

        )

    @staticmethod
    def calculate_xp(user):

        xp = 0

        xp += ProfileService.profile_completion(user) * 10

        if hasattr(user, "projects"):

            xp += len(user.projects) * 100

        if hasattr(user, "team") and user.team:

            xp += 200

        if hasattr(user, "skills") and user.skills:

            xp += len(

                user.skills.split(",")

            ) * 25

        return xp

    @staticmethod
    def calculate_level(user):

        xp = ProfileService.calculate_xp(user)

        return (xp // 1000) + 1

    @staticmethod
    def next_level(user):

        level = ProfileService.calculate_level(user)

        current = ProfileService.calculate_xp(user)

        required = level * 1000

        return {

            "level": level,

            "current_xp": current,

            "required_xp": required,

            "remaining": max(

                required - current,

                0

            )

        }

    @staticmethod
    def leaderboard():

        users = User.query.all()

        users = sorted(

            users,

            key=lambda u:

            ProfileService.calculate_xp(u),

            reverse=True

        )

        return users