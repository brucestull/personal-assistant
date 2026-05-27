# Django Apps Overview

This document lists every installed Django app in the **Personal Assistant** project,
its app label, the concrete models it defines, and the purpose of each model.

Apps are listed in the order they appear in `INSTALLED_APPS` (project apps only;
third-party and Django built-in apps are omitted).

---

## `accounts` — User Accounts & Authentication

**App config:** `accounts.apps.AccountsConfig`

### Models

#### `CustomUser(AbstractUser)`

| Field | Type | Notes |
|---|---|---|
| `registration_accepted` | `BooleanField` | `default=False`; must be set to `True` by an admin before the user can access most features |
| `beastie` | `ForeignKey("accounts.CustomUser")` | Optional self-referential link to a "beastie" (buddy/accountability partner) |

**Purpose:** Extends Django's built-in `AbstractUser` to add the
registration-accepted workflow and the beastie relationship used by the `boosts` app.
This is `AUTH_USER_MODEL` for the entire project.

---

## `app_tracker` — Application & Infrastructure Tracker

**App config:** `app_tracker.apps.AppTrackerConfig`

### Models

#### `OperatingSystem`

| Field | Type | Notes |
|---|---|---|
| `name` | `CharField(100)` | Unique; e.g. `"Ubuntu Server 22.04"` |
| `code_name` | `CharField(100)` | Optional; e.g. `"Jammy Jellyfish"` |

**Purpose:** Reference table of known host operating systems.

---

#### `LanguageFrameworkSystem(CreatedUpdatedBase)`

| Field | Type | Notes |
|---|---|---|
| `name` | `CharField(30)` | Unique; e.g. `"Python"`, `"Django"` |

**Purpose:** Tracks languages, frameworks, and tooling (Python, Django, Docker, etc.)
used in tracked applications.

---

#### `OrganizationalConcept(CreatedUpdatedBase)`

| Field | Type | Notes |
|---|---|---|
| `name` | `CharField(50)` | Unique |
| `description` | `TextField` | Optional |
| `applications` | `ManyToManyField(Application)` | Optional |

**Purpose:** Documents team standards, naming conventions, `TODO`/`LEARN` tag usage,
and other organisational practices, cross-referenced to applications.

---

#### `Label(CreatedUpdatedBase)`

| Field | Type | Notes |
|---|---|---|
| `name` | `CharField(50)` | Unique |
| `hue` | `CharField(25)` | Optional colour value (hex / name) |
| `description` | `TextField` | Optional |
| `application` | `ManyToManyField(Application)` | Optional |

**Purpose:** Tracks GitHub issue/PR label definitions and maps them to applications.

---

#### `Note(CreatedUpdatedBase)`

| Field | Type | Notes |
|---|---|---|
| `title` | `CharField(255)` | |
| `content` | `TextField` | |
| `application` | `ForeignKey(Application)` | Optional; `CASCADE` |

**Purpose:** Free-form development notes attached to specific applications.

---

#### `URL(base.URL)`

| Field | Type | Notes |
|---|---|---|
| *(inherits from `base.URL`)* | | `url`, `label`, `description`, `url_type` |
| `application` | `ForeignKey(Application)` | Optional; `CASCADE` |

**Purpose:** Stores categorised URLs (production, staging, repo, docs, etc.) for
tracked applications.

---

#### `HostQuerySet(QuerySet)` *(custom manager)*

Provides `.visible_on_dashboard()` — filters to `ACTIVE` hosts.

---

#### `Host(CreatedUpdatedBase)`

| Field | Type | Notes |
|---|---|---|
| `name` | `CharField(100)` | Unique |
| `description` | `TextField` | Optional |
| `operating_system` | `ForeignKey(OperatingSystem)` | Optional |
| `host_name` | `CharField(100)` | Unique |
| `mac_address` | `CharField(17)` | Unique; format `XX:XX:XX:XX:XX:XX` |
| `ram` | `CharField(50)` | e.g. `"8GB"` |
| `form_factor` | `CharField(20)` | Choices: Raspberry Pi variants, Desktop, Laptop, VM, Cloud, etc. |
| `ip_address` | `GenericIPAddressField` | Optional |
| `environment` | `CharField(50)` | Choices: `production`, `staging`, `test`, `development` |
| `notes` | `TextField` | Optional |
| `applications` | `ManyToManyField(Application)` | Optional |
| `status` | `CharField(10)` | Choices: `ACTIVE`, `PAUSED`, `RETIRED`; default `ACTIVE` |
| `archived_at` | `DateTimeField` | Optional; when paused or retired |

