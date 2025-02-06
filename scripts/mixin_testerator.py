import ast
import os

from dotenv import load_dotenv

# Loads variables from .env
load_dotenv()
MIXIN_TESTERATOR_PATH = os.environ.get("MIXIN_TESTERATOR_PATH", ".")


class ClassVisitor(ast.NodeVisitor):
    def __init__(self):
        self.class_names = []

    def visit_ClassDef(self, node):
        base_names = [base.id for base in node.bases if isinstance(base, ast.Name)]
        if "RegistrationAcceptedMixin" in base_names:
            self.class_names.append(node.name)


def is_django_view_file(filename):
    with open(filename, "r") as file:
        tree = ast.parse(file.read(), filename=filename)
        visitor = ClassVisitor()
        visitor.visit(tree)
        return bool(visitor.class_names), visitor.class_names


def check_project_for_mixin(root_dir):
    for subdir, dirs, files in os.walk(root_dir):
        for filename in files:
            filepath = os.path.join(subdir, filename)
            if filepath.endswith("views.py"):
                has_mixin, class_names = is_django_view_file(filepath)
                if has_mixin:
                    print(f"Found in {filepath}: {class_names}")
                else:
                    print(f"Mixin is missing in {filepath}")


if __name__ == "__main__":
    # Replace '/path/to/your/django/project' with the actual path to your Django
    # project directory
    check_project_for_mixin(MIXIN_TESTERATOR_PATH)
