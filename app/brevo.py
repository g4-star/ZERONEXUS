import os
import requests

BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"


def send_email(
    to_email: str,
    subject: str,
    html_content: str,
):
    """
    Send an email using the Brevo Transactional Email API.

    Args:
        to_email (str): Recipient email address.
        subject (str): Email subject.
        html_content (str): HTML body.

    Returns:
        dict: Brevo API response.

    Raises:
        Exception: If configuration is missing or the API request fails.
    """

    api_key = os.getenv("BREVO_API_KEY")

    if not api_key:
        raise RuntimeError(
            "BREVO_API_KEY environment variable is missing."
        )

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": api_key,
    }

    payload = {
        "sender": {
            "name": "ZeroNexus",
            "email": "zeronexus.admin001@gmail.com",
        },
        "to": [
            {
                "email": to_email
            }
        ],
        "subject": subject,
        "htmlContent": html_content,
    }

    try:
        response = requests.post(
            BREVO_API_URL,
            headers=headers,
            json=payload,
            timeout=30,
        )

        print("=" * 70)
        print("BREVO EMAIL")
        print("Recipient :", to_email)
        print("Subject   :", subject)
        print("Status    :", response.status_code)
        print("Response  :", response.text)
        print("=" * 70)

        response.raise_for_status()

        return response.json()

    except requests.exceptions.Timeout:
        print("=" * 70)
        print("❌ BREVO ERROR")
        print("Request timed out.")
        print("=" * 70)
        raise

    except requests.exceptions.HTTPError:
        print("=" * 70)
        print("❌ BREVO HTTP ERROR")
        print("Status :", response.status_code)
        print("Body   :", response.text)
        print("=" * 70)
        raise

    except requests.exceptions.RequestException as e:
        print("=" * 70)
        print("❌ BREVO REQUEST ERROR")
        print(str(e))
        print("=" * 70)
        raise

    except Exception as e:
        print("=" * 70)
        print("❌ UNKNOWN BREVO ERROR")
        print(type(e).__name__)
        print(str(e))
        print("=" * 70)
        raise