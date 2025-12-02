# RUNBOOK – Time-Based Dyno Scaling with Heroku Scheduler

## 1. Purpose

This runbook describes how to:

* Use **Heroku Scheduler** plus a small helper script (`heroku_scale.py`)
* To **automatically scale web dynos up and down** at specific times of day.

Example schedule used here (America/New_York):

* **Start app** every day at **06:00**
* **Stop app** every day at **08:00**

You can adjust times later as needed.

---

## 2. Overview of Approach

* A script named **`heroku_scale.py`** is already present in the repo root.

* This script calls the **Heroku Platform API** and sets the dyno quantity (e.g., `web=1` or `web=0`).

* The **Procfile** exposes two process types:

  * `scale_up` → runs `python heroku_scale.py up`
  * `scale_down` → runs `python heroku_scale.py down`

* **Heroku Scheduler** is configured to run these processes at the desired times (in UTC).

---

## 3. Prerequisites

* You have a working Heroku app (e.g., **Personal Assistant**).
* Git remote is set (`heroku` remote points to the correct app).
* `heroku_scale.py` exists in the **repo root** and is committed.
* You can log in to:

  * Heroku Dashboard in a browser
  * Heroku CLI (optional, but helpful):

    ```bash
    heroku login
    ```

---

## 4. Confirm Script & Procfile

### 4.1 Verify `heroku_scale.py`

* Location: **repo root** (same level as `Procfile` and `manage.py`).
* Purpose (high-level description to keep in mind):

  * Reads config vars such as `HEROKU_API_KEY`, `HEROKU_APP_NAME`, and dyno quantity settings.
  * Makes a **PATCH** request to the Heroku Formation API endpoint to set the dyno quantity for a given process type (usually `web`).
  * Supports two modes via CLI arguments:

    * `up` → sets dyno quantity to the “up” value
    * `down` → sets dyno quantity to the “down” value

> **Best practice note:** treat `heroku_scale.py` as an **infra/ops helper**, not part of the Django app. It should remain small, logged sensibly, and not import from project code if it doesn’t have to. Changes to this script should be reviewed like any other deployment/infra change.

### 4.2 Update `Procfile`

In the repo root, ensure `Procfile` contains **both** the app processes and the scaling processes:

```Procfile
web: gunicorn config.wsgi
release: python manage.py migrate accounts && python manage.py migrate
worker: celery -A config worker --beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler

scale_up: python heroku_scale.py up
scale_down: python heroku_scale.py down
```

Deploy any changes:

```bash
git add Procfile
git commit -m "Add scale_up and scale_down processes"
git push heroku main    # or 'master' depending on the branch in use
```

---

## 5. Configure Heroku Config Vars

1. In the Heroku Dashboard, open the app (e.g., **Personal Assistant**).
2. Go to **Settings → Config Vars → Reveal Config Vars**.
3. Add or confirm the following vars:

   * `HEROKU_API_KEY`

     * Value: your Heroku account API key

       * From Dashboard: click your avatar → **Account Settings** → **API Key**.
   * `HEROKU_APP_NAME`

     * Value: your app name exactly as shown (e.g., `personal-assistant`).
   * `DYNO_PROCESS_TYPE`

     * Value: `web`

       * (Change only if you want to scale a different process type.)
   * `DYNO_QTY_UP`

     * Value: `1` (or `2`, etc., if you ever need more than one dyno).
   * `DYNO_QTY_DOWN`

     * Value: `0` (turns the web dynos off).

Optional (for logging/diagnostics, if supported by script):

* `LOG_LEVEL` or similar, if the script reads it.

---

## 6. Add the Heroku Scheduler Add-on

If Heroku Scheduler is not already on the app:

1. In the app’s **Resources** tab:

   * Under **Add-ons**, search for **Heroku Scheduler**.
   * Choose **Standard – Free**.
   * Click **Submit Order Form**.

This provisions Scheduler on the app.

---

## 7. Create Scheduler Jobs for Daily Scaling

> **Important:** Heroku Scheduler uses **UTC**.
> You are in **America/New_York (UTC-5 in standard time)**.

Target times (local):

