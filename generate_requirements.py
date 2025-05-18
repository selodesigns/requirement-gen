import os
import ast
import sys
from pathlib import Path
from importlib.metadata import distributions, PackageNotFoundError

# Built-in and standard library modules
try:
    from stdlib_list import stdlib_list
    stdlib_modules = set(stdlib_list(sys.version[:3]))
except ImportError:
    stdlib_modules = set(sys.builtin_module_names)  # fallback

def find_python_files(root_dir):
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                yield os.path.join(root, file)

def extract_imports_from_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read(), filename=filepath)
        except SyntaxError:
            return set()
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split('.')[0])
    return imports

def get_installed_versions():
    return {dist.metadata["Name"].lower(): dist.version for dist in distributions()}

def main(project_dir="."):
    all_imports = set()
    for py_file in find_python_files(project_dir):
        all_imports.update(extract_imports_from_file(py_file))

    third_party_imports = {
        imp for imp in all_imports
        if imp not in stdlib_modules and not imp.startswith('_')
    }

    installed_versions = get_installed_versions()
    requirements = []

    for module in sorted(third_party_imports):
        pkg_lower = module.lower()
        if pkg_lower in installed_versions:
            version = installed_versions[pkg_lower]
            requirements.append(f"{module}=={version}")
        else:
            print(f"⚠️ Warning: Package '{module}' is imported but not installed.")

    # Output
    with open("requirements.txt", "w") as req_file:
        req_file.write("\n".join(requirements))
    
    print("✅ requirements.txt generated successfully.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Auto-generate requirements.txt from Python project")
    parser.add_argument("project_dir", nargs="?", default=".", help="Project directory to scan")
    args = parser.parse_args()
    main(args.project_dir)
