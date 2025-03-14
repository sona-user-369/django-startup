import subprocess

import re
import os


def generate_env_name(project_name):
    """
    Generates a virtual environment name from the project name.

    - Replaces spaces and special characters with underscores.
    - Converts to lowercase.
    - Truncates if necessary to keep the name short.

    :param project_name: Project name (str)
    :return: Formatted environment name (str)
    """
    # Remove special characters and replace spaces with underscores
    env_name = re.sub(r'[^a-zA-Z0-9]+', '_', project_name).lower()

    # Truncate the name if it exceeds 30 characters
    return env_name[:30]


def install_env(project_name):
    create_project_directory(project_name)

    # generate env name of the project
    env_name = f"{generate_env_name(project_name)}_env"

    env_path = os.path.join(project_name, env_name)
    env_path_bin = os.path.join(project_name, env_name, "bin")
    python_executable = os.path.join(env_path_bin, "python")

    # create and activate environment
    subprocess.check_call(["python3", "-m" "venv", env_path])

    django_package = "django"
    django_rest_package = "django-rest-framework"
    django_startup_package = "django-startup"

    subprocess.check_call([python_executable, "-m", "pip", "install", django_package, django_rest_package])


def create_project_directory(name):
    try:
        subprocess.check_call(["django-admin", "startproject", f"{name}"])
    except SystemExit:
        subprocess.check_call(["pip", "install", "django"])
        create_project_directory(name)