**Purpose:** Tracks physical/virtual hosts and their relationship to applications.

---

#### `Project(CreatedUpdatedBase)`

| Field | Type | Notes |
|---|---|---|
| `name` | `CharField(255)` | Unique |
| `owner` | `ManyToManyField(AUTH_USER_MODEL)` | |
| `description` | `TextField` | Optional |

**Purpose:** Groups related applications under an overarching project name.

---

#### `Application(CreatedUpdatedBase)`

| Field | Type | Notes |
|---|---|---|
| `project` | `ManyToManyField(Project)` | Optional |
| `name` | `CharField(255)` | Unique |
| `description` | `TextField` | Optional |
| `production_url` | `URLField` | Optional |
| `repository_url` | `URLField` | Optional |
| `reference_repository_url` | `URLField` | Optional |
| `reference_url` | `URLField` | Optional |
| `is_official_repository` | `BooleanField` | |
| `is_adapted_repository` | `BooleanField` | |
| `is_archive_repository` | `BooleanField` | |
| `project_board_url` | `URLField` | Optional |
| `is_favorite` | `BooleanField` | |
| `is_simple_example` | `BooleanField` | |
| `has_custom_user` | `BooleanField` | |
| `has_sticky_footer` | `BooleanField` | |
| `has_prod_deployment` | `BooleanField` | |
| `has_cicd` | `BooleanField` | |
| `has_email_sending` | `BooleanField` | |
| `repository_is_public` | `BooleanField` | |
| `settings_in_environment` | `BooleanField` | |
| `settings_in_dot_env_file` | `BooleanField` | |
| `settings_in_dot_yml_file` | `BooleanField` | |
| `is_template_repository` | `BooleanField` | |
| `is_pending_deployment` | `BooleanField` | |
| `testing_level` | `CharField(6)` | Choices: `high`, `medium`, `low`, `none` |
| `all_tests_passing` | `BooleanField` | |
| `language_framework_systems` | `ManyToManyField(LanguageFrameworkSystem)` | |

**Purpose:** Central tracking record for a software application: its URLs, deployment
status, testing coverage, CI/CD status, and tech stack.

---

#### `DjangoModel(CreatedUpdatedBase)`

| Field | Type | Notes |
|---|---|---|
| `name` | `CharField(255)` | Unique |
| `description` | `TextField` | |
| `is_current_model` | `BooleanField` | `True` = in use, `False` = planned |
| `application` | `ForeignKey(Application)` | `CASCADE` |

**Purpose:** Documents individual Django models belonging to an application — both
currently implemented and future/planned models.

---

## `vitals` — Health Vitals Tracking

**App config:** `vitals.apps.VitalsConfig`

### Models

#### `BloodPressureQuerySet / BloodPressureManager`

Custom queryset with helpers: `.for_user(user)`, `.in_date_range(start, end)`,
`.for_month(year, month)`, `.for_iso_week(iso_year, iso_week)`, and `.summary()` (returns
min/max/avg/median statistics dict).

---

#### `BloodPressure(CreatedUpdatedBase)`

| Field | Type | Notes |
|---|---|---|
| `user` | `ForeignKey(AUTH_USER_MODEL)` | `CASCADE` |
| `systolic` | `PositiveSmallIntegerField` | 50–260 mmHg |
| `diastolic` | `PositiveSmallIntegerField` | 30–160 mmHg |
| `pulse` | `PositiveSmallIntegerField` | 20–220 bpm |
| `note` | `TextField` | Optional |

**Purpose:** Records a single blood pressure measurement (systolic, diastolic, pulse)
for a user.

---

#### `Pulse(CreatedUpdatedBase)`

| Field | Type | Notes |
|---|---|---|
| `user` | `ForeignKey(AUTH_USER_MODEL)` | `CASCADE` |
| `bpm` | `PositiveSmallIntegerField` | |

**Purpose:** Records a stand-alone pulse measurement.

---

#### `Temperature(CreatedUpdatedBase)`

| Field | Type | Notes |
|---|---|---|
| `subject` | `ForeignKey(AUTH_USER_MODEL)` | `CASCADE` |
| `measurement` | `DecimalField(4, 1)` | Degrees Fahrenheit |

**Purpose:** Records a body temperature measurement.

---

