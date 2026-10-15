
#!/usr/bin/env python3

"""
PDF Merger - Bootstrap

Automatically:
1. Checks Python version
2. Creates a virtual environment
3. Installs dependencies
4. Verifies dependencies
5. Launches the Streamlit application

Usage:
    python3 bootstrap.py
"""

import os
import subprocess
import sys
import venv
from pathlib import Path


# ---------------------------------------
# Configuration
# ---------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent
VENV_DIR = PROJECT_DIR / ".venv"
REQUIREMENTS = PROJECT_DIR / "requirements.txt"
APP_FILE = PROJECT_DIR / "app.py"

REQUIRED_MODULES = [
    "streamlit",
    "pypdf",
    "PIL",
]


# ---------------------------------------
# Helpers
# ---------------------------------------

def log(message):
    print(f"\n[PDF Merger] {message}", flush=True)


def run_command(command):
    subprocess.run(
        command,
        cwd=PROJECT_DIR,
        check=True
    )


def get_venv_python():
    if os.name == "nt":
        return VENV_DIR / "Scripts" / "python.exe"

    return VENV_DIR / "bin" / "python"


# ---------------------------------------
# Python Version Check
# ---------------------------------------

def check_python():

    log("Checking Python version...")

    if sys.version_info < (3, 10):
        raise RuntimeError(
            "Python 3.10 or newer is required."
        )

    print(
        f"Python version: "
        f"{sys.version_info.major}."
        f"{sys.version_info.minor}."
        f"{sys.version_info.micro}"
    )


# ---------------------------------------
# Create Virtual Environment
# ---------------------------------------

def create_environment():

    python_path = get_venv_python()

    if python_path.is_file():
        log("Existing virtual environment found.")
        return python_path

    log("Creating virtual environment...")

    venv.create(
        VENV_DIR,
        with_pip=True
    )

    if not python_path.is_file():
        raise RuntimeError(
            "Virtual environment creation failed."
        )

    log("Virtual environment created successfully.")

    return python_path


# ---------------------------------------
# Install Dependencies
# ---------------------------------------

def install_dependencies(python_path):

    if not REQUIREMENTS.is_file():
        raise FileNotFoundError(
            f"Missing requirements file: {REQUIREMENTS}"
        )

    log("Installing required Python libraries...")

    run_command([
        str(python_path),
        "-m",
        "pip",
        "install",
        "-r",
        str(REQUIREMENTS)
    ])

    log("Library installation completed.")


# ---------------------------------------
# Verify Libraries
# ---------------------------------------

def verify_libraries(python_path):

    log("Verifying installed libraries...")

    import_script = "\n".join(
        f"import {module}"
        for module in REQUIRED_MODULES
    )

    run_command([
        str(python_path),
        "-c",
        import_script
    ])

    log("All required libraries are available.")


# ---------------------------------------
# Launch Streamlit
# ---------------------------------------

def launch_app(python_path):

    if not APP_FILE.is_file():
        raise FileNotFoundError(
            f"Missing application file: {APP_FILE}"
        )

    log("Starting PDF Merger application...")

    print("\nOpen your browser at:")
    print("http://localhost:8501")
    print("\nPress Ctrl+C to stop the application.\n")

    run_command([
        str(python_path),
        "-m",
        "streamlit",
        "run",
        str(APP_FILE),
        "--server.address=localhost"
    ])


# ---------------------------------------
# Main
# ---------------------------------------

def main():

    print("=" * 48)
    print("          PDF MERGER BOOTSTRAP")
    print("=" * 48)

    try:

        check_python()

        python_path = create_environment()

        install_dependencies(python_path)

        verify_libraries(python_path)

        launch_app(python_path)

    except KeyboardInterrupt:
        log("Application stopped.")

    except subprocess.CalledProcessError as error:
        log(
            f"Command failed with exit code "
            f"{error.returncode}"
        )
        sys.exit(1)

    except Exception as error:
        log(f"Setup failed: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()