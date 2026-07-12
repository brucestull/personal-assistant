# Adding the `events` app to your repo

This bundle contains:

- `events/` — the Django app (known-good version, wired to work with your `main`)
- `install_events.py` — a script that does the three wiring edits for you
- `INSTALL_README.md` — this file

The app itself is unchanged from the version you already had. This bundle's job is
only to **drop it into `main` and wire it up correctly**, plus add the four Google
libraries your `main` Pipfile was missing. The code-review fixes (items 4–10) are
**not** included here — those come later, one reviewable change at a time.

---

## Steps (run in WSL)

**1. Unzip at your repo root** — the folder that contains `manage.py` and `config/`:

```bash
cd ~/path/to/personal-assistant
unzip ~/Downloads/events-app-install.zip
```

This drops `events/`, `install_events.py`, and this README next to `config/`.

**2. Run the installer** (idempotent — safe to run twice, backs up every file it edits):

```bash
python3 install_events.py
```

It makes exactly three edits:
- adds `"events.apps.EventsConfig"` to `INSTALLED_APPS` in `config/settings.py`
- adds `path("events/", include("events.urls"))` to `config/urls.py`
- adds the four Google libraries to `[packages]` in `Pipfile`

Originals are backed up to `<file>.bak.<timestamp>` right next to each file.

**3. Install deps and verify** — run these yourself and watch each one:

```bash
pipenv install                                              # installs Google libs + relocks
pipenv run python manage.py check                           # expect: no issues
pipenv run python manage.py makemigrations --check --dry-run  # events should show no changes
pipenv run python manage.py migrate                         # applies events/0001_initial
pipenv run python manage.py test events                     # expect: 17 tests OK
```

> Note: `makemigrations --check` may report drift in `app_tracker` and `thoughts`.
> That is pre-existing in your `main` and unrelated to `events` — safe to ignore for now.

**4. Clean up (optional):**

```bash
rm install_events.py INSTALL_README.md
```

---

## If something goes wrong

Every edited file has a `.bak.<timestamp>` copy beside it. To undo an edit:

```bash
cp config/settings.py.bak.<timestamp> config/settings.py
```

Nothing in this process touches git, so `git status` will simply show the new
`events/` folder and the three edited files whenever you're ready to commit.

## Still to come (not in this bundle)

Items 4–10 from the code review — the sync-duplication fix, OAuth hardening,
pagination, etc. — each delivered later as its own small, testable change.
