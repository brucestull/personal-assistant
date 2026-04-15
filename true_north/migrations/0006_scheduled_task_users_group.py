from django.db import migrations


def create_scheduled_task_users_group(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")

    group, _ = Group.objects.get_or_create(name="ScheduledTaskUsers")

    try:
        crontab_ct = ContentType.objects.get(
            app_label="django_celery_beat",
            model="crontabschedule",
        )
        periodic_task_ct = ContentType.objects.get(
            app_label="django_celery_beat",
            model="periodictask",
        )
    except ContentType.DoesNotExist:
        return

    permissions = Permission.objects.filter(
        content_type__in=[crontab_ct, periodic_task_ct],
        codename__in=[
            "add_crontabschedule",
            "view_crontabschedule",
            "add_periodictask",
            "change_periodictask",
            "delete_periodictask",
            "view_periodictask",
        ],
    )
    group.permissions.add(*permissions)


def delete_scheduled_task_users_group(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name="ScheduledTaskUsers").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("true_north", "0005_corevalueemailschedule_send_time_days_of_week"),
        ("django_celery_beat", "0018_improve_crontab_helptext"),
    ]

    operations = [
        migrations.RunPython(
            create_scheduled_task_users_group,
            delete_scheduled_task_users_group,
        ),
    ]
