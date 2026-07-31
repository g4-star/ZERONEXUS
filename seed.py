from app import create_app
from app.extensions import db
from app.models import Team

app = create_app()

teams_data = [
    {
        'slug': 'blue-defense',
        'name': 'Blue Defense',
        'lead_name': 'Team Lead',
        'lead_role': 'Blue Team Lead',
        'short_description': 'Defensive security, monitoring, SOC operations, and incident response.',
        'description': 'Blue Defense focuses on threat detection, monitoring, SIEM operations, incident handling, and defensive security engineering.'
    },
    {
        'slug': 'threat-hunters',
        'name': 'Threat Hunters',
        'lead_name': 'Team Lead',
        'lead_role': 'Threat Hunting Lead',
        'short_description': 'Threat hunting, malware analysis, and detection engineering.',
        'description': 'Threat Hunters proactively search for hidden threats, analyze malware, and improve detection capabilities.'
    },
    {
        'slug': 'red-operations',
        'name': 'Red Operations',
        'lead_name': 'Team Lead',
        'lead_role': 'Red Team Lead',
        'short_description': 'Offensive security, ethical hacking, and penetration testing.',
        'description': 'Red Operations conducts ethical hacking exercises, penetration tests, and adversary simulations.'
    },
    {
        'slug': 'digital-forensics',
        'name': 'Digital Forensics',
        'lead_name': 'Team Lead',
        'lead_role': 'Forensics Lead',
        'short_description': 'Digital investigations, evidence handling, and forensic analysis.',
        'description': 'Digital Forensics investigates security incidents and performs evidence acquisition and analysis.'
    },
    {
        'slug': 'cloud-security',
        'name': 'Cloud Security',
        'lead_name': 'Team Lead',
        'lead_role': 'Cloud Security Lead',
        'short_description': 'Cloud infrastructure security, IAM, and DevSecOps.',
        'description': 'Cloud Security secures cloud platforms, identity systems, containers, and DevSecOps pipelines.'
    },
    {
        'slug': 'ai-security',
        'name': 'AI Security',
        'lead_name': 'Team Lead',
        'lead_role': 'AI Security Lead',
        'short_description': 'AI safety, model security, and responsible AI engineering.',
        'description': 'AI Security researches secure AI systems, model protection, prompt security, and AI safety.'
    }
]

with app.app_context():
    db.create_all()

    for item in teams_data:
        existing = Team.query.filter_by(slug=item['slug']).first()
        if not existing:
            db.session.add(Team(**item))

    db.session.commit()
    print('6 teams created successfully.')