import os
from setuptools import setup, find_packages

cur_dir = os.path.abspath(os.path.dirname(__file__))


def read(path):
    with open(path, "r") as _file:
        return _file.read()


def read_req(name):
    path = os.path.join(cur_dir, name)
    return [req.strip() for req in read(path).splitlines() if req.strip()]


version_ns = {}
with open(os.path.join(cur_dir, "version.py")) as f:
    exec(f.read(), {}, version_ns)


long_description = open("README.rst").read()
setup(
    name="modi-helper",
    version=version_ns["__version__"],
    description="A set of scripts and tools to help configure a MODI environment.",
    long_description=long_description,
    author="Rasmus Munk",
    author_email="munk1@live.dk",
    packages=find_packages(),
    package_data={"modi_helper": ["templates/*.j2"]},
    package_dir={"modi_helper": "modi_helper"},
    url="https://github.com/ucphhpc/modi-helper-scripts",
    keywords=[],
    install_requires=read_req("requirements.txt"),
    extras_require={
        "dev": read_req("requirements-dev.txt"),
    },
    entry_points={
        "console_scripts": [
            "modi-new-job=modi_helper.cli.job_submit:main",
            "modi-new-environment=modi_helper.cli.environment_new:main",
            "modi-delete-environment=modi_helper.cli.environment_delete:main",
            "modi-load-environments=modi_helper.cli.environments_load:main",
            "modi-list-environments=modi_helper.cli.environments_list:main",
        ]
    },
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
