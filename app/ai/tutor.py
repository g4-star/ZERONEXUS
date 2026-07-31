import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found. Please add it to your .env file."
    )

client = genai.Client(api_key=api_key)


def ask_nexus_ai(course, lesson, question):
    """
    Sends the student's question to Gemini and returns the response.
    """

    prompt = f"""
You are Nexus AI, the official instructor of ZeroNexus AI Academy.

You are teaching the following course:

Course:
{course}

Current Lesson:
{lesson}

Student Question:
{question}

Instructions:
- Teach like an experienced instructor.
- Explain concepts step by step.
- Assume the student is a complete beginner.
- Use simple English.
- Give practical examples.
- Include Python code when appropriate.
- Encourage the student.
- End by asking if the student would like another example or a quiz.
"""

    try:
        response = client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"❌ Gemini Error:⚠️ Nexus AI is temporarily unavailable. {e}"