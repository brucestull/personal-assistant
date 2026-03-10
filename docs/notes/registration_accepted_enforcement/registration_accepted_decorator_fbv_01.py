import os
import ast

PROJECT_ROOT = os.getcwd()
DECORATOR_NAME = "registration_accepted_required"
REPORT_FILE = "registration_accepted_decorator_report_01.txt"


def is_request_function(node):
    """Return True if the function has 'request' as its first argument."""
    if not isinstance(node, ast.FunctionDef):
        return False
    if not node.args.args:
        return False
    first_arg = node.args.args[0].arg
    return first_arg == "request"


def has_decorator(node, decorator_name):
    for decorator in node.decorator_list:
        # Handles both @decorator and @module.decorator
        if isinstance(decorator, ast.Name) and decorator.id == decorator_name:
            return True
        if isinstance(decorator, ast.Attribute) and decorator.attr == decorator_name:
            return True
    return False


def analyze_view_functions(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        tree = ast.parse(file.read(), filename=filepath)

    with_decorator = []
    without_decorator = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and is_request_function(node):
            if has_decorator(node, DECORATOR_NAME):
                with_decorator.append(node.name)
            else:
                without_decorator.append(node.name)

    return with_decorator, without_decorator


def main():
    with open(REPORT_FILE, "w", encoding="utf-8") as report:
        for dirpath, _, filenames in os.walk(PROJECT_ROOT):
            for filename in filenames:
                if filename == "views.py":
                    full_path = os.path.join(dirpath, filename)
                    with_decorator, without_decorator = analyze_view_functions(
                        full_path
                    )  # noqa E501

                    if with_decorator or without_decorator:
                        rel_path = os.path.relpath(full_path, PROJECT_ROOT)
                        report.write(f"\nFile: {rel_path}\n")
                        if with_decorator:
                            report.write(f"  Decorated with @{DECORATOR_NAME}:\n")
                            for fn in with_decorator:
                                report.write(f"    - {fn}\n")
                        if without_decorator:
                            report.write(f"  Missing @{DECORATOR_NAME}:\n")
                            for fn in without_decorator:
                                report.write(f"    - {fn}\n")
    print(f"Report generated: {REPORT_FILE}")


if __name__ == "__main__":
    main()
