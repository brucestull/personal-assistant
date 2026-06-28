# Compare Pytest and Django Unittest Coverage

## Commands used

### Pytest coverage

```bash
make coverage
coverage report
```

- `make coverage` runs: `coverage run -m pytest && coverage report && coverage html`
- In this environment, pytest had 4 failures (Redis connection in `true_north/tests/test_views.py`), so `coverage report` was run separately to read the generated data.
- Pytest result: **4 failed, 945 passed**
- Pytest coverage total: **95%** (`TOTAL 5078 stmts, 277 miss`)

### Django unittest coverage

```bash
make djcoverage
```

- `make djcoverage` runs: `coverage run manage.py test && coverage report && coverage html`
- Django unittest result: **698 passed**
- Django unittest coverage total: **81%** (`TOTAL 5059 stmts, 952 miss`)

## Recommendation: use Pytest or Django Unittest exclusively?

Do **not** switch to one framework exclusively yet.

Recommended near-term path:

1. Keep both runners available while fixing pytest environment parity (the Redis-dependent pytest failures).
2. Prefer pytest for day-to-day development after parity is fixed (better plugin ecosystem and richer test selection/reporting).
3. Re-measure coverage after pytest is fully green; then decide whether to retire direct `manage.py test` usage.
