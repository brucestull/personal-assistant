from __future__ import annotations

import importlib
import inspect

from django.core import mail
from django.test import Client, TestCase

PYTEST_MODULES = [
    "thoughts.tests.test_models",
    "thoughts.tests.test_views",
    "warcrafting.tests.test_admin",
    "warcrafting.tests.test_forms",
    "warcrafting.tests.test_models",
    "warcrafting.tests.test_views",
    "vitals.tests.test_bp_summary",
    "true_north.tests.test_additional_tasks",
    "true_north.tests.test_admin",
    "true_north.tests.test_models",
    "true_north.tests.test_tasks",
    "true_north.tests.test_views",
]

_SUPPORTED_PARAMS = {"client", "mailoutbox"}
_SKIPPED_FUNCTIONS = {
    "true_north.tests.test_views.test_corevalue_send_email_queues_task",
    "true_north.tests.test_views.test_goal_send_email_queues_task",
    "true_north.tests.test_views.test_milestone_send_email_queues_task",
    "true_north.tests.test_views.test_valueaction_send_email_queues_task",
}


def _supports_params(params: list[str]) -> bool:
    return all(param in _SUPPORTED_PARAMS for param in params)


def _make_function_adapter(func, params: list[str]):
    def _test(self):
        kwargs = {}
        if "client" in params:
            kwargs["client"] = Client()
        if "mailoutbox" in params:
            if not hasattr(mail, "outbox"):
                mail.outbox = []
            mail.outbox.clear()
            kwargs["mailoutbox"] = mail.outbox
        func(**kwargs)

    _test.__name__ = func.__name__
    _test.__doc__ = f"Adapter for {func.__module__}.{func.__name__}"
    return _test


def _make_method_adapter(cls, method_name: str):
    def _test(self):
        getattr(cls(), method_name)()

    _test.__name__ = method_name
    _test.__doc__ = f"Adapter for {cls.__module__}.{cls.__name__}.{method_name}"
    return _test


class PytestCompatibilityTests(TestCase):
    """Run selected pytest-style tests under Django's unittest test runner."""


_counter = 0
for module_name in PYTEST_MODULES:
    module = importlib.import_module(module_name)

    for attr_name, obj in vars(module).items():
        if attr_name.startswith("test_") and inspect.isfunction(obj):
            fully_qualified_name = f"{module_name}.{attr_name}"
            if fully_qualified_name in _SKIPPED_FUNCTIONS:
                continue
            param_names = list(inspect.signature(obj).parameters)
            if _supports_params(param_names):
                _counter += 1
                setattr(
                    PytestCompatibilityTests,
                    f"test_pycompat_{_counter:04d}_{module_name.replace('.', '_')}_{attr_name}",
                    _make_function_adapter(obj, param_names),
                )

    for class_name, cls_obj in vars(module).items():
        if class_name.startswith("Test") and inspect.isclass(cls_obj):
            for method_name, method in vars(cls_obj).items():
                if method_name.startswith("test_") and inspect.isfunction(method):
                    param_names = list(inspect.signature(method).parameters)
                    if param_names == ["self"]:
                        _counter += 1
                        setattr(
                            PytestCompatibilityTests,
                            f"test_pycompat_{_counter:04d}_{module_name.replace('.', '_')}_{class_name}_{method_name}",
                            _make_method_adapter(cls_obj, method_name),
                        )
