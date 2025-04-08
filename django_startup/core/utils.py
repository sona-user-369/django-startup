import secrets
import string
import subprocess

import re
import os

import click

from django_startup.core.operations import (
    change_variable_value, create_env_file, add_variable_value)


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

    # modify settings
    modify_settings(project_name)

    # add .env file

    django_package = "django"
    django_rest_package = "django-rest-framework"
    decouple_package = "python-decouple"
    django_startup_package = "django-startup"

    subprocess.check_call([
        python_executable, "-m", "pip", "install",
        django_package,
        django_rest_package,
        decouple_package
    ])

    create_authentication_app(project_name)


def create_project_directory(name):
    """Create the project with django-admin startproject."""
    try:
        subprocess.check_call(["django-admin", "startproject", f"{name}"])
    except SystemExit:
        subprocess.check_call(["pip", "install", "django"])
        create_project_directory(name)


def generate_secret_key(length=50):
    """Generate a random Django SECRET_KEY."""
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))


def modify_settings(project_name):
    """Modify settings.py file and set .env file for settings variables such as
    SECRET_KEY, DEBUG, ALLOWED_HOSTS, INSTALLED_APPS, AUTH_USER_MODEL,
    STATIC_ROOT, and STATIC_URL, STATICFILES_DIRS, LOGGING. """
    # get settings file path
    file_path = os.path.join(project_name, project_name, "settings.py")
    click.echo(f"Modifying settings file at {file_path}")

    # Import decouple package for getting variables from .env file

    with open(file_path, "r") as f:
        content = f.readlines()

    content.insert(0, "from decouple import config\n")

    with open(file_path, "w") as f:
        f.writelines(content)

    env_data = {
        "SECRET_KEY": generate_secret_key(),
        "DEBUG": "True",
        "ALLOWED_HOSTS": ["*"]
    }

    create_env_file(project_name, env_data)

    # Change SECRET_KEY
    change_variable_value("SECRET_KEY", "config('SECRET_KEY')", file_path, with_quote=False)
    # Change DEBUG
    change_variable_value("DEBUG", "config('DEBUG')", file_path, with_quote=False)
    # Change ALLOWED_HOSTS
    change_variable_value("ALLOWED_HOSTS", "config('ALLOWED_HOSTS')", file_path, with_quote=False)
    # Change INSTALLED_APPS
    change_variable_value("INSTALLED_APPS", ["rest_framework", "rest_framework.authtoken"],
                          file_path, type_variable='list')


def create_authentication_app(project_name):
    file_path = os.path.join(project_name)

    authentication_dir = os.path.join(project_name, 'authentication')

    subprocess.run(["mkdir", "-p", authentication_dir], check=True)

    settings_path = os.path.join(project_name, project_name, "settings.py")

    click.echo(f"Creating authentication app at {authentication_dir}")

    subprocess.check_call(["django-admin", "startapp", "authentication", authentication_dir])

    change_variable_value("INSTALLED_APPS", "authentication",
                          settings_path, type_variable='list')

    # creating user in authentication app

    models_file = os.path.join(project_name, "authentication", "models.py")

    with open(models_file, "r") as f:
        content = f.read()

    # Ensure 'from django.db import models' and 'from django.contrib.auth.models import AbstractUser' exists
    content = "from django.db import models\n" + content
    content = "from django.contrib.auth.models import AbstractUser\n" + content
    content = "import uuid\n" + content

    model_code = f"""class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    profile_picture	= models.TextField(null=True, blank=True)
    role = models.CharField(max_length=100,null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=100,null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=200,null=True, blank=True)
    two_factor_enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    """

    # Append model code at end
    content = content.rstrip()  # Remove trailing spaces/new lines
    content += "\n" + model_code.lstrip()  # Ensure proper alignment

    # Write back to models.py
    with open(models_file, "w") as f:
        f.write(content)

    add_variable_value("AUTH_USER_MODEL", "authentication.User", settings_path)

