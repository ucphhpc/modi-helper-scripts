import os
from modi_helper.utils.job import run


def delete_environment(name):
    command = ["conda", "remove", "--name", name, "--all"]
    return run(command, format_output_str=True)
