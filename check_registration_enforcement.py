import os
import ast

PROJECT_ROOT = os.getcwd()
MIXIN_NAME = "RegistrationAcceptedMixin"
DECORATOR_NAME = "registration_accepted_required"
REPORT_FILE = "registration_enforcement_report.txt"


def is_view_function(func_node):
    if not func_node.args.args:
        return False
    return func_node.args.args[0].arg == "request"


def has_decorator(func_node, decorator_name):
    for decorator in func_node.decorator_list:
        if isinstance(decorator, ast.Name) and decorator.id == decorator_name:
            return True
        elif isinstance(decorator, ast.Attribute) and decorator.attr == decorator_name:
            return True
        elif isinstance(decorator, ast.Call):
            if (
                isinstance(decorator.func, ast.Name)
                and decorator.func.id == decorator_name
            ):
                return True
            elif (
                isinstance(decorator.func, ast.Attribute)
                and decorator.func.attr == decorator_name
            ):
                return True
    return False


def analyze_views(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=filepath)

    cbv_inherits = []
    cbv_missing = []
    fbv_decorated = []
    fbv_missing = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            base_names = [
                base.id if isinstance(base, ast.Name) else getattr(base, "attr", "")
                for base in node.bases
            ]
            if any("View" in name for name in base_names):  # likely CBV
                if MIXIN_NAME in base_names:
                    cbv_inherits.append(node.name)
                else:
                    cbv_missing.append(node.name)

        elif isinstance(node, ast.FunctionDef) and is_view_function(node):
            if has_decorator(node, DECORATOR_NAME):
                fbv_decorated.append(node.name)
            else:
                fbv_missing.append(node.name)

    return cbv_inherits, cbv_missing, fbv_decorated, fbv_missing


def main():
    with open(REPORT_FILE, "w", encoding="utf-8") as report:
        report.write("REGISTRATION ENFORCEMENT REPORT\n")
        report.write("=================================\n")

        for dirpath, _, filenames in os.walk(PROJECT_ROOT):
            for filename in filenames:
                if filename == "views.py":
                    full_path = os.path.join(dirpath, filename)
                    rel_path = os.path.relpath(full_path, PROJECT_ROOT)

                    cbv_inherits, cbv_missing, fbv_decorated, fbv_missing = (
                        analyze_views(full_path)
                    )

                    if any([cbv_inherits, cbv_missing, fbv_decorated, fbv_missing]):
                        report.write(f"\nFile: {rel_path}\n")

                        if cbv_inherits:
                            report.write(f"  ✅ CBVs with {MIXIN_NAME}:\n")
                            for cls in cbv_inherits:
                                report.write(f"    - {cls}\n")
                        if cbv_missing:
                            report.write(f"  ❌ CBVs MISSING {MIXIN_NAME}:\n")
                            for cls in cbv_missing:
                                report.write(f"    - {cls}\n")

                        if fbv_decorated:
                            report.write(f"  ✅ FBVs with @{DECORATOR_NAME}:\n")
                            for fn in fbv_decorated:
                                report.write(f"    - {fn}\n")
                        if fbv_missing:
                            report.write(f"  ❌ FBVs MISSING @{DECORATOR_NAME}:\n")
                            for fn in fbv_missing:
                                report.write(f"    - {fn}\n")

    print(f"Report generated: {REPORT_FILE}")


if __name__ == "__main__":
    main()
