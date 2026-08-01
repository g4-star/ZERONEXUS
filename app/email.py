from flask_mail import Message
from flask import current_app
from app.extensions import mail


def send_member_welcome(member):
    """
    Sends a professional welcome email with a private profile edit link.
    """

    site_url = current_app.config.get(
        'SITE_URL',
        'https://zeronexus.vercel.app'
    )

    # Private edit link for this member
    edit_link = f"{site_url}/member/edit/{member.profile_token}"

    msg = Message(
        subject="🎉 Welcome to ZeroNexus",
        recipients=[member.email]
    )

    msg.html = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family:Arial,sans-serif;background:#f4f6f9;padding:30px;">

        <div style="
            max-width:700px;
            margin:auto;
            background:white;
            border-radius:10px;
            overflow:hidden;
            box-shadow:0 5px 20px rgba(0,0,0,.15);
        ">

            <div style="
                background:#0d6efd;
                color:white;
                text-align:center;
                padding:35px;
            ">
                <h1>Welcome to ZeroNexus</h1>
                <p>Cybersecurity Collaboration Platform</p>
            </div>

            <div style="padding:35px;">

                <h2>Hello {member.full_name},</h2>

                <p>
                    Congratulations! You have successfully been added to
                    <strong>ZeroNexus</strong>.
                </p>

                <p>
                    ZeroNexus is a collaborative cybersecurity platform where
                    students showcase projects, join teams, build portfolios,
                    and work together on innovative solutions.
                </p>

                <h3>Your Details</h3>

                <table style="width:100%;border-collapse:collapse;">

                    <tr>
                        <td><strong>Name</strong></td>
                        <td>{member.full_name}</td>
                    </tr>

                    <tr>
                        <td><strong>Email</strong></td>
                        <td>{member.email}</td>
                    </tr>

                    <tr>
                        <td><strong>Role</strong></td>
                        <td>{member.role}</td>
                    </tr>

                    <tr>
                        <td><strong>Team</strong></td>
                        <td>{member.team.name if member.team else 'Not Assigned'}</td>
                    </tr>

                </table>

                <br>

                <p>
                    Complete your ZeroNexus profile by adding your photo,
                    LinkedIn, GitHub, portfolio, skills, and contact details.
                </p>

                <a href="{edit_link}"
                   style="
                        display:inline-block;
                        padding:14px 30px;
                        background:#0dcaf0;
                        color:#000;
                        text-decoration:none;
                        border-radius:6px;
                        font-weight:bold;
                   ">
                    Update My Profile
                </a>

                <p style="margin-top:20px;font-size:13px;color:#666;">
                    This private link allows you to update your own profile.
                    Please do not share it with others.
                </p>

                <hr>

                <p>
                    We look forward to your contributions to the ZeroNexus
                    community.
                </p>

                <p>
                    Regards,<br>
                    <strong>ZeroNexus Administration</strong>
                </p>

            </div>

            <div style="
                background:#f8f9fa;
                padding:20px;
                text-align:center;
                color:#666;
                font-size:13px;
            ">
                © ZeroNexus • Built by Moringa School Cybersecurity Students
            </div>

        </div>

    </body>
    </html>
    """

    mail.send(msg)
    
def send_member_invitation(user, password):
    
    site_url = current_app.config.get(
        "SITE_URL",
        "https://zeronexus.vercel.app"
    )

    activation_link = (
        f"{site_url}/activate/{user.activation_token}"
    )


    msg = Message(
        subject="🎉 Welcome to ZeroNexus Team",
        recipients=[user.email]
    )


    msg.html = f"""

    <!DOCTYPE html>

    <html>

    <body style="
        font-family:Arial;
        background:#f4f6f9;
        padding:30px;
    ">


    <div style="
        max-width:650px;
        margin:auto;
        background:white;
        padding:35px;
        border-radius:12px;
    ">


    <h1 style="color:#0d6efd;">
        Welcome to ZeroNexus 🎉
    </h1>


    <p>
        You have been invited to join a ZeroNexus team.
    </p>


    <h3>Your Account Details</h3>


    <p>
        <b>Username:</b>
        {user.username}
    </p>


    <p>
        <b>Temporary Password:</b>
        {password}
    </p>


    <p>
        For security reasons, you must change your
        password before accessing your team dashboard.
    </p>



    <a href="{activation_link}"

    style="
    display:inline-block;
    background:#0dcaf0;
    color:#000;
    padding:14px 25px;
    text-decoration:none;
    border-radius:6px;
    font-weight:bold;
    ">

    Activate My Account

    </a>



    <br><br>


    <p>
    After activation you will be redirected to your
    assigned ZeroNexus team dashboard.
    </p>



    <hr>


    <strong>
    ZeroNexus Administration
    </strong>


    </div>


    </body>

    </html>

    """


    mail.send(msg)

def send_contact_confirmation(contact_message):
    """
    Sends an automatic confirmation email after someone
    submits the ZeroNexus contact form.
    """

    msg = Message(
        subject="✅ Thank You for Contacting ZeroNexus",
        recipients=[contact_message.email]
    )

    msg.html = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family:Arial,sans-serif;background:#f4f6f9;padding:30px;">

        <div style="
            max-width:700px;
            margin:auto;
            background:#ffffff;
            border-radius:12px;
            overflow:hidden;
            box-shadow:0 6px 20px rgba(0,0,0,.15);
        ">

            <div style="
                background:#0dcaf0;
                color:#000;
                text-align:center;
                padding:35px;
            ">

                <h1>Thank You!</h1>

                <p>Your message has been received.</p>

            </div>

            <div style="padding:35px;">

                <h2>Hello {contact_message.full_name},</h2>

                <p>
                    Thank you for contacting
                    <strong>ZeroNexus</strong>.
                </p>

                <p>
                    Your message has been successfully received by our team.
                    We appreciate you taking the time to reach out.
                </p>

                <h3>Your Submission</h3>

                <table style="width:100%;border-collapse:collapse;">

                    <tr>
                        <td style="padding:8px;"><strong>Name</strong></td>
                        <td style="padding:8px;">{contact_message.full_name}</td>
                    </tr>

                    <tr>
                        <td style="padding:8px;"><strong>Email</strong></td>
                        <td style="padding:8px;">{contact_message.email}</td>
                    </tr>

                    <tr>
                        <td style="padding:8px;"><strong>Subject</strong></td>
                        <td style="padding:8px;">{contact_message.subject}</td>
                    </tr>

                </table>

                <br>

                <div style="
                    background:#f8f9fa;
                    border-left:5px solid #0dcaf0;
                    padding:20px;
                ">

                    {contact_message.message}

                </div>

                <br>

                <p>
                    Our team will review your message and respond as soon as
                    possible.
                </p>

                <p>
                    Thank you for supporting the ZeroNexus community.
                </p>

                <br>

                <p>
                    Regards,<br>
                    <strong>ZeroNexus Team</strong><br>
                    <span style="color:#666;">
                        Forge Skills. Build Solutions. Secure the Future.
                    </span>
                </p>

            </div>

            <div style="
                background:#f8f9fa;
                padding:18px;
                text-align:center;
                color:#666;
                font-size:13px;
            ">

                © ZeroNexus • Thank you for connecting with us.

            </div>

        </div>

    </body>
    </html>
    """

    mail.send(msg)