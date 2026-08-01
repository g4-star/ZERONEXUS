from flask import (
    render_template
)

from flask_login import (
    login_required,
    current_user
)

from . import user_bp


# =====================================================
# MEMBER PROFILE
# =====================================================

@user_bp.route("/profile")
@login_required
def profile():

    return render_template(
        "user/profile.html",
        user=current_user
    )