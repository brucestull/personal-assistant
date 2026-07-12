#!/usr/bin/env python3
"""
install_events.py  —  Wire the `events` app into the personal-assistant repo.

Run this from the ROOT of your repo (the folder containing manage.py and config/),
AFTER unzipping so that the `events/` folder sits next to config/.

    cd ~/path/to/personal-assistant
    unzip ~/Downloads/events-app-install.zip     # drops events/, this script, README
    python3 install_events.py

What it does (all idempotent — safe to run twice):
  1. Adds "events.apps.EventsConfig" to INSTALLED_APPS in config/settings.py
  2. Adds path("events/", include("events.urls")) to config/urls.py
  3. Adds the four Google client libraries to the [packages] section of Pipfile

Every file it edits is backed up first to <file>.bak.<timestamp>.
It changes nothing else and touches no git state.
"""

import re
import sys
import shutil
import datetime
from pathlib import Path

GOOGLE_PACKAGES = [
    'google-api-python-client = "==2.198.0"',
    'google-auth-oauthlib = "==1.4.0"',
    'google-auth = "==2.55.2"',
    'google-auth-httplib2 = "==0.4.0"',
]

STAMP = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")


def fail(msg):
    print(f"\n  ERROR: {msg}\n")
    sys.exit(1)


def backup(path: Path):
    dest = path.with_name(f"{path.name}.bak.{STAMP}")
    shutil.copy2(path, dest)
    print(f"    backed up -> {dest.name}")


def check_location():
    """Make sure we're in the repo root with the events app already unzipped."""
    required = ["manage.py", "config/settings.py", "config/urls.py", "Pipfile", "events/apps.py"]
    missing = [r for r in required if not Path(r).exists()]
    if missing:
        fail(
            "This must be run from the repo root, and the events/ folder must be "
            "unzipped here first.\n         Missing: " + ", ".join(missing)
        )
    print("  Location looks correct (found manage.py, config/, Pipfile, events/).")


def edit_installed_apps():
    path = Path("config/settings.py")
    text = path.read_text()
    if "events.apps.EventsConfig" in text:
        print("  [settings.py] events already in INSTALLED_APPS — skipping.")
        return
    # Find the INSTALLED_APPS = [ ... ] block and insert before its closing ].
    m = re.search(r"(INSTALLED_APPS\s*=\s*\[)(.*?)(\n\])", text, re.DOTALL)
    if not m:
        fail("Could not locate the INSTALLED_APPS list in config/settings.py. "
             "No changes made to this file; please add \"events.apps.EventsConfig\" by hand.")
    backup(path)
    insertion = '\n    "events.apps.EventsConfig",'
    new_text = text[:m.end(2)] + insertion + text[m.end(2):]
    path.write_text(new_text)
    print('  [settings.py] added "events.apps.EventsConfig" to INSTALLED_APPS.')


def edit_urls():
    path = Path("config/urls.py")
    text = path.read_text()
    if 'include("events.urls")' in text or "include('events.urls')" in text:
        print("  [urls.py] events include already present — skipping.")
        return
    # Prefer inserting right after the bus-drive include (known last entry); fall back
    # to inserting before the closing ] of urlpatterns.
    anchor = re.search(r'\n(\s*)path\(\s*"bus-drive/".*?\),', text, re.DOTALL)
    line = '    path("events/", include("events.urls")),'
    backup(path)
    if anchor:
        new_text = text[:anchor.end()] + "\n" + line + text[anchor.end():]
    else:
        m = re.search(r"(urlpatterns\s*=\s*\[)(.*?)(\n\])", text, re.DOTALL)
        if not m:
            fail("Could not locate urlpatterns in config/urls.py. Backup was made; "
                 "please add the events include by hand.")
        new_text = text[:m.end(2)] + "\n" + line + text[m.end(2):]
    path.write_text(new_text)
    print('  [urls.py] added path("events/", include("events.urls")).')


def edit_pipfile():
    path = Path("Pipfile")
    text = path.read_text()
    if "google-auth-oauthlib" in text:
        print("  [Pipfile] Google libraries already present — skipping.")
        return
    m = re.search(r"\n\[packages\]\n", text)
    if not m:
        fail("Could not find a [packages] section in Pipfile. Backup NOT made; "
             "please add the Google libraries by hand.")
    backup(path)
    block = "\n".join(GOOGLE_PACKAGES) + "\n"
    new_text = text[:m.end()] + block + text[m.end():]
    path.write_text(new_text)
    print("  [Pipfile] added the four Google client libraries to [packages].")


def main():
    print("\n=== Installing the events app into this repo ===\n")
    check_location()
    print()
    edit_installed_apps()
    edit_urls()
    edit_pipfile()
    print("\n=== Wiring complete. ===\n")
    print("Next steps (run these yourself and watch each one):\n")
    print("  1. Install the new dependencies and refresh the lock file:")
    print("       pipenv install")
    print("       # (this both installs the Google libs and regenerates Pipfile.lock)\n")
    print("  2. Confirm Django is happy with the project:")
    print("       pipenv run python manage.py check\n")
    print("  3. Confirm there is no migration drift, then apply the migration:")
    print("       pipenv run python manage.py makemigrations --check --dry-run")
    print("       pipenv run python manage.py migrate\n")
    print("  4. Run the events app's own tests:")
    print("       pipenv run python manage.py test events\n")
    print("If any step fails, the .bak.* backups next to each edited file let you")
    print("restore the original instantly. Nothing here touched git.\n")


if __name__ == "__main__":
    main()
