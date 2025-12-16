# tests/test_admin_module_imports.py

def test_import_admin_modules_for_coverage():
    import inbox.admin  # noqa: F401
    import knowledge.admin  # noqa: F401
    import projects.admin  # noqa: F401