#### `BodyWeight(CreatedUpdatedBase)`

| Field | Type | Notes |
|---|---|---|
| `subject` | `ForeignKey(AUTH_USER_MODEL)` | `CASCADE` |
| `measurement` | `DecimalField(5, 2)` | Pounds |

**Purpose:** Records a body-weight measurement.

---

## `uc_goals` — Ultimate Concerns / Goals

**App config:** `uc_goals.apps.UCGoalsConfig`

### Models

#### `Goal`

| Field | Type | Notes |
|---|---|---|
| `user` | `ForeignKey(AUTH_USER_MODEL)` | `CASCADE` |
| `is_ultimate_concern` | `BooleanField` | Marks top-level "ultimate concern" goals |
| `name` | `CharField(255)` | |
| `parent` | `ForeignKey("self")` | Optional; enables hierarchical sub-goals |
| `description` | `TextField` | Optional |
| `character_strengths` | `ManyToManyField(VIACharacterStrength)` | Optional |
| `due_date` | `DateField` | Optional |
| `completed` | `BooleanField` | |
| `is_archived` | `BooleanField` | |

**Purpose:** A hierarchical goal model where top-level goals represent an individual's
"ultimate concerns" and child goals represent sub-goals.

---

#### `Virtue`

| Field | Type | Notes |
|---|---|---|
| `name` | `CharField(255)` | |
| `description` | `TextField` | |

**Purpose:** Reference data for VIA (Values in Action) virtues (e.g. Wisdom, Courage,
Humanity).

---

#### `VIACharacterStrength`

| Field | Type | Notes |
|---|---|---|
| `name` | `CharField(255)` | |
| `description` | `TextField` | |
| `virtue` | `ForeignKey(Virtue)` | `CASCADE` |

**Purpose:** Reference data for individual VIA character strengths (e.g. Creativity,
Bravery, Kindness) grouped under a parent virtue.

---

## `unimportant_notes` — Casual Notes

**App config:** `unimportant_notes.apps.UnimportantNotesConfig`

### Models

#### `NoteTag`

| Field | Type | Notes |
|---|---|---|
| `name` | `CharField(255)` | |
| `author` | `ForeignKey(AUTH_USER_MODEL)` | `CASCADE` |

**Purpose:** User-owned tags for categorising notes.

---

#### `UnimportantNote(base.Note)`

| Field | Type | Notes |
|---|---|---|
| *(inherits `base.Note`)* | | `title`, `content`, `url`, `main_image` (overridden) |
| `author` | `ForeignKey(AUTH_USER_MODEL)` | `CASCADE`; `related_name="notes"` |
| `main_image` | `ImageField` | Overrides `base.Note.main_image`; `upload_to="unimportant_notes/"` |
| `tag` | `ManyToManyField(NoteTag)` | Optional |

**Methods:** `display_tags()` — returns comma-separated tag names.

**Purpose:** Quick, low-stakes notes that a user wants to capture but does not consider
important.

---

## `boosts` — Inspirational Messages

**App config:** `boosts.apps.BoostsConfig`

### Models

#### `Inspirational`

| Field | Type | Notes |
|---|---|---|
| `body` | `TextField` | Required |
| `author` | `ForeignKey(AUTH_USER_MODEL)` | `CASCADE`; `related_name="inspirationals"` |
| `created` | `DateTimeField` | `auto_now_add=True` |

**Purpose:** Stores an inspirational/motivational message created by a user.

---

#### `InspirationalSent`

| Field | Type | Notes |
|---|---|---|
| `inspirational` | `ForeignKey(Inspirational)` | `CASCADE` |
| `inspirational_text` | `TextField` | Snapshot of the message text at time of send |
| `sender` | `ForeignKey(AUTH_USER_MODEL)` | `CASCADE` |
| `beastie` | `ForeignKey(AUTH_USER_MODEL)` | `CASCADE`; recipient |
| `sent_at` | `DateTimeField` | `auto_now_add=True` |

**Purpose:** Audit log of every time an inspirational message was sent to a beastie.

---

#### `RandomInspirationalEmailSend`

| Field | Type | Notes |
|---|---|---|
| `user` | `ForeignKey(AUTH_USER_MODEL)` | `CASCADE` |
| `status` | `CharField(20)` | Choices: `pending`, `sent`, `failed` |
| `created` | `DateTimeField` | `auto_now_add=True` |
| `sent_at` | `DateTimeField` | Optional |
| `inspirational_sent` | `ForeignKey(InspirationalSent)` | Optional; `SET_NULL` |
| `error_message` | `TextField` | Optional |

