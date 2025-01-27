import sys
import subprocess
import pkg_resources  # For checking installed packages


def check_python_version():
    """Ensure Python 3 is being used."""
    if sys.version_info.major < 3:
        print("Error: Python 3 is required to run this script. Please install Python 3.")
        sys.exit(1)


def is_package_installed(package_name):
    """Check if a package is already installed."""
    try:
        pkg_resources.get_distribution(package_name)
        return True
    except pkg_resources.DistributionNotFound:
        return False


def install_packages():
    """Install packages from requirements.txt, skipping already installed packages."""
    with open("requirements.txt", "r") as f:
        packages = f.read().splitlines()

    for package in packages:
        package_name = package.split("==")[0]  # Extract the package name if version is specified
        if is_package_installed(package_name):
            print(f"Skipping {package_name}: already installed.")
        else:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])


if __name__ == "__main__":
    check_python_version()
    install_packages()