* **Start app at 06:00 Eastern → 11:00 UTC**
* **Stop app at 08:00 Eastern → 13:00 UTC**

### 7.1 Create “Scale Up” Job

1. From the app’s **Resources** tab, click **Heroku Scheduler**.

2. Click **Add Job**.

3. In the **Run Command** field, enter:

   ```bash
   python heroku_scale.py up
   ```

4. Set:

   * Frequency: **Daily**
   * Next due: **11:00** (UTC)

5. Save the job.

### 7.2 Create “Scale Down” Job

1. Click **Add Job** again.

2. In the **Run Command** field, enter:

   ```bash
   python heroku_scale.py down
   ```

3. Set:

   * Frequency: **Daily**
   * Next due: **13:00** (UTC)

4. Save the job.

> ✅ Result: Each day, Heroku Scheduler will:
>
> * At **11:00 UTC** → run `python heroku_scale.py up` → set `web` dynos to `DYNO_QTY_UP`.
> * At **13:00 UTC** → run `python heroku_scale.py down` → set `web` dynos to `DYNO_QTY_DOWN`.

### 7.3 DST Note

* When Eastern switches to **Daylight Saving Time (UTC-4)**:

  * 11:00 UTC = 07:00 local
  * 13:00 UTC = 09:00 local
* If you want to **keep 06:00–08:00 local year-round**, adjust the Scheduler job times when the time changes:

  * During DST, change jobs to:

    * Scale up at **10:00 UTC** (06:00 EDT)
    * Scale down at **12:00 UTC** (08:00 EDT)

---

## 8. Verifying Operation

### 8.1 Manual Test (Recommended Once)

From your local machine (or any shell with Heroku CLI):

```bash
heroku run python heroku_scale.py up   --app <your-app-name>
heroku ps                              --app <your-app-name>
```

Check that:

* `web.1` (or more) shows up and is **up**.

Then:

```bash
heroku run python heroku_scale.py down --app <your-app-name>
heroku ps                              --app <your-app-name>
```

Check that:

* `web` dynos are now **stopped** (no running web processes).

### 8.2 Check Scheduler History

In the **Heroku Scheduler** UI:

* Each job shows the **Last Run** and **Next Run** times.
* If a job failed, click it to view logs.

You can also check app logs:

```bash
heroku logs --tail --app <your-app-name>
```

Look for messages printed by `heroku_scale.py` confirming the new dyno quantity.

---

## 9. Using the Feature (Day-to-Day)

* **Normal case**: Do nothing; Scheduler will:

  * Turn the app **on** at 06:00 Eastern.
  * Turn the app **off** at 08:00 Eastern.
* **Temporarily keep it running longer**:

  * Manually scale via CLI:

    ```bash
    heroku ps:scale web=1 --app <your-app-name>
    ```
  * The next scheduled **down** job will still run at its usual time unless you disable or edit it.
* **Temporarily disable automation**:

  * In Scheduler, uncheck or delete the `scale_up` and/or `scale_down` jobs.

---

## 10. Advanced Options (Optional)

* **Multiple windows per day**

  * You can create additional jobs:

    * e.g., another `scale_up` at 16:00 UTC and `scale_down` at 20:00 UTC.
* **Weekday-only behavior**

  * Keep Scheduler jobs daily, but modify `heroku_scale.py` to:

    * Check the current weekday.
    * Exit without scaling on Saturday/Sunday (or whatever days you choose).
* **Different dyno quantities**

  * Adjust `DYNO_QTY_UP` if you ever need more than one web dyno during busy windows.

---

## 11. Troubleshooting

* **Script exits with “Missing HEROKU_API_KEY or HEROKU_APP_NAME”**

  * Confirm both config vars exist and are spelled correctly.
* **Dyno count doesn’t change**

  * Check that:

    * Scheduler job actually ran (check job history).
    * `DYNO_PROCESS_TYPE` matches the process type you want to scale (`web` vs `worker`).
* **“Unauthorized” or 401 errors from Heroku API**

  * Regenerate API key from Heroku account settings and update `HEROKU_API_KEY` config var.
* **Times are off by an hour**

  * Confirm UTC vs local time and whether you’re in standard vs daylight time.
  * Adjust Scheduler job times if needed.

---
