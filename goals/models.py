from django.db import models


class Goal(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    related_goals = models.ManyToManyField(
        "self",
        through="GoalRelationship",
        symmetrical=False,
        related_name="related_to",  # noqa E501
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Goal"
        verbose_name_plural = "Goals"


class GoalRelationship(models.Model):
    parent_goal = models.ForeignKey(
        Goal, on_delete=models.CASCADE, related_name="subgoals"
    )
    child_goal = models.ForeignKey(
        Goal, on_delete=models.CASCADE, related_name="supergoals"
    )
    relationship_type = models.CharField(
        max_length=50,
        choices=[
            # ("subgoal", "Subgoal"),
            # ("supergoal", "Supergoal"),
            ("goal_hierarchy", "Goal Hierarchy"),
            ("task_hierarchy", "Task Hierarchy"),
        ],
    )

    class Meta:
        unique_together = ("parent_goal", "child_goal")
        verbose_name = "Goal Relationship"
        verbose_name_plural = "Goal Relationships"

    def __str__(self):
        return (
            f"{self.child_goal.name} "
            f" -> "
            f"{self.parent_goal.name}"
            f"({self.relationship_type})"
        )
