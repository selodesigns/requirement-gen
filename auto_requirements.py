import os
import ast
import sys
from pathlib import Path

try:
    from stdlib_list import stdlib_list
    stdlib_modules = set(stdlib_list(sys.version[:3]))
except ImportError:

    import sysconfig
    stdlib_path = sysconfig.get_paths()["stdlib"]
    stdlib_modules = set(sys.builtin_module_names)
    stdlib_modules.update({
        'argparse', 'asyncio', 'atexit', 'base64', 'binascii', 'calendar', 'cmath', 'collections',
        'concurrent', 'contextlib', 'copy', 'csv', 'ctypes', 'datetime', 'decimal', 'difflib',
        'dis', 'email', 'enum', 'errno', 'faulthandler', 'filecmp', 'fileinput', 'fnmatch',
        'fractions', 'functools', 'gc', 'getopt', 'getpass', 'gettext', 'glob', 'gzip',
        'hashlib', 'heapq', 'hmac', 'html', 'http', 'imaplib', 'imghdr', 'imp', 'importlib',
        'inspect', 'io', 'ipaddress', 'itertools', 'json', 'keyword', 'linecache', 'locale',
        'logging', 'lzma', 'math', 'mimetypes', 'multiprocessing', 'numbers', 'operator',
        'os', 'pathlib', 'pickle', 'pkgutil', 'platform', 'plistlib', 'pprint', 'profile',
        'pstats', 'pty', 'pwd', 'pyclbr', 'pydoc', 'queue', 'random', 're', 'readline',
        'reprlib', 'sched', 'secrets', 'select', 'selectors', 'shlex', 'shutil', 'signal',
        'site', 'smtplib', 'socket', 'sqlite3', 'ssl', 'stat', 'statistics', 'string',
        'stringprep', 'struct', 'subprocess', 'sunau', 'symbol', 'symtable', 'sys',
        'sysconfig', 'tabnanny', 'tarfile', 'tempfile', 'textwrap', 'threading', 'time',
        'timeit', 'tkinter', 'token', 'tokenize', 'trace', 'traceback', 'tracemalloc',
        'tty', 'types', 'typing', 'unicodedata', 'unittest', 'urllib', 'uuid', 'venv',
        'warnings', 'wave', 'weakref', 'webbrowser', 'wsgiref', 'xdrlib', 'xml', 'xmlrpc',
        'zipapp', 'zipfile', 'zipimport', 'zlib'
    })

# Known PyPI package mappings for alias imports
known_package_aliases = {
    "PIL": "Pillow",
    "cv2": "opencv-python",
    "yaml": "PyYAML",
    "sklearn": "scikit-learn",
    "Image": "Pillow",
    "playsound": "playsound",
    "docx": "python-docx",
    "sentence_transformers": "sentence-transformers",
    "flask_socketio": "flask-socketio",
    "flask_cors": "flask-cors",
    "socketio": "python-socketio",
    "edge_tts": "edge-tts",
    "pygame": "pygame",
    "psutil": "psutil",
    "aiohttp": "aiohttp",
    "sounddevice": "sounddevice",
    "transformers": "transformers",
    "spacy": "spacy",
    "torch": "torch",
    "PyPDF2": "PyPDF2",
    "scipy": "scipy",
    "numpy": "numpy",
    "matplotlib": "matplotlib",
    "schedule": "schedule",
    "pytz": "pytz",
    "gevent": "gevent",
    "geventwebsocket": "gevent-websocket",
}

# Likely internal modules in user projects
likely_internal_modules = {
    "api", "config", "core", "self_learning_api", "selo_client", "selo_desktop", "utilities", "ui"
}
>>>>>>> 1170d0c (Add auto_requirements.py to generate clean requirements.txt)

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

<<<<<<< HEAD
def get_installed_versions():
    return {dist.metadata["Name"].lower(): dist.version for dist in distributions()}

=======
>>>>>>> 1170d0c (Add auto_requirements.py to generate clean requirements.txt)
def main(project_dir="."):
    all_imports = set()
    for py_file in find_python_files(project_dir):
        all_imports.update(extract_imports_from_file(py_file))

    third_party_imports = {
        imp for imp in all_imports
<<<<<<< HEAD
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
=======
        if imp not in stdlib_modules and imp not in likely_internal_modules and not imp.startswith('_')
    }

    resolved_packages = set()
    for imp in third_party_imports:
        resolved_packages.add(known_package_aliases.get(imp, imp))

    output_path = os.path.join(project_dir, "requirements.txt")
    with open(output_path, "w") as req_file:
        for pkg in sorted(resolved_packages):
            req_file.write(f"{pkg}\n")

    print("✅ requirements.txt created with likely third-party dependencies.")
    print("📦 Run this to install:")
    print("    pip install -r requirements.txt")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Scan Python project and generate cleaned requirements.txt")
>>>>>>> 1170d0c (Add auto_requirements.py to generate clean requirements.txt)
    parser.add_argument("project_dir", nargs="?", default=".", help="Project directory to scan")
    args = parser.parse_args()
    main(args.project_dir)
