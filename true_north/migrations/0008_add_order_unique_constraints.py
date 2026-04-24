from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Add unique-order constraints in a separate migration from the data
    normalisation in 0007 so that each runs in its own transaction.

    PostgreSQL raises "cannot ALTER TABLE because it has pending trigger events"
    when an ALTER TABLE (AddConstraint) follows UPDATE statements in the same
    transaction.  Keeping the RunPython and the DDL in separate migrations
    guarantees a transaction boundary between them.
    """

    dependencies = [
        (
            "true_north",
            "0007_corevalue_true_north_corevalue_unique_order_per_user_and_more",
        ),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="corevalue",
            constraint=models.UniqueConstraint(
                fields=("user", "order"),
                name="true_north_corevalue_unique_order_per_user",
            ),
        ),
        migrations.AddConstraint(
            model_name="goal",
            constraint=models.UniqueConstraint(
                condition=models.Q(("value__isnull", False)),
                fields=("user", "value", "order"),
                name="true_north_goal_unique_order_per_value",
            ),
        ),
        migrations.AddConstraint(
            model_name="goal",
            constraint=models.UniqueConstraint(
                condition=models.Q(("value__isnull", True)),
                fields=("user", "order"),
                name="true_north_goal_unique_order_without_value",
            ),
        ),
        migrations.AddConstraint(
            model_name="milestone",
            constraint=models.UniqueConstraint(
                fields=("user", "goal", "order"),
                name="true_north_milestone_unique_order_per_goal",
            ),
        ),
        migrations.AddConstraint(
            model_name="valueaction",
            constraint=models.UniqueConstraint(
                fields=("user", "milestone", "order"),
                name="true_north_valueaction_unique_order_per_milestone",
            ),
        ),
    ]
