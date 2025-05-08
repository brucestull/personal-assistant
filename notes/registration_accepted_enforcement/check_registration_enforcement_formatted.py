import os
import ast
import json

PROJECT_ROOT = os.getcwd()
MIXIN_NAME = "RegistrationAcceptedMixin"
DECORATOR_NAME = "registration_accepted_required"

TXT_REPORT = "registration_enforcement_report.txt"
MD_REPORT = "registration_enforcement_report.md"
JSON_REPORT = "registration_enforcement_report.json"


def is_view_function(func_node):
    return bool(func_node.args.args) and func_node.args.args[0].arg == "request"


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
            if any("View" in name for name in base_names):
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
    results = {}

    for dirpath, _, filenames in os.walk(PROJECT_ROOT):
        for filename in filenames:
            if filename == "views.py":
                full_path = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(full_path, PROJECT_ROOT)

                cbv_inherits, cbv_missing, fbv_decorated, fbv_missing = analyze_views(
                    full_path
                )

                if any([cbv_inherits, cbv_missing, fbv_decorated, fbv_missing]):
                    results[rel_path] = {
                        "cbv_with_mixin": cbv_inherits,
                        "cbv_without_mixin": cbv_missing,
                        "fbv_with_decorator": fbv_decorated,
                        "fbv_without_decorator": fbv_missing,
                    }

    # TEXT Report
    with open(TXT_REPORT, "w", encoding="utf-8") as f:
        f.write("REGISTRATION ENFORCEMENT REPORT\n")
        f.write("=================================\n")
        for file, data in results.items():
            f.write(f"\nFile: {file}\n")
            if data["cbv_with_mixin"]:
                f.write(f"  ✅ CBVs with {MIXIN_NAME}:\n")
                for cls in data["cbv_with_mixin"]:
                    f.write(f"    - {cls}\n")
            if data["cbv_without_mixin"]:
                f.write(f"  ❌ CBVs MISSING {MIXIN_NAME}:\n")
                for cls in data["cbv_without_mixin"]:
                    f.write(f"    - {cls}\n")
            if data["fbv_with_decorator"]:
                f.write(f"  ✅ FBVs with @{DECORATOR_NAME}:\n")
                for fn in data["fbv_with_decorator"]:
                    f.write(f"    - {fn}\n")
            if data["fbv_without_decorator"]:
                f.write(f"  ❌ FBVs MISSING @{DECORATOR_NAME}:\n")
                for fn in data["fbv_without_decorator"]:
                    f.write(f"    - {fn}\n")

    # MARKDOWN Report
    with open(MD_REPORT, "w", encoding="utf-8") as f:
        f.write("# 📝 Registration Enforcement Report\n\n")
        for file, data in results.items():
            f.write(f"## `{file}`\n\n")
            if data["cbv_with_mixin"]:
                f.write(f"### ✅ CBVs with `{MIXIN_NAME}`\n")
                for cls in data["cbv_with_mixin"]:
                    f.write(f"- {cls}\n")
            if data["cbv_without_mixin"]:
                f.write(f"\n### ❌ CBVs MISSING `{MIXIN_NAME}`\n")
                for cls in data["cbv_without_mixin"]:
                    f.write(f"- {cls}\n")
            if data["fbv_with_decorator"]:
                f.write(f"\n### ✅ FBVs with `@{DECORATOR_NAME}`\n")
                for fn in data["fbv_with_decorator"]:
                    f.write(f"- {fn}\n")
            if data["fbv_without_decorator"]:
                f.write(f"\n### ❌ FBVs MISSING `@{DECORATOR_NAME}`\n")
                for fn in data["fbv_without_decorator"]:
                    f.write(f"- {fn}\n")
            f.write("\n---\n\n")

    # JSON Report
    with open(JSON_REPORT, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    print(f"Reports generated:\n- {TXT_REPORT}\n- {MD_REPORT}\n- {JSON_REPORT}")


if __name__ == "__main__":
    main()
