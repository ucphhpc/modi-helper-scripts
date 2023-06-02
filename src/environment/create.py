import os
from utils.job import run


def create_environment(name, destination=None):
    command = ["conda", "create"]
    if destination:
        command.extend(["-p", os.path.join(destination, name)])
    else:
        command.extend(["-n", name])
    return run(command, format_output_str=True)


def activate_environment(name):
    command = ["conda", "activate", name]
    return run(command, format_output_str=True)
