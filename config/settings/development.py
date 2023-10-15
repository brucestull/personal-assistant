from config.settings.common import *  # noqa: F401


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# Create your own `SECRET_KEY` here for use in Development.
# This one is provided here for user to get the DjangoCustomUserStarter up and
# running quickly.
# Ideally, you would not run with `SECRET_KEY` exposed in development either.
# You can set a `SECRET_KEY` on you development computer system.
# Create a specific `SECRET_KEY` for development and use it in development
# only.
# Create a specific `SECRET_KEY` for production and use it in production only.

# Get `SECRET_KEY` (first method argument) from environment variable
# `SECRET_KEY`, if it exists, or use the default one (second method argument)
# provided here:
# If user has a `SECRET_KEY` set in their environment variable, it will be
# used.
# Otherwise, the default one provided here will be used.
