import subprocess
import sys

# List of required packages
required_packages = [
    "tkinter",  # GUI library for client
]

def install_package(package):
    """Install a Python package using pip."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_and_install():
    """Check and install required packages."""
    for package in required_packages:
        try:
            __import__(package)
            print(f"{package} is already installed.")
        except ImportError:
            print(f"{package} not found. Installing...")
            install_package(package)

if __name__ == "__main__":
    check_and_install()
