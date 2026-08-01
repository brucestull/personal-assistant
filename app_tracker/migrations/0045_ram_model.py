from django.db import migrations, models
import django.db.models.deletion


def copy_host_ram_to_lookup(apps, schema_editor):
    Host = apps.get_model("app_tracker", "Host")
    Ram = apps.get_model("app_tracker", "Ram")

    for host in Host.objects.exclude(ram__isnull=True).exclude(ram="").iterator():
        value = host.ram.strip()
        if not value:
            continue

        ram, _ = Ram.objects.get_or_create(name=value)
        host.ram_lookup = ram
        host.save(update_fields=["ram_lookup"])


class Migration(migrations.Migration):
    dependencies = [
        ("app_tracker", "0044_add_sshconnection"),
    ]

    operations = [
        migrations.CreateModel(
            name="Ram",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="The date and time this object was created.",
                        verbose_name="Created",
                    ),
                ),
                (
                    "updated",
                    models.DateTimeField(
                        auto_now=True,
                        help_text="The date and time this object was last updated.",
                        verbose_name="Updated",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="e.g., 500MB, .5GB, 2GB, 4GB, 8GB",
                        max_length=50,
                        unique=True,
                        verbose_name="RAM",
                    ),
                ),
            ],
            options={
                "verbose_name": "RAM",
                "verbose_name_plural": "RAM",
                "ordering": ["name"],
            },
        ),
        migrations.AddField(
            model_name="host",
            name="ram_lookup",
            field=models.ForeignKey(
                blank=True,
                help_text="The RAM configuration for this host.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="hosts",
                to="app_tracker.ram",
                verbose_name="RAM",
            ),
        ),
        migrations.RunPython(copy_host_ram_to_lookup, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="host",
            name="ram",
        ),
        migrations.RenameField(
            model_name="host",
            old_name="ram_lookup",
            new_name="ram",
        ),
    ]
