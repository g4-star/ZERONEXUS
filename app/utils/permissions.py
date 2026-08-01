from flask_login import current_user


def is_admin():

    return (
        current_user.is_authenticated
        and current_user.role == "admin"
    )



def is_team_lead():

    return (
        current_user.is_authenticated
        and current_user.role == "team_lead"
    )



def is_member():

    return (
        current_user.is_authenticated
        and current_user.role == "member"
    )



def is_viewer():

    return (
        current_user.is_authenticated
        and current_user.role == "viewer"
    )
