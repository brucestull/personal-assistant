# config/utils.py
from __future__ import annotations

from typing import Any
from urllib.parse import parse_qs, unquote, urlparse


def get_database_config_variables(database_url: str) -> dict[str, Any]:
    """
    Parse a DATABASE_URL into a dictionary of config values.

    Supports:
    - postgres://... and postgresql://...
    - query string params (e.g. ?sslmode=require)
    - percent-encoded credentials
    - IPv6 hosts

    Returns keys compatible with your existing usage:
      DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT, DATABASE_NAME
    And may also include:
      OPTIONS (dict)  -> e.g. {"sslmode": ["require"]}
    """
    if not database_url:
        raise ValueError("database_url is required")

    parsed = urlparse(database_url)

    if parsed.scheme not in {"postgres", "postgresql"}:
        raise ValueError(f"Unsupported database scheme: {parsed.scheme!r}")

    # urlparse splits these safely even if user/pass contain special chars (when encoded)
    user = unquote(parsed.username or "")
    password = unquote(parsed.password or "")
    host = parsed.hostname or ""
    port = str(parsed.port or "5432")

    # path is like "/dbname"
    dbname = (parsed.path or "").lstrip("/")
    if not dbname:
        raise ValueError("DATABASE_URL is missing database name")

    query = parse_qs(parsed.query)  # values are lists (e.g. {"sslmode": ["require"]})

    result: dict[str, Any] = {
        "DATABASE_USER": user,
        "DATABASE_PASSWORD": password,
        "DATABASE_HOST": host,
        "DATABASE_PORT": port,
        "DATABASE_NAME": dbname,
    }

    # Only attach OPTIONS if present (keeps old consumers happy)
    if query:
        result["OPTIONS"] = query

    return result
