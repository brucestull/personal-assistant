# Generated migration

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("true_north", "0004_add_corevalue_email_schedule"),
    ]

    operations = [
        migrations.AddField(
            model_name="corevalueemailschedule",
            name="send_time",
            field=models.TimeField(
                blank=True,
                null=True,
                help_text=(
                    "Time of day to receive the reminder (e.g. 09:00). "
                    "Leave blank to use the current time when the schedule is created."
                ),
            ),
        ),
        migrations.AddField(
            model_name="corevalueemailschedule",
            name="days_of_week",
            field=models.CharField(
                blank=True,
                default="",
                max_length=20,
                help_text=(
                    "Comma-separated weekday numbers (0=Mon \u2026 6=Sun) on which to send "
                    "reminders.  When set, overrides the Frequency field."
                ),
            ),
        ),
        migrations.AlterField(
            model_name="corevalueemailschedule",
            name="frequency",
            field=models.CharField(
                choices=[
                    ("twice_daily", "Twice a day (every 12 hours)"),
                    ("daily", "Once a day"),
                    ("three_per_week", "Three times a week (every 2 days)"),
                    ("weekly", "Once a week"),
                    ("biweekly", "Every two weeks"),
                    ("monthly", "Once a month"),
                ],
                default="daily",
                help_text=(
                    "How often to receive a reminder "
                    "(used when no specific days are chosen)."
                ),
                max_length=20,
            ),
        ),
    ]
