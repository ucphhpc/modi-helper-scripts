import os
from modi_helper.utils.job import run


def create_environment(name, destination=None, automatic_yes=False):
    command = ["conda", "create"]
    if destination:
        command.extend(["-p", os.path.join(destination, name)])
    else:
        command.extend(["-n", name])

    if automatic_yes:
        command.extend(["-y"])

    return run(command, format_output_str=True)


def activate_environment(name):
    command = ["conda", "activate", name]
    return run(command, format_output_str=True)


def add_environment_directory(path):
    command = ["conda", "config", "--append", "envs_dirs", path]
    return run(command, format_output_str=True)
