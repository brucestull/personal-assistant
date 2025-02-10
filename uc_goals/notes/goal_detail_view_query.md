# `GoalDetailView` Query

```sql
SELECT
"uc_goals_goal"."id",
"uc_goals_goal"."user_id",
"uc_goals_goal"."name",
"uc_goals_goal"."is_ultimate_concern",
"uc_goals_goal"."description",
"uc_goals_goal"."due_date",
"uc_goals_goal"."completed",
"uc_goals_goal"."parent_id",
"uc_goals_goal"."is_archived"
FROM "uc_goals_goal"
WHERE "uc_goals_goal"."user_id" = 1
```