**Purpose:** Tracks requests for sending a random inspirational to the user themselves,
processed asynchronously via Celery.

---

## `pomodo` — Pomodoro Timer

**App config:** `pomodo.apps.PomodoConfig`

*This app has no Django models.*  It provides a single view (`timer_view`) that renders
a Pomodoro timer interface in the browser.  All timer state is managed client-side.

---

## `story_line` — Story Line Notes

**App config:** `story_line.apps.StoryLineConfig`

### Models

#### `StoryLineNote(base.Note)`

| Field | Type | Notes |
|---|---|---|
| *(inherits `base.Note`)* | | `title`, `content`, `url`, `main_image` |
| `user` | `ForeignKey(AUTH_USER_MODEL)` | `CASCADE` |

**Purpose:** Notes specifically related to story-line or narrative concepts, ordered
newest-first.

---

## `packing_list` — Packing Lists

**App config:** `packing_list.apps.PackingListConfig`

### Models

#### `Activity`

| Field | Type | Notes |
|---|---|---|
| `name` | `CharField(255)` | |
| `description` | `TextField` | Optional |
| `user` | `ForeignKey(AUTH_USER_MODEL)` | `CASCADE` |

**Purpose:** A named activity (e.g. "Camping Trip") that groups packing items and
tasks.

---

#### `ActivityEntry` *(abstract)*

| Field | Type | Notes |
|---|---|---|
| `name` | `CharField(255)` | |
| `description` | `TextField` | Optional |
| `activity` | `ForeignKey(Activity)` | `CASCADE` |
| `user` | `ForeignKey(AUTH_USER_MODEL)` | `CASCADE` |

**Purpose:** Abstract base for both `Item` and `Task`.

---

#### `Item(ActivityEntry)`

| Field | Type | Notes |
|---|---|---|
| `quantity` | `PositiveIntegerField` | Default `1` |
| `is_packed` | `BooleanField` | Default `False` |
| `is_essential` | `BooleanField` | Default `False` |

**Purpose:** A thing to pack for an activity.

---

#### `Task(ActivityEntry)`

| Field | Type | Notes |
|---|---|---|
| `is_completed` | `BooleanField` | Default `False` |

**Purpose:** A to-do task associated with preparing for an activity.

---

## `decide` — Decision-Making Tool

**App config:** `decide.apps.DecideConfig`

### Models

#### `Decision`

| Field | Type | Notes |
|---|---|---|
| `user` | `ForeignKey(User)` | `CASCADE` |
| `title` | `CharField(255)` | |
| `description` | `TextField` | Optional |
| `created_at` | `DateTimeField` | `auto_now_add=True` |
| `quadrant` | `CharField(2)` | Choices: `Q1` Urgent+Important, `Q2` Not Urgent+Important, `Q3` Urgent+Not Important, `Q4` Not Urgent+Not Important |

**Purpose:** A single decision to be evaluated, optionally classified into the
Eisenhower matrix quadrant.

---

#### `Prompt`

| Field | Type | Notes |
|---|---|---|
| `slug` | `SlugField` | Unique |
| `order` | `PositiveIntegerField` | |
| `text` | `CharField(255)` | |

