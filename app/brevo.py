import os
import requests


def send_email(to_email, subject, html_content):

    api_key = os.getenv("BREVO_API_KEY")

    response = requests.post(
        "https://api.brevo.com/v3/smtp/email",
        headers={
            "accept": "application/json",
            "api-key": api_key,
            "content-type": "application/json"
        },
        json={
            "sender": {
                "name": "ZeroNexus",
                "email": "zeronexus.admin001@gmail.com"
            },
            "to": [
                {
                    "email": to_email
                }
            ],
            "subject": subject,
            "htmlContent": html_content
        },
        timeout=15
    )

    print("BREVO STATUS:", response.status_code)
    print(response.text)

    response.raise_for_status()

    return True