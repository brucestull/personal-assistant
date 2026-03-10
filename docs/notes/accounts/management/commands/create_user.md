# `create_user` Management Command – Deep Dive

- [Django Create User Management Command - ChatGPT - Private](https://chatgpt.com/c/68a06085-29e4-8322-8e65-c5e9af1f62e9)
- [Django Create User Management Command - ChatGPT - Shared](https://chatgpt.com/share/68a0665c-5f6c-8002-8581-f50fd505bb80)

This command creates a **superuser** and/or a **regular user** using values from a `.env` file. It’s designed for **repeatable, idempotent** bootstrapping in development, CI, and admin tasks.

---

## Why this exists

- **Bootstrap fast**: Spin up a dev DB with a known admin and demo user.
- **Automate CI**: Seed accounts before integration tests.
- **Safe updates**: With `--update-existing`, rotate credentials or elevate privileges reproducibly.

---

## How to run it

- Create a `.env` file (default expected at `project_root/.env`), then:

```bash
# Create both superuser + regular user
python manage.py create_user

# Only superuser
python manage.py create_user --create su

# Only regular user
python manage.py create_user --create user

# Update an existing username with current .env values
python manage.py create_user --create user --update-existing

# Use a custom .env path
python manage.py create_user --dotenv ./config/local.env
```

> Tip: The command is **idempotent**. Running it repeatedly won’t create duplicates; it either updates or no-ops.

---

## Environment Variables

### Superuser

| Env var              | Required | Maps to    |
| -------------------- | -------- | ---------- |
| `DJANGO_SU_NAME`     | ✅        | `username` |
| `DJANGO_SU_EMAIL`    | ❌        | `email`    |
| `DJANGO_SU_PASSWORD` | ❌        | `password` |

### Regular user

| Env var                | Required | Maps to                    |
| ---------------------- | -------- | -------------------------- |
| `DJANGO_USER_NAME`     | ✅        | `username`                 |
| `DJANGO_USER_EMAIL`    | ❌        | `email`                    |
| `DJANGO_USER_PASSWORD` | ❌        | `password`                 |
| `DJANGO_USER_ACCEPTED` | ❌        | `registration_accepted`(1) |
| `DJANGO_USER_IS_STAFF` | ❌        | `is_staff`                 |

(1) `registration_accepted` is an example of a **custom field** your project might use. If your `CustomUser` doesn’t have it, the extra value is simply ignored.

**Password behavior:**

* If `password` is **omitted or empty**, we pass `None` to `create_user()`, which gives the user an **unusable password** (cannot log in via password). For a superuser, you almost certainly want a real password.

---

## CLI Options

| Option              | Meaning                                                                |
| ------------------- | ---------------------------------------------------------------------- |
| `--create`          | What to create: `su`, `user`, or `both` (default).                     |
| `--update-existing` | If a username already exists, update email/password/flags from `.env`. |
| `--dotenv PATH`     | Path to `.env` file (default: `project_root/.env`).                    |

---

## Walkthrough of the code

This section explains each constant, function, and step.

### Module-level constants

* `ENV_ROOT = Path(__file__).resolve().parents[3]`
  Finds the project root by walking up from `accounts/management/commands/`. This is used to default `.env` to `project_root/.env` while keeping a `--dotenv` override.

* `DOTENV_PATH = ENV_ROOT / ".env"`
  The default `.env` path. You can override it with `--dotenv`.

* `SU_VARS` / `USER_VARS`
  Dictionaries mapping semantic keys (`username`, `email`, etc.) to exact environment variable names. Centralizing these lets `_read_env()` stay generic and makes it trivial to add/remove env controls later.

### Class: `Command(BaseCommand)`

* `help`
  The one-liner shown in `python manage.py help`.

* `add_arguments(self, parser)`
  Declares three flags:

  * `--create {su|user|both}`: chooses the accounts to act on.
  * `--update-existing`: toggles updating an existing username.
  * `--dotenv`: where to load environment values from.

* `handle(self, *args, **options)`
  Orchestrates the run:

  1. Loads the `.env` (raises `CommandError` if missing).
  2. Depending on `--create`, calls `_create_superuser()` and/or `_create_regular_user()`.
  3. If neither created nor updated anything, prints “Nothing to do.”

### Helper: `_read_env(mapping) -> (username, email, password, extras)`

* Reads env vars per the supplied `mapping` (`SU_VARS` or `USER_VARS`).
* Ensures `username` is present; otherwise raises `CommandError`.
* Returns:

  * `username`, `email`, `password` strings (empty string if missing for email/password).
  * `extras` dict of optional flags. For regular users, this may include:

    * `registration_accepted` from `DJANGO_USER_ACCEPTED` (`"1"`/`"0"`).
    * `is_staff` from `DJANGO_USER_IS_STAFF` (`"1"`/`"0"`).

### Helper: `_ensure_user(..., update_existing: bool, **extra_fields)`

* Decorated with `@transaction.atomic` so create/update is all-or-nothing.
* Looks up the user by `username`:

  * **If exists**:

    * With `--update-existing`:

      * Updates **only provided** values (email if non-empty, password if non-empty, and any boolean flags present in `extra_fields`).
      * Calls `set_password()` to hash a new password.
      * Saves and prints a success message if anything changed; otherwise prints a no-change warning.
    * Without `--update-existing`:

      * Prints a “user already exists” warning and does nothing.
    * Returns `False` (not created).
  * **If does not exist**:

    * Calls `User.objects.create_user(...)` to create a new user.

      * `password or None` ensures that an empty string results in an **unusable** password (safe default).
      * `**extra_fields` applies flags like `is_staff`, `is_superuser`, `registration_accepted`.
    * Prints a success message and returns `True` (created).

### Helper: `_create_superuser(update_existing)`

* Reads SU envs via `_read_env(SU_VARS)`.
* Forces:

  * `is_superuser = True`
  * `is_staff = True`
  * `registration_accepted = True` (if applicable)
* Calls `_ensure_user(...)` with those flags. If a user already exists but isn’t a superuser, `--update-existing` will **elevate** them.

### Helper: `_create_regular_user(update_existing)`

* Reads regular user envs via `_read_env(USER_VARS)`.
* Forces `is_superuser = False` explicitly (belt & suspenders).
* Delegates to `_ensure_user(...)`.

---

## Data integrity & safety

* **Transactional updates**: `_ensure_user` is atomic, so partial writes don’t leave users in a half-updated state.
* **Idempotent**: Running the command multiple times won’t create duplicates.
* **Selective updates**: Only non-empty email/password and declared flags change with `--update-existing`.
* **Safe defaults**: Missing password → unusable password; safe in dev/CI but not acceptable for real admin accounts.

---

## Custom user model considerations

If your `AUTH_USER_MODEL` adds required fields, pass them via env and add them to `USER_VARS`/`SU_VARS`, then map them in `_read_env()` to populate `extras`. Example:

```python
# add to USER_VARS:
"first_name": "DJANGO_USER_FIRST",
"last_name": "DJANGO_USER_LAST",
```

Then in `_read_env()`:

```python
if "first_name" in mapping:
    extras["first_name"] = os.getenv(mapping["first_name"], "")
if "last_name" in mapping:
    extras["last_name"] = os.getenv(mapping["last_name"], "")
```

---

## Examples

**Create or update both users from a custom env file:**

```bash
python manage.py create_user --dotenv ./envs/dev.env --update-existing
```

**Promote an existing user to superuser:**

```bash
export DJANGO_SU_NAME="existing_username"
python manage.py create_user --create su --update-existing
```

**Create a demo user without a password (unusable):**

```bash
export DJANGO_USER_NAME="demo"
export DJANGO_USER_EMAIL="demo@example.com"
python manage.py create_user --create user
```

---

## Troubleshooting

* **“.env file not found”**
  Pass `--dotenv PATH` or ensure `project_root/.env` exists.
* **“XYZ not set”**
  Required variable (`DJANGO_*_NAME`) missing. Add it to your `.env`.
* **“Nothing to do.”**
  Nothing was created, and either no updates were requested or provided values matched existing fields.
* **Can’t log in after creation**
  You probably created a user with an **unusable password** (empty/omitted). Set a real password in `.env` or run with `--update-existing` after setting it.

---

## Testing tips

* Use a temp database (e.g., `sqlite3 :memory:`) and `.env` fixtures.
* Mock `os.getenv` in unit tests to simulate env permutations.
* Assert both **creation** and **update** branches:

  * Existing user w/ `--update-existing`
  * Existing user w/o `--update-existing`
  * Missing required env (assert `CommandError`)

---
