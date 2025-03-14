from setuptools import setup, find_packages

setup(
    name="django_startup",
    version="0.1.0",
    author="Donatien Davakan",
    author_email="donadavak@gmail.com",
    description="A librairy for Django startup",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sona-user-369/django_startup",
    packages=find_packages(),
    install_requires=["click"],  # Ajoute click comme dépendance
    entry_points={
        "console_scripts": [
            "djs=django_startup.core.cmdcore:django_startup",  # Associe la commande CLI
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
