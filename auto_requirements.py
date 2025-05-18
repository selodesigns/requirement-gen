import os
import ast
import sys
import json
import datetime
import subprocess
from pathlib import Path
from importlib.metadata import distributions

# Built-in and standard library modules
try:
    from stdlib_list import stdlib_list
    # Use a compatible version as fallback since stdlib_list doesn't support Python 3.13 yet
    python_version = "3.11" if sys.version_info.major == 3 and sys.version_info.minor >= 12 else sys.version[:3]
    stdlib_modules = set(stdlib_list(python_version))
    print(f"Using stdlib_list for Python {python_version} (actual: {sys.version[:5]})")
except (ImportError, ValueError):
    import sysconfig
    stdlib_path = sysconfig.get_paths()["stdlib"]
    stdlib_modules = set(sys.builtin_module_names)
    print(f"Using basic standard library detection for Python {sys.version[:5]}")
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

# Additional Windows-specific standard library modules
if sys.platform == "win32":
    stdlib_modules.update(["winsound", "winreg"])

# Known PyPI package mappings for alias imports
known_package_aliases = {
    "PIL": "Pillow",
    "cv2": "opencv-python",
    "yaml": "PyYAML",
    "sklearn": "scikit-learn",
    "mx": "mxnet",
    "bs4": "beautifulsoup4",
    "cairo": "pycairo",
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

def check_package_compatibility(package_name, python_version=None):
    """Check if a package is compatible with the current or specified Python version"""
    if not python_version:
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    
    try:
        # Use pip to check available versions
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", f"{package_name}==", "--dry-run"],
            capture_output=True,
            text=True
        )
        
        # Check for Python compatibility errors
        if "No matching distribution found" in result.stderr:
            if f"Requires-Python" in result.stderr:
                return False, "Version compatibility issue with Python " + python_version
        return True, ""
    except Exception as e:
        return False, str(e)

def get_installed_versions():
    """Get versions of installed packages"""
    try:
        return {dist.metadata["Name"].lower(): dist.version for dist in distributions()}
    except Exception:
        print("Warning: Unable to get installed package versions")
        return {}

def main(project_dir="."):
    all_imports = set()
    for py_file in find_python_files(project_dir):
        all_imports.update(extract_imports_from_file(py_file))

    third_party_imports = {
        imp for imp in all_imports
        if imp not in stdlib_modules and imp not in likely_internal_modules and not imp.startswith('_')
    }
    
    # Map import names to package names
    mapped_packages = set()
    for import_name in third_party_imports:
        if import_name in known_package_aliases:
            mapped_packages.add(known_package_aliases[import_name])
        else:
            mapped_packages.add(import_name)

    resolved_packages = set()
    for imp in third_party_imports:
        resolved_packages.add(known_package_aliases.get(imp, imp))

    output_path = os.path.join(project_dir, "requirements.txt")
    
    # Get installed versions
    installed_versions = get_installed_versions()
    
    # Prepare requirements with compatibility checks
    requirements = []
    compatibility_notes = []
    
    for package in sorted(mapped_packages):
        # Check compatibility with current Python version
        is_compatible, reason = check_package_compatibility(package)
        
        # Add version if installed
        pkg_lower = package.lower()
        if pkg_lower in installed_versions:
            version = installed_versions[pkg_lower]
            if is_compatible:
                requirements.append(f"{package}=={version}")
            else:
                compatibility_notes.append(f"# {package}: {reason}")
                requirements.append(f"# {package}=={version}  # {reason}")
        else:
            if is_compatible:
                requirements.append(package)
            else:
                compatibility_notes.append(f"# {package}: {reason}")
                requirements.append(f"# {package}  # {reason}")
    
    # Write results to requirements.txt
    with open(output_path, 'w') as f:
        # Add compatibility notes at the top if any
        if compatibility_notes:
            f.write("# COMPATIBILITY NOTES:\n")
            for note in compatibility_notes:
                f.write(f"{note}\n")
            f.write("\n")
        
        # Write requirements
        f.write("\n".join(requirements))
    
    print(f"\nGenerated requirements.txt with {len(requirements)} packages")
    if compatibility_notes:
        print(f"Found {len(compatibility_notes)} packages with Python {sys.version_info.major}.{sys.version_info.minor} compatibility issues")
    print("📦 Run this to install:")
    print("    pip install -r requirements.txt")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Scan Python project and generate cleaned requirements.txt")
    parser.add_argument("project_dir", nargs="?", default=".", help="Project directory to scan")
    args = parser.parse_args()
    main(args.project_dir)
