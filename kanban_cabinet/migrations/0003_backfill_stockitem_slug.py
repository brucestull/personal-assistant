from django.db import migrations
from django.utils.text import slugify

def forwards(apps, schema_editor):
    StockItem = apps.get_model("kanban_cabinet", "StockItem")

    used = set(
        StockItem.objects.exclude(slug__isnull=True)
        .exclude(slug="")
        .values_list("slug", flat=True)
    )

    for item in StockItem.objects.all().order_by("id"):
        if item.slug:
            used.add(item.slug)
            continue

        base = slugify(getattr(item, "name", "")) or "item"
        candidate = base[:255]

        if candidate in used:
            suffix = f"-{item.id}"
            candidate = f"{base[:255 - len(suffix)]}{suffix}"

            counter = 2
            while candidate in used:
                suffix = f"-{item.id}-{counter}"
                candidate = f"{base[:255 - len(suffix)]}{suffix}"
                counter += 1

        item.slug = candidate
        item.save(update_fields=["slug"])
        used.add(candidate)

def backwards(apps, schema_editor):
    StockItem = apps.get_model("kanban_cabinet", "StockItem")
    StockItem.objects.update(slug=None)

class Migration(migrations.Migration):
    dependencies = [("kanban_cabinet", "0002_stockitem_slug")]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
