import os
import requests


BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"


def send_email(
    to_email,
    subject,
    html_content
):

    api_key = os.getenv("BREVO_API_KEY")

    if not api_key:
        raise Exception(
            "BREVO_API_KEY missing"
        )


    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json",
    }


    data = {

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
    }


    response = requests.post(
        BREVO_API_URL,
        headers=headers,
        json=data,
        timeout=30
    )


    print("=" * 60)
    print("BREVO STATUS:", response.status_code)
    print(response.text)
    print("=" * 60)


    response.raise_for_status()


    return response.json()