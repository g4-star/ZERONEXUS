from flask_mail import Message
from app.extensions import mail


def send_member_welcome(member):
    """
    Sends a professional welcome email to a newly added member.
    """

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
                        <td>{member.team.name if member.team else "Not Assigned"}</td>
                    </tr>

                </table>

                <br>

                <a href="https://zeronexus.vercel.app"
                   style="
                        display:inline-block;
                        padding:14px 30px;
                        background:#0d6efd;
                        color:white;
                        text-decoration:none;
                        border-radius:6px;
                   ">
                    Visit ZeroNexus
                </a>

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