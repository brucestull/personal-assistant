## 1. What this Justfile is for

This `Justfile` replaces your Makefile as a tiny task runner for your Django repo. It provides:

* cleanup of caches/coverage
* test + coverage flows
* migrations + DB reset/seed flows
* runserver, shell, create superuser
* a built-in help menu

Everything is meant to be run from the repo root.

---

## 2. Prereqs (one-time setup)

### Install `just`

Pick one:

**macOS (Homebrew)**

```bash
brew install just
```

**Linux**

* If your distro has it:

```bash
sudo apt install just
# or
sudo dnf install just
# or
sudo pacman -S just
```

* If not, Cargo works everywhere:

```bash
cargo install just
```

**Windows**

* If you’re using WSL (you are), install inside WSL with apt/cargo.
* If you want native Windows:

```powershell
choco install just
# or
scoop install just
```

### Verify

```bash
just --version
```

---

## 3. File placement

Put the `Justfile` at repo root, same level as:

* `manage.py`
* `pyproject.toml` / `Pipfile`
* `.env` (if you use it)

Example:

```
personal-assistant/
├─ Justfile
├─ manage.py
├─ config/
├─ apps/
└─ .env
```

---

## 4. Basic usage

### Show tasks

```bash
just
# or
just help
# or
just --list
```

### Run a task

```bash
just test
just runserver
just makemigrate
```

Just will stop on errors unless you explicitly chain things.

---

## 5. Commands-only quick reference

```
just
just help
just clean
just test
just coverage
just makemigrations
just migrate
just makemigrate
just runserver
just createuser
just shell
just delete_db
just resetdb
just seed
```

---

## 6. Task-by-task behavior

### `just clean`

Deletes:

* `__pycache__/`
* `.pytest_cache/`
* `htmlcov/`
* `*.pyc`
* `*.coverage`

Use when your environment feels “stale” or coverage is lying to you.

---

### `just test`

Runs:

```bash
python manage.py test
```

Use for normal Django unit testing.

---

### `just coverage`

Runs tests with coverage and generates both console + HTML reports:

* `coverage run manage.py test`
* `coverage report`
* `coverage html` → outputs `htmlcov/`

Open the HTML report:

```bash
# WSL/Linux
xdg-open htmlcov/index.html

# macOS
open htmlcov/index.html
```

---

### `just makemigrations`

Runs:

```bash
python manage.py makemigrations
```

Make new migration files after model changes.

---

### `just migrate`

Runs:

```bash
python manage.py migrate
```

Apply migrations to database.

---

### `just makemigrate`

Dependency recipe:

1. `makemigrations`
2. `migrate`

Use when you want “do the right DB thing” in one go after model changes.

---

### `just runserver`

Runs:

```bash
python manage.py runserver
```

Normal dev server.

---

### `just createuser`

Runs your custom management command:

```bash
python manage.py create_user
```

**Important:** The Justfile has `dotenv-load := true`, so `.env` values will be available automatically.
Make sure `.env` includes whatever `create_user` expects (username/email/password).

---

### `just shell`

Runs:

```bash
python manage.py shell
```

---

### `just delete_db`

Deletes sqlite DB:

```bash
rm -f db.sqlite3
```

Only safe if sqlite is what you’re using locally.

---

### `just resetdb`

Performs:

1. delete `db.sqlite3`
2. run `just makemigrate`
3. run `just createuser`

Use for “nuke it from orbit, rebuild clean.”

---

### `just seed`

Performs:

1. `makemigrations`
2. `migrate`
3. load fixture `plan_it/fixtures/demo_data.json`

Use when you want a known demo dataset.

---

## 7. Common workflows

### Fresh local setup

```bash
just makemigrate
just createuser
just seed
just runserver
```

---

### Daily dev loop

After editing models:

```bash
just makemigrate
```

Before commits:

```bash
just test
just coverage
```

---

### “DB is haunted” reset

```bash
just resetdb
just seed
```

---

## 8. Overriding Python (if you ever need to)

You defined variables:

```just
PYTHON := "python"
MANAGE := "{{PYTHON}} manage.py"
```

So you can override on the CLI:

```bash
just PYTHON=python3.12 test
just PYTHON=python3 makemigrate
```

That’s handy if you have multiple venvs or are testing a different interpreter.

---

## 9. WSL + Windows notes

Your Justfile uses:

```just
set shell := ["bash", "-cu"]
```

So recipes assume a bash-like shell:

* ✅ Works great in WSL (your default)
* ✅ Works in Linux/macOS
* ⚠️ On native Windows PowerShell/CMD it will fail unless you run inside Git Bash or WSL.

So: **run `just` inside WSL for this repo.**

---

## 10. Troubleshooting

**“just: recipe `xyz` not found”**

* You typoed the task name. Run `just --list`.

**`coverage: command not found`**

* Install in your venv:

```bash
pip install coverage
```

**`find: command not found`**

* You’re not in bash/WSL. Run inside WSL.

**`create_user` fails**

* Your `.env` is missing fields expected by the management command.
* Open `.env`, confirm values, retry:

```bash
just createuser
```

---

## 11. Extending the Justfile (tiny pattern)

Add a new recipe like:

```just
# Collect static files
collectstatic:
  {{MANAGE}} collectstatic --noinput
```

Then it automatically shows up in `just --list`.
