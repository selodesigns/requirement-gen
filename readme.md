# Auto Requirements Generator

> 🔍 Analyze a Python project directory and auto-generate an accurate `requirements.txt` file based on real imports and installed packages.

## 📦 Overview

This tool scans all `.py` files in a given directory, extracts imported modules using Python's AST, filters out standard library modules, and then matches third-party packages to their installed versions using `importlib.metadata`.

It’s especially useful when:
- You forgot to track dependencies manually
- You're retrofitting a project with proper packaging
- You want a clean `requirements.txt` for deployment or sharing

## 🚀 Features

- 🧠 AST-based static import analysis (no code execution required)
- ✅ Filters out standard library modules intelligently
- 📄 Outputs an accurate `requirements.txt` with pinned versions
- 🔁 Works recursively across all subfolders

## 🧰 Dependencies

### Required

- Python 3.8+
- [`importlib.metadata`](https://docs.python.org/3/library/importlib.metadata.html) (included in Python 3.8+)

### Optional

- [`stdlib-list`](https://pypi.org/project/stdlib-list/): Used for more accurate detection of standard library modules.

Install with:

```bash
pip install stdlib-list

## 🛠️ Usage

```bash
# Basic usage (in current folder)
python auto_requirements.py

# Specify a directory
python auto_requirements.py path/to/project
