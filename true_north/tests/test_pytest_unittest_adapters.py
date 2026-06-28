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
for _module_name in PYTEST_MODULES:
    _module = importlib.import_module(_module_name)

    for _attr_name, _obj in vars(_module).items():
        if _attr_name.startswith("test_") and inspect.isfunction(_obj):
            _fully_qualified_name = f"{_module_name}.{_attr_name}"
            if _fully_qualified_name in _SKIPPED_FUNCTIONS:
                continue
            _param_names = list(inspect.signature(_obj).parameters)
            if _supports_params(_param_names):
                _counter += 1
                _method_name = (
                    f"test_pycompat_{_counter:04d}"
                    f"_{_module_name.replace('.', '_')}_{_attr_name}"
                )
                setattr(
                    PytestCompatibilityTests,
                    _method_name,
                    _make_function_adapter(_obj, _param_names),
                )

    for _class_name, _cls_obj in vars(_module).items():
        if _class_name.startswith("Test") and inspect.isclass(_cls_obj):
            for _meth_name, _method in vars(_cls_obj).items():
                if _meth_name.startswith("test_") and inspect.isfunction(_method):
                    _param_names = list(inspect.signature(_method).parameters)
                    if _param_names == ["self"]:
                        _counter += 1
                        _method_name = (
                            f"test_pycompat_{_counter:04d}"
                            f"_{_module_name.replace('.', '_')}"
                            f"_{_class_name}_{_meth_name}"
                        )
                        setattr(
                            PytestCompatibilityTests,
                            _method_name,
                            _make_method_adapter(_cls_obj, _meth_name),
                        )