import os
from modi_helper.utils.job import run


def create_environment(
    name, destination=None, automatic_yes=False, quiet=False, extra_conda_args=None
):
    command = ["conda", "create"]
    if extra_conda_args:
        if isinstance(extra_conda_args, (list, tuple, set)):
            command.extend(extra_conda_args)
        elif isinstance(extra_conda_args, str):
            extra_conda_args_list = extra_conda_args.split(" ")
            command.extend(extra_conda_args_list)

    if destination:
        command.extend(["-p", os.path.join(destination, name)])
    else:
        command.extend(["-n", name])

    if automatic_yes:
        command.extend(["-y"])

    if quiet:
        command.extend(["-q"])

    return run(command, format_output_str=True, capture_output=quiet)


def activate_environment(name):
    command = ["conda", "activate", name]
    return run(command, format_output_str=True)


def add_environment_directory(path):
    command = ["conda", "config", "--append", "envs_dirs", path]
    return run(command, format_output_str=True)
