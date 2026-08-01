from app import create_app
from app.extensions import db
from app.models.course import Course
from app.models.lesson import Lesson

app = create_app()

with app.app_context():

    # Delete existing lessons and courses
    Lesson.query.delete()
    Course.query.delete()
    db.session.commit()

    courses = [
        {
            "title": "Python Fundamentals",
            "slug": "python",
            "description": "Learn Python from beginner to advanced.",
            "icon": "🐍",
            "level": "Beginner",
            "duration": "12 Hours",
            "lessons": [
                "What is Python?",
                "Installing Python",
                "Variables",
                "Data Types",
                "Conditions",
                "Loops",
                "Functions",
                "Lists",
                "Dictionaries",
                "File Handling",
                "Object-Oriented Programming",
                "Final Project"
            ]
        },
        {
            "title": "HTML • CSS • JavaScript",
            "slug": "web-development",
            "description": "Build beautiful, responsive and interactive websites.",
            "icon": "🌐",
            "level": "Beginner",
            "duration": "15 Hours",
            "lessons": [
                "Introduction to the Web",
                "HTML Basics",
                "HTML Forms",
                "Semantic HTML",
                "CSS Basics",
                "CSS Layout",
                "Flexbox",
                "Grid",
                "Responsive Design",
                "JavaScript Basics",
                "DOM Manipulation",
                "Events",
                "Functions",
                "Arrays",
                "Objects",
                "ES6",
                "Async JavaScript",
                "APIs",
                "Mini Project",
                "Portfolio Website"
            ]
        },
        {
            "title": "Cybersecurity",
            "slug": "cybersecurity",
            "description": "Ethical hacking, SOC, Blue Team and Digital Forensics.",
            "icon": "🛡",
            "level": "Intermediate",
            "duration": "20 Hours",
            "lessons": [
                "Introduction to Cybersecurity",
                "Linux Basics",
                "Networking",
                "TCP/IP",
                "Ports and Services",
                "Nmap",
                "Web Security",
                "OWASP Top 10",
                "Burp Suite",
                "SQL Injection",
                "XSS",
                "Authentication",
                "Wireshark",
                "Digital Forensics",
                "Incident Response",
                "SOC Fundamentals",
                "Threat Hunting",
                "Malware Basics",
                "Reporting",
                "Final Lab"
            ]
        },
        {
            "title": "Artificial Intelligence",
            "slug": "artificial-intelligence",
            "description": "Learn AI, prompt engineering and machine learning.",
            "icon": "🤖",
            "level": "Beginner",
            "duration": "10 Hours",
            "lessons": [
                "Introduction to AI",
                "Generative AI",
                "Prompt Engineering",
                "ChatGPT",
                "AI Tools",
                "Machine Learning Basics",
                "Neural Networks",
                "Computer Vision",
                "Natural Language Processing",
                "Building AI Apps"
            ]
        }
    ]

    for course_data in courses:

        course = Course(
            title=course_data["title"],
            slug=course_data["slug"],
            description=course_data["description"],
            icon=course_data["icon"],
            level=course_data["level"],
            duration=course_data["duration"],
            published=True
        )

        db.session.add(course)
        db.session.commit()

        for number, title in enumerate(course_data["lessons"], start=1):

            lesson = Lesson(
                course_id=course.id,
                lesson_number=number,
                title=title,
                content=f"Content for {title} will be added here.",
                estimated_time="15 Minutes",
                level=course.level,
                published=True
            )

            db.session.add(lesson)

        db.session.commit()

    print("ZeroNexus Academy seeded successfully.")