# Email Settings

```python
CONSOLE_EMAIL = os.getenv("CONSOLE_EMAIL")

# Settings determined by `ENVIRONMENT` value:
if ENVIRONMENT == "production":
    # ...
else:
    # Email sending settings:
    if CONSOLE_EMAIL:
        EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    else:
        # EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
        load_dotenv(".env.email")
        EMAIL_HOST = os.getenv("EMAIL_HOST")
        EMAIL_PORT = os.getenv("EMAIL_PORT")
        EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
        EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
        EMAIL_USE_TLS = True

    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_PORT = os.getenv("EMAIL_PORT")
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
    EMAIL_USE_TLS = True
```
