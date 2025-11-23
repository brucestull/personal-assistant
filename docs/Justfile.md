## Justfile Runbook

### Commands Only
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

### Commands + Explanations

- `just`  
  Shows the task list (same as `just help`). This Justfile sets `default: help`.

- `just help`  
  Lists all available recipes with their names.

- `just clean`  
  Removes Python caches and test/coverage artifacts: `__pycache__`, `.pytest_cache`, `htmlcov`, `*.pyc`, `*.coverage`.  
  Use when your environment feels stale or coverage reports look wrong.

- `just test`  
  Runs Django unit tests via `python manage.py test`.

- `just coverage`  
  Runs Django tests with coverage, prints a console report, and generates an HTML report in `htmlcov/`.  
  Open report with:  
  - Linux/WSL: `xdg-open htmlcov/index.html`  
  - macOS: `open htmlcov/index.html`

- `just makemigrations`  
  Creates new migration files after model changes.

- `just migrate`  
  Applies migrations to your database.

- `just makemigrate`  
  Convenience combo: runs `makemigrations` then `migrate`.

- `just runserver`  
  Starts the Django dev server (`python manage.py runserver`).

- `just createuser`  
  Runs your custom management command `create_user`.  
  `.env` is auto-loaded by Justfile (`dotenv-load := true`), so your env values are available automatically.

- `just shell`  
  Opens a Django shell (`python manage.py shell`).

- `just delete_db`  
  Deletes the local sqlite database file `db.sqlite3`.  
  Use only if sqlite is your local DB.

- `just resetdb`  
  “Nuke and rebuild” flow: deletes `db.sqlite3`, runs `makemigrate`, then `createuser`.

- `just seed`  
  Rebuilds DB state and loads demo data from `plan_it/fixtures/demo_data.json`.

### Common Workflows

**Fresh local setup**
```

just makemigrate
just createuser
just seed
just runserver

```

**After changing models**
```

just makemigrate

```

**Before committing**
```

just test
just coverage

```

**DB reset**
```

just resetdb
just seed

```

### Notes

- Run these from the repo root (same folder as `manage.py`).
- Recipes assume bash (ideal for WSL/Linux/macOS). If you run native Windows PowerShell, use WSL or Git Bash.
- You can override the Python interpreter if needed:
  - `just PYTHON=python3.12 test`
  - `just PYTHON=python3 makemigrate`
