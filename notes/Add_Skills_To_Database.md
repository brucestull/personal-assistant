# `add_it_automation_skills.py`

```python
# load_skills.py

from your_app.models import Skill
from django.contrib.auth import get_user_model

# Replace 'your_app' with the actual name of the app that contains the Skill model

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
    "Web Services"
]

# Get user with ID 1
User = get_user_model()
user = User.objects.get(id=1)

# Create and save Skill objects
for index, skill_name in enumerate(skill_names):
    skill, created = Skill.objects.get_or_create(
        user=user,
        name=skill_name,
        defaults={'order': index}
    )
    if created:
        print(f"Added: {skill_name}")
    else:
        print(f"Skipped (already exists): {skill_name}")
```

---

I have a Django model `Skill`:

```python
class Skill(OrderableMixin, CreatedUpdatedBase):
    """
    This model represents a single skill.

    Attributes:
        user (ForeignKey): The user who created the skill.
        name (CharField): The name of the skill.
    """

    # `user` is the user who created the skill.
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        verbose_name="User",
        help_text="The user who created the skill.",
        on_delete=models.CASCADE,
    )

    # `name` is the name of the skill.
    name = models.CharField(
        verbose_name="Name",
        help_text="The name of the skill.",
        max_length=255,
    )

    order = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        # If the object is new and doesn't have an order yet
        if not self.pk and not hasattr(self, "order"):
            # Get the highest order number
            highest_order = Skill.objects.all().aggregate(models.Max("order"))[
                "order__max"
            ]
            # Add one to that number and make it this object's order
            self.order = (highest_order if highest_order is not None else -1) + 1
        # Call the "real" save() method. In other words, call the super class'
        # save() method.
        super(Skill, self).save(*args, **kwargs)

    def __str__(self):
        """
        Returns the string representation of the skill.
        """
        return self.name

    class Meta:
        verbose_name_plural = "Skills"
```

Here is a list of skills:

```markdown
* Applicant Tracking System
* Application Performance Management
* Application Programming Interface (API)
* Automation
* Bash (Scripting Language)
* CI/CD
* Cloud Computing
* Cloud Services
* Cloud Storage
* Command-Line Interface
* Computer Programming
* Configuration Management
* Containerization
* Continuous Integration
* Data Structures
* Debugging
* Development Environment
* Development Testing
* DevOps
* Docker (Software)
* File Management
* Git (Version Control System)
* GitHub
* Image Analysis
* Incident Management
* Infrastructure Architecture
* Infrastructure as Code (IaC)
* Integrated Development Environments
* Interviewing Skills
* Issue Tracking
* JSON
* Kubernetes
* Linux Commands
* Load Balancing
* Maintainability
* Network Troubleshooting
* Operating Systems
* OS Process Management
* Performance Tuning
* Problem Management
* Programming Principles
* Puppet (Configuration Management Tool)
* Python Programming
* RESTful API
* Scripting
* Scalability
* Software Development Tools
* Software Engineering Tools
* Software Testing
* String/List/Dictionary Use
* System Monitoring
* System Support
* Technical Communication
* Technical Documentation
* Technical Support
* Unit Testing
* Version Control
* Web Services
```

Remove the `*` from each line of the skills and provide a python script to load these skills into the database for user with ID of `1`.

---

Here's a Python script that loads the skills into your Django database for the user with ID `1`. This script assumes you are running it within the Django environment (e.g., via `shell` or a management command):

---

### ✅ **Script: `load_skills.py`**

```python
# load_skills.py

from your_app.models import Skill
from django.contrib.auth import get_user_model

# Replace 'your_app' with the actual name of the app that contains the Skill model

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
    "Web Services"
]

# Get user with ID 1
User = get_user_model()
user = User.objects.get(id=1)

# Create and save Skill objects
for index, skill_name in enumerate(skill_names):
    skill, created = Skill.objects.get_or_create(
        user=user,
        name=skill_name,
        defaults={'order': index}
    )
    if created:
        print(f"Added: {skill_name}")
    else:
        print(f"Skipped (already exists): {skill_name}")
```

---

### 🔧 **Usage Options**

**Option 1: Run from Django shell**

```bash
python manage.py shell
```

```python
exec(open('load_skills.py').read())
```

**Option 2: Convert to Django management command**
Put the script logic inside `your_app/management/commands/load_skills.py`.

Would you like me to provide that version as well?

---

Update this to use a Django management command. Also, if appropriate, separate the list of skills into a .json.

```python
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
```

---

Here’s how to update your script to use a proper **Django management command**, and to load the list of skills from a separate `.json` file.

---

### ✅ Step 1: Create the JSON File

Save the following as `it_automation_skills.json` (you can put it in your app directory or another directory like `career_organizerator/data/`):

```json
[
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
  "Web Services"
]
```

---

### ✅ Step 2: Create the Management Command

File: `career_organizerator/management/commands/load_it_skills.py`

```python
import json
import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from career_organizerator.models import Skill


class Command(BaseCommand):
    help = "Load IT Automation skills into the database for a given user."

    def add_arguments(self, parser):
        parser.add_argument(
            "--user-id",
            type=int,
            required=True,
            help="User ID to associate the skills with."
        )
        parser.add_argument(
            "--json-path",
            type=str,
            default="career_organizerator/data/it_automation_skills.json",
            help="Path to the JSON file containing skill names."
        )

    def handle(self, *args, **options):
        user_id = options["user_id"]
        json_path = options["json_path"]

        # Load the skill names from the JSON file
        if not os.path.exists(json_path):
            self.stderr.write(self.style.ERROR(f"JSON file not found at {json_path}"))
            return

        with open(json_path, "r", encoding="utf-8") as f:
            try:
                skill_names = json.load(f)
            except json.JSONDecodeError as e:
                self.stderr.write(self.style.ERROR(f"Invalid JSON format: {e}"))
                return

        User = get_user_model()
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            self.stderr.write(self.style.ERROR(f"User with ID {user_id} does not exist."))
            return

        created_count = 0
        skipped_count = 0

        for index, skill_name in enumerate(skill_names):
            skill, created = Skill.objects.get_or_create(
                user=user,
                name=skill_name,
                defaults={"order": index},
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"✅ Added: {skill_name}"))
            else:
                skipped_count += 1
                self.stdout.write(f"⚠️ Skipped (already exists): {skill_name}")

        self.stdout.write(
            self.style.NOTICE(
                f"\nSummary:\n  ➕ Created: {created_count}\n  🔁 Skipped: {skipped_count}"
            )
        )
```

---

### ✅ Step 3: Run the Command

From your project root:

```bash
python manage.py load_it_skills --user-id 1
```

Optionally specify a custom JSON path:

```bash
python manage.py load_it_skills --user-id 1 --json-path custom/path/to/skills.json
```

---

Let me know if you'd like this to:

* Work interactively (prompt for confirmation)?
* Add tags or categories to the skills?
* Load skills into multiple users?

I'm happy to help extend it.
