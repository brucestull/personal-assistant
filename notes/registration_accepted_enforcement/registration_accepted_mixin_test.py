import os
import ast

PROJECT_ROOT = os.getcwd()
MIXIN_NAME = "RegistrationAcceptedMixin"
REPORT_FILE = "registration_accepted_mixin_report.txt"


def analyze_view_classes(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        tree = ast.parse(file.read(), filename=filepath)

    inherits_mixin = []
    does_not_inherit = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            base_names = [
                base.id if isinstance(base, ast.Name) else getattr(base, "attr", "")
                for base in node.bases
            ]  # noqa: E501
            if any("View" in name for name in base_names):  # likely a CBV
                if MIXIN_NAME in base_names:
                    inherits_mixin.append(node.name)
                else:
                    does_not_inherit.append(node.name)
    return inherits_mixin, does_not_inherit


def main():
    with open(REPORT_FILE, "w", encoding="utf-8") as report:
        for dirpath, _, filenames in os.walk(PROJECT_ROOT):
            for filename in filenames:
                if filename == "views.py":
                    full_path = os.path.join(dirpath, filename)
                    inherits, does_not = analyze_view_classes(full_path)

                    if inherits or does_not:
                        rel_path = os.path.relpath(full_path, PROJECT_ROOT)
                        report.write(f"\nFile: {rel_path}\n")
                        if inherits:
                            report.write(f"  Inherits {MIXIN_NAME}:\n")
                            for cls in inherits:
                                report.write(f"    - {cls}\n")
                        if does_not:
                            report.write(f"  Does NOT inherit {MIXIN_NAME}:\n")
                            for cls in does_not:
                                report.write(f"    - {cls}\n")
    print(f"Report generated: {REPORT_FILE}")


if __name__ == "__main__":
    main()
