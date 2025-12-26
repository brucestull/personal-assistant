# config/settings/__init__.py
from __future__ import annotations

import os

env = os.getenv("ENVIRONMENT", "dev").lower().strip()

if env in {"prod", "production"}:
    from .prod import *  # noqa: F401,F403
elif env in {"test", "ci"}:
    from .test import *  # noqa: F401,F403
else:
    from .dev import *  # noqa: F401,F403
