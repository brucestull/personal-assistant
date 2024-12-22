# Goal Models

[Goal Tracking Models](https://chatgpt.com/share/675f01ee-3fe8-8002-aa84-0d6b54ab21dc)

## The Code

To implement a system for tracking "Goals" that can be goals, sub-goals, or super-goals, with many-to-many relationships, you can structure your Django models as follows:

### Models Implementation

```python
from django.db import models

class Goal(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    related_goals = models.ManyToManyField(
        'self', 
        through='GoalRelationship', 
        symmetrical=False, 
        related_name='related_to'
    )
    
    def __str__(self):
        return self.name

class GoalRelationship(models.Model):
    parent_goal = models.ForeignKey(
        Goal, 
        on_delete=models.CASCADE, 
        related_name='subgoals'
    )
    child_goal = models.ForeignKey(
        Goal, 
        on_delete=models.CASCADE, 
        related_name='supergoals'
    )
    relationship_type = models.CharField(
        max_length=50,
        choices=[
            ('subgoal', 'Subgoal'),
            ('supergoal', 'Supergoal'),
        ]
    )

    class Meta:
        unique_together = ('parent_goal', 'child_goal')

    def __str__(self):
        return f"{self.parent_goal.name} -> {self.child_goal.name} ({self.relationship_type})"
```

### Explanation

1. **Goal Model**:
   - Represents a single "Goal."
   - Has attributes like `name`, `description`, `due_date`, and `completed` status.
   - Includes a `related_goals` field that establishes a many-to-many relationship with itself through the `GoalRelationship` model.

2. **GoalRelationship Model**:
   - Handles the many-to-many relationships between `Goal` instances.
   - Specifies a `relationship_type` field to identify if a relationship is a "subgoal" or "supergoal."
   - Enforces `unique_together` to prevent duplicate relationships between the same parent and child goals.

3. **Symmetry**:
   - The `symmetrical=False` in the `related_goals` field ensures that relationships are directional. For example, a goal can be a subgoal to one goal and a supergoal to another.

4. **Relationships**:
   - By using the `GoalRelationship` model, you can track the directionality and type of relationships between goals.

### Example Usage

#### Creating Goals
```python
goal1 = Goal.objects.create(name="Learn Django")
goal2 = Goal.objects.create(name="Build a Django App")
goal3 = Goal.objects.create(name="Understand Django Models")

# Adding relationships
GoalRelationship.objects.create(
    parent_goal=goal1, child_goal=goal2, relationship_type="supergoal"
)
GoalRelationship.objects.create(
    parent_goal=goal3, child_goal=goal2, relationship_type="subgoal"
)
```

#### Querying Relationships
```python
# Get subgoals of a goal
subgoals = goal1.subgoals.all()

# Get supergoals of a goal
supergoals = goal2.supergoals.all()

# Get related goals
related_goals = goal2.related_goals.all()
```

This structure gives you the flexibility to manage hierarchical goal relationships while maintaining clear directionality.