**Purpose:** A reusable decision-framework question/prompt (e.g. "Is this aligned with
my values?"), ordered for presentation.

---

#### `DecisionResponse`

| Field | Type | Notes |
|---|---|---|
| `decision` | `ForeignKey(Decision)` | `CASCADE` |
| `prompt` | `ForeignKey(Prompt)` | `CASCADE` |
| `answer` | `BooleanField` | Yes/No |
| `answered_at` | `DateTimeField` | `auto_now_add=True` |

**Purpose:** Records a user's Yes/No answer to a decision prompt; together the
responses guide the user to a decision quadrant.

---

## `warcrafting` — World of Warcraft Crafting Tracker

**App config:** `warcrafting.apps.WarcraftingConfig`

### Models

#### `TimeStampedModel` *(abstract, local to this app)*

| Field | Type | Notes |
|---|---|---|
| `created` | `DateTimeField` | `auto_now_add=True` |
| `updated` | `DateTimeField` | `auto_now=True` |

> **Note:** Duplicates `base.CreatedUpdatedBase`.  Consider consolidating.

---

#### `Profession(TimeStampedModel)`

| Field | Type | Notes |
|---|---|---|
| `name` | `CharField(64)` | Unique; choices include all WoW professions |

**Purpose:** A World of Warcraft base profession (e.g. Mining, Alchemy).

---

#### `ProfessionTier(TimeStampedModel)`

| Field | Type | Notes |
|---|---|---|
| `profession` | `ForeignKey(Profession)` | `CASCADE` |
| `expansion_label` | `CharField(64)` | Choices: Classic, Burning Crusade, …, The War Within |
| `max_skill` | `PositiveIntegerField` | Auto-filled from known expansion defaults |

**Purpose:** Expansion-specific tier of a profession (e.g. "Cataclysm Mining", max
skill 75).

---

#### `Character(TimeStampedModel)`

| Field | Type | Notes |
|---|---|---|
| `owner` | `ForeignKey(AUTH_USER_MODEL)` | `CASCADE` |
| `name` | `CharField(64)` | Unique per owner |
| `wow_class` | `CharField(32)` | Choices: Warrior, Paladin, …, Evoker |
| `race` | `CharField(32)` | Choices: Human, Orc, …, Earthen |
| `level` | `PositiveIntegerField` | Min 1 |
| `professions` | `ManyToManyField(ProfessionTier)` | Through `CharacterProfession` |

**Properties/methods:** `profile_line` (e.g. `"70 Night Elf Druid"`),
`profession_summary()`, `total_gold()`.

**Purpose:** A WoW character belonging to a user, with class, race, level, and
profession skill tracking.

---

#### `CharacterProfession(TimeStampedModel)` *(through model)*

| Field | Type | Notes |
|---|---|---|
| `character` | `ForeignKey(Character)` | `CASCADE` |
| `profession_tier` | `ForeignKey(ProfessionTier)` | `CASCADE` |
| `current_skill` | `PositiveIntegerField` | Default `0` |

**Property:** `skill_percentage` — percentage toward max skill.

**Purpose:** Through model for the Character ↔ ProfessionTier M2M; stores the
character's current skill level in each expansion tier.

---

#### `Asset(TimeStampedModel)`

| Field | Type | Notes |
|---|---|---|
| `character` | `ForeignKey(Character)` | `CASCADE` |
| `name` | `CharField(128)` | |
| `category` | `CharField(16)` | Choices: `gold`, `currency`, `gear`, `mount`, `pet`, `other` |
| `quantity` | `PositiveIntegerField` | |
| `is_unique` | `BooleanField` | |
| `notes` | `TextField` | Optional |

**Purpose:** Tracks per-character assets — gold, mounts, gear, pets, etc.

---

## `kanban_cabinet` — Kanban-Style Inventory

**App config:** `kanban_cabinet.apps.KanbanCabinetConfig`

### Models

#### `Location`

| Field | Type | Notes |
|---|---|---|
| `owner` | `ForeignKey(AUTH_USER_MODEL)` | `CASCADE` |
| `name` | `CharField(200)` | Unique per owner |
| `description` | `TextField` | Optional |
| `is_active` | `BooleanField` | Default `True` |

**Purpose:** A named physical or logical storage place (e.g. "Bathroom Cabinet / Top
Shelf").

---

#### `StockItem`

| Field | Type | Notes |
|---|---|---|
| `owner` | `ForeignKey(AUTH_USER_MODEL)` | `CASCADE` |
| `location` | `ForeignKey(Location)` | `PROTECT`; optional |
| `name` | `CharField(200)` | Unique per owner+location |
| `slug` | `SlugField(255)` | Auto-generated; unique |
| `description` | `TextField` | Optional |
| `is_physical` | `BooleanField` | |
| `unit_name` | `CharField(50)` | e.g. `"pill"`, `"roll"` |
| `quantity_on_hand` | `PositiveIntegerField` | |
| `target_quantity` | `PositiveIntegerField` | |
| `is_active` | `BooleanField` | |
| `created_at` | `DateTimeField` | `auto_now_add=True` |
| `updated_at` | `DateTimeField` | `auto_now=True` |

**Properties:** `quantity_to_restock`, `needs_restock`.

**Purpose:** Tracks stocked items in a Kanban-style inventory system — you define a
target quantity and see at a glance what needs restocking.

---

## `true_north` — Core Values & Goals (Advanced)

**App config:** `true_north.apps.TrueNorthConfig`

### Models

#### `UserOwnedBase(CreatedUpdatedBase)` *(abstract, local to this app)*

| Field | Type | Notes |
|---|---|---|
| `user` | `ForeignKey(AUTH_USER_MODEL)` | `CASCADE`; `related_name="%(app_label)s_%(class)ss"` |

**Purpose:** Abstract base for all `true_north` models; ties objects to a user and uses
templated related names to avoid collisions.

---

#### `CoreValue(UserOwnedBase, OrderableMixin)`

| Field | Type | Notes |
|---|---|---|
| `name` | `CharField(100)` | Unique per user |
| `slug` | `SlugField(120)` | Auto from name; unique per user |
| `definition` | `TextField` | Optional |
| `is_active` | `BooleanField` | |
| `order` | `PositiveIntegerField` | Auto-assigned on create |

**Purpose:** A personal core value (e.g. "Integrity"), orderable within a user's list.

---

#### `Goal(UserOwnedBase, OrderableMixin)`

| Field | Type | Notes |
|---|---|---|
| `value` | `ForeignKey(CoreValue)` | Optional; `SET_NULL` |
| `title` | `CharField(200)` | |
| `slug` | `SlugField(220)` | Auto from title; unique per user |
| `description` | `TextField` | Optional |
| `status` | `CharField(20)` | Choices: `draft`, `active`, `paused`, `done`, `archived` |
| `start_date` | `DateField` | Optional |
| `target_date` | `DateField` | Optional |
| `is_active` | `BooleanField` | |
| `order` | `PositiveIntegerField` | Auto-assigned per user+value |

**Purpose:** A goal optionally linked to a core value, with status lifecycle and
ordering.

---

#### `Milestone(UserOwnedBase, OrderableMixin)`

| Field | Type | Notes |
|---|---|---|
| `goal` | `ForeignKey(Goal)` | `CASCADE` |
| `description` | `CharField(200)` | |
| `slug` | `SlugField(220)` | Auto from description; unique per goal+user |
| `notes` | `TextField` | Optional |
| `due_date` | `DateField` | Optional |
| `is_completed` | `BooleanField` | |
| `completed_at` | `DateTimeField` | Optional |
| `order` | `PositiveIntegerField` | Auto-assigned per user+goal |

**Purpose:** A milestone (step) toward a goal, orderable within a goal.

---

#### `ValueAction(UserOwnedBase, OrderableMixin)`

| Field | Type | Notes |
|---|---|---|
| `milestone` | `ForeignKey(Milestone)` | `CASCADE`; `related_name="tasks"` |
| `content` | `TextField` | |
| `status` | `CharField(20)` | Choices: `todo`, `doing`, `done`, `skipped` |
| `due_date` | `DateField` | Optional |
| `is_completed` | `BooleanField` | |
| `completed_at` | `DateTimeField` | Optional |
| `order` | `PositiveIntegerField` | Auto-assigned per user+milestone |

**Purpose:** An actionable task (leaf node) belonging to a milestone.

---

#### `CoreValueEmailSchedule(CreatedUpdatedBase)`

| Field | Type | Notes |
|---|---|---|
| `user` | `ForeignKey(AUTH_USER_MODEL)` | `CASCADE` |
| `core_value` | `ForeignKey(CoreValue)` | `CASCADE` |
| `frequency` | `CharField(20)` | Choices: `twice_daily`, `daily`, `three_per_week`, `weekly`, `biweekly`, `monthly` |
| `send_time` | `TimeField` | Optional |
| `days_of_week` | `CharField(20)` | Optional; comma-separated weekday integers `0`–`6` |
| `is_active` | `BooleanField` | |
| `next_send` | `DateTimeField` | Optional |
| `last_sent` | `DateTimeField` | Optional |

**Methods:** `compute_next_send()`, `get_subject()`, `get_content()`,
`get_days_of_week_list()`.

**Purpose:** Schedules recurring email reminders about a core value, processed by
Celery.

---

## `thoughts` — Thoughts Capture

**App config:** `thoughts.apps.ThoughtsConfig`

### Models

#### `Thought(CreatedUpdatedBase)`

| Field | Type | Notes |
|---|---|---|
| `text` | `TextField` | |
| `user` | `ForeignKey(AUTH_USER_MODEL)` | `CASCADE`; `related_name="thoughts"` |

**Purpose:** A simple, free-form thought belonging to a user.

---

## `thing_thought_reminder` — Things, Thoughts & Reminders

**App config:** `thing_thought_reminder.apps.ThingThoughtReminderConfig`

### Models

#### `Thing(CreatedUpdatedBase)`

| Field | Type | Notes |
|---|---|---|
| `user` | `ForeignKey(AUTH_USER_MODEL)` | `CASCADE` |
| `name` | `CharField(255)` | |
| `content` | `TextField` | |
| `type` | `CharField(100)` | Free-form category label |

**Purpose:** A named "thing" (any concept or item) with content and a type label, owned
by a user.

---

#### `Thought(CreatedUpdatedBase)`

| Field | Type | Notes |
|---|---|---|
| `user` | `ForeignKey(AUTH_USER_MODEL)` | `CASCADE`; `related_name="ttr_thoughts"` |
| `name` | `CharField(255)` | |
| `content` | `TextField` | |
| `realm` | `CharField(100)` | Free-form category/realm label |

**Purpose:** A named thought with a realm categorisation, owned by a user.

---

#### `ReminderSchedule(CreatedUpdatedBase)`

| Field | Type | Notes |
|---|---|---|
| `user` | `ForeignKey(AUTH_USER_MODEL)` | `CASCADE` |
| `thing` | `ForeignKey(Thing)` | Optional; `CASCADE` |
| `thought` | `ForeignKey(Thought)` | Optional; `CASCADE` |
| `frequency` | `CharField(20)` | Choices: `daily`, `weekly`, `monthly` |
| `is_active` | `BooleanField` | |
| `next_send` | `DateTimeField` | Optional |
| `last_sent` | `DateTimeField` | Optional |

**Validation:** Must reference exactly one of `thing` or `thought` (not both, not
neither).

**Methods:** `compute_next_send()`, `get_subject()`, `get_content()`.

**Purpose:** Schedules recurring email reminders about either a `Thing` or a
`Thought`, processed by Celery.

---

## `item_location` — Item & Storage Location Tracker

**App config:** `item_location.apps.ItemLocationConfig`

### Models

#### `StorageLocation(CreatedUpdatedBase)`

| Field | Type | Notes |
|---|---|---|
| `user` | `ForeignKey(AUTH_USER_MODEL)` | `CASCADE` |
| `name` | `CharField(255)` | |
| `type` | `CharField(100)` | Choices: `room`, `cabinet`, `shelf`, `drawer`, `box`, `bin`, `closet`, `garage`, `attic`, `basement`, `other` |

**Purpose:** A named storage location (e.g. a drawer, shelf, garage).

---

#### `Item(CreatedUpdatedBase)`

| Field | Type | Notes |
|---|---|---|
| `user` | `ForeignKey(AUTH_USER_MODEL)` | `CASCADE` |
| `name` | `CharField(255)` | |
| `type` | `CharField(100)` | Choices: `tool`, `clothing`, `electronics`, `document`, `food`, `book`, `toy`, `sports`, `kitchen`, `furniture`, `other` |
| `location` | `ForeignKey(StorageLocation)` | Optional; `SET_NULL` |

**Purpose:** Tracks physical items and their current storage location so the user can
find things quickly.

---

## `bus_drive` — Bus/Drive Thoughts

**App config:** `bus_drive.apps.BusDriveConfig`

### Models

#### `Thought(CreatedUpdatedBase)`

| Field | Type | Notes |
|---|---|---|
| `text` | `TextField` | |
| `user` | `ForeignKey(AUTH_USER_MODEL)` | `CASCADE`; `related_name="bus_drive_thoughts"` |

**Purpose:** Captures quick thoughts that occur during commutes (bus/drive).

---

## App Model Count Summary

| App | Model Count |
|---|---|
| `accounts` | 1 |
| `app_tracker` | 9 (including `HostQuerySet`) |
| `vitals` | 4 (+ custom queryset/manager) |
| `uc_goals` | 3 |
| `unimportant_notes` | 2 |
| `boosts` | 3 |
| `pomodo` | 0 |
| `story_line` | 1 |
| `packing_list` | 4 (1 abstract + 3 concrete) |
| `decide` | 3 |
| `warcrafting` | 6 (1 abstract + 5 concrete) |
| `kanban_cabinet` | 2 |
| `true_north` | 6 (2 abstract + 4 concrete) |
| `thoughts` | 1 |
| `thing_thought_reminder` | 3 |
| `item_location` | 2 |
| `bus_drive` | 1 |
