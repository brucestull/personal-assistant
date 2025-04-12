# Mailgun Setup

- [Django Mailgun Integration](https://chatgpt.com/share/67f83ec9-0f24-8002-93d1-846c3dd0c002)

To use **Mailgun** to send emails from your **Django app**, you need to update your Django settings and optionally install a library to make integration easier. Here’s a simple step-by-step guide:

---

## ✅ 1. Create a Mailgun Account

1. Go to [https://www.mailgun.com/](https://www.mailgun.com/)
2. Sign up and verify your domain.
3. Get your Mailgun **API key**, **domain name**, and optionally **SMTP credentials**.

---

## ✅ 2. Install Required Package (Optional but recommended)

You can send emails via Mailgun using SMTP (built into Django) or the Mailgun API (via a package like `django-anymail`).

### 📦 Using the Mailgun API (Recommended)

```bash
pip install django-anymail
```

---

## ✅ 3. Update `settings.py`

### Add Anymail to Installed Apps
```python
INSTALLED_APPS = [
    ...
    "anymail",
]
```

### Configure Anymail with Mailgun
```python
# settings.py

EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
ANYMAIL = {
    "MAILGUN_API_KEY": "your-mailgun-api-key",
    "MAILGUN_SENDER_DOMAIN": "your-mailgun-domain",  # e.g. "mg.example.com"
}

DEFAULT_FROM_EMAIL = "Your Name <you@yourdomain.com>"
```

> **Tip:** Keep API keys secure using environment variables. For example:
```python
import os

ANYMAIL = {
    "MAILGUN_API_KEY": os.environ.get("MAILGUN_API_KEY"),
    "MAILGUN_SENDER_DOMAIN": os.environ.get("MAILGUN_DOMAIN"),
}
```

---

## ✅ 4. Test Email Sending

You can test sending an email in Django shell:

```bash
python manage.py shell
```

```python
from django.core.mail import send_mail

send_mail(
    "Hello from Mailgun",
    "This is a test email sent using Mailgun.",
    "you@yourdomain.com",  # From
    ["recipient@example.com"],  # To
)
```

---

## ✅ Alternative: Use SMTP

If you'd rather not use the API, you can use Mailgun’s SMTP:

```python
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.mailgun.org"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "postmaster@yourdomain.com"
EMAIL_HOST_PASSWORD = "your-smtp-password"
DEFAULT_FROM_EMAIL = "you@yourdomain.com"
```

---

Want me to help you write out a `.env` file and configure Django to load it?
