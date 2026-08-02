from datetime import datetime


class AIService:

    @staticmethod
    def welcome(user):

        return (

            f"Welcome back {user.username}! "

            "I'm ZeroNexus AI. "

            "I can help you with "

            "Python, Networking, "

            "Linux, SOC, Digital Forensics, "

            "Web Security, Programming "

            "and Cybersecurity."

        )

    @staticmethod
    def starter_prompts():

        return [

            "Explain Python variables",

            "Teach me Networking",

            "Start Linux Basics",

            "Teach Ethical Hacking",

            "Create a SOC Lab",

            "Explain SQL Injection",

            "Create a Python Quiz",

            "Generate CTF Challenge"

        ]

    @staticmethod
    def generate(prompt):

        """
        Temporary placeholder.

        Replace this method later with

        OpenAI

        Ollama

        Gemini

        Claude

        etc.

        """

        return {

            "prompt": prompt,

            "response":

                "ZeroNexus AI backend "

                "is not connected yet.",

            "time":

                datetime.utcnow()

        }