# Docs Directory Summary

This file summarizes the content and purpose of every markdown file in the `docs/` directory.
For a navigable index with direct links, see [DOCS_INDEX.md](DOCS_INDEX.md).

---

## Root-level files

### `README.md`
Overview of the `docs/` directory with links to the True North section of the docs.
Entry point for the True North sub-topic (hierarchy guide, quick start, and admin cheat card).

### `apps_overview.md`
Reference guide covering every installed Django app in the project.
Lists each app's label, the concrete models it defines, and the purpose of each model.
Apps are listed in the order they appear in `INSTALLED_APPS`.

### `base_overview.md`
Detailed overview of the `base` Django app — the shared foundation used across all other apps.
Documents the abstract models (`CreatedUpdatedBase`, `DateTimeBase`), view mixins, function-based
view decorators, DRF permissions, and management commands provided by `base`.

### `COMPARE__PYTEST__AND__UNITTEST.md`
Side-by-side comparison of running tests and measuring coverage with **pytest** versus
**Django's built-in unittest runner** (`manage.py test`).
Includes actual command output (pass counts, coverage totals) and a recommendation on
whether to standardise on one framework.

### `How_Why_Celery_Redis_Is_Used.md`
Explains why the project uses **Celery** (async/background task execution) and **Redis**
(message broker and result backend), and how the three moving parts — Django, Celery worker,
and Redis — interact at runtime.

### `Justfile.md`
Quick-reference runbook listing every `just` command available at the project root.
Companion to the more detailed `Justfile/Justfile.md`.

### `refactoring_recommendations.md`
Curated list of code-quality observations and refactoring suggestions for the project.
Covers topics such as consolidating timestamp abstract models, removing duplicate logic,
and aligning patterns across apps.  No code changes are included — observations only.

### `registration_accepted_status_report_2026-05-23.md`
Audit report (dated 2026-05-23) confirming which views enforce the `registration_accepted`
access control mechanism.
Covers both vanilla Django views (CBV mixins and FBV decorators) and DRF API views
(`RegistrationAcceptedPermission`), listing compliant and non-compliant views per app.

### `RUNBOOK_Run_Prod_Like_Celery_On_Local.md`
Step-by-step runbook for spinning up a production-like Celery + Redis stack on a local
development machine.
Covers prerequisites (`.env` setup, Redis installation), starting Redis, the Celery worker,
and django-celery-beat scheduler, and validating that tasks run correctly.

### `settings_review.md`
Code-review of `config/settings.py` against current Django 4.x/5.x best practices.
Each section describes the current state, the recommended improvement, and why it matters
(e.g. settings split, `SECRET_KEY` handling, `ALLOWED_HOSTS`, `DATABASES`, static/media,
email, Celery, and security middleware).

### `true_north_admin_cheat_card.md`
One-page cheat card for using the **True North** feature in Django Admin.
Gives the one-sentence meaning of each hierarchy level (CoreValue → Goal → Milestone → Task)
and a 60-second workflow for creating and linking records in Admin.

### `true_north_hierarchy_guide.md`
Full user guide for the **True North** app hierarchy (CoreValue → Goal → Milestone → Task).
Explains the purpose of each level, how they relate to each other, and how consistent use
connects short-term tasks to long-term values.
References `true_north_ordering_guide.md` for ordering details.

### `true_north_ordering_guide.md`
Technical guide on how ordering (the `order` field and `Meta.ordering`) works across all
four True North models.
Explains the current implementation, how users can reorder records, current limitations,
and suggested improvements.

### `true_north_quick_start.md`
Beginner-friendly quick-start for the **True North** app.
Walks through creating CoreValues, Goals, Milestones, and Tasks with concrete examples
and describes every relevant field for each model.

---

## Subdirectories

### `Justfile/`

#### `Justfile/Justfile.md`
Detailed documentation of the project `Justfile`.
Covers prerequisites (`just` installation), a description of every available recipe,
and usage examples.

#### `Justfile/README.md`
Compact command-only reference listing all `just` recipes in a single code block.
Use this for a quick reminder of available commands.

### `runbooks/`

#### `runbooks/Time_Based_Dyno_Scaling_Heroku_Scheduler.md`
Runbook for automating time-based dyno scaling on Heroku using **Heroku Scheduler** and
the `heroku_scale.py` helper script.
Covers the scaling approach, scheduler setup, environment variable configuration,
and how to adjust the scale-up / scale-down schedule.

### `TODOS/`

#### `TODOS/Extract_Apps_To_Packages.md`
Checklist tracking the work to extract individual Django apps into reusable,
independently-installable Python packages.
Lists each app and its completion status.
