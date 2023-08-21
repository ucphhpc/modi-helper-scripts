import os
from modi_helper.utils.job import run


def create_environment(name, destination=None, automatic_yes=False, quiet=False, extra_conda_args=None):
    if not extra_conda_args:
        extra_conda_args = []

    command = ["conda", "create"]
    if destination:
        command.extend(["-p", os.path.join(destination, name)])
    else:
        command.extend(["-n", name])

    if automatic_yes:
        command.extend(["-y"])
    
    if quiet:
        command.extend(["-q"])

    command.extend(extra_conda_args)
    return run(command, format_output_str=True)


def activate_environment(name):
    command = ["conda", "activate", name]
    return run(command, format_output_str=True)


def add_environment_directory(path):
    command = ["conda", "config", "--append", "envs_dirs", path]
    return run(command, format_output_str=True)
