# add_it_automation_skills.py

from career_organizerator.models import Skill
from django.contrib.auth import get_user_model


# Skill names without the asterisks
skill_names = [
    "Applicant Tracking System",
    "Application Performance Management",
    "Application Programming Interface (API)",
    "Automation",
    "Bash (Scripting Language)",
    "CI/CD",
    "Cloud Computing",
    "Cloud Services",
    "Cloud Storage",
    "Command-Line Interface",
    "Computer Programming",
    "Configuration Management",
    "Containerization",
    "Continuous Integration",
    "Data Structures",
    "Debugging",
    "Development Environment",
    "Development Testing",
    "DevOps",
    "Docker (Software)",
    "File Management",
    "Git (Version Control System)",
    "GitHub",
    "Image Analysis",
    "Incident Management",
    "Infrastructure Architecture",
    "Infrastructure as Code (IaC)",
    "Integrated Development Environments",
    "Interviewing Skills",
    "Issue Tracking",
    "JSON",
    "Kubernetes",
    "Linux Commands",
    "Load Balancing",
    "Maintainability",
    "Network Troubleshooting",
    "Operating Systems",
    "OS Process Management",
    "Performance Tuning",
    "Problem Management",
    "Programming Principles",
    "Puppet (Configuration Management Tool)",
    "Python Programming",
    "RESTful API",
    "Scripting",
    "Scalability",
    "Software Development Tools",
    "Software Engineering Tools",
    "Software Testing",
    "String/List/Dictionary Use",
    "System Monitoring",
    "System Support",
    "Technical Communication",
    "Technical Documentation",
    "Technical Support",
    "Unit Testing",
    "Version Control",
    "Web Services",
]

# Get user with ID 1
User = get_user_model()
user = User.objects.get(id=1)

# Create and save Skill objects
for index, skill_name in enumerate(skill_names):
    skill, created = Skill.objects.get_or_create(
        user=user, name=skill_name, defaults={"order": index}
    )
    if created:
        print(f"Added: {skill_name}")
    else:
        print(f"Skipped (already exists): {skill_name}")
