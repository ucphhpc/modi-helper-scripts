from modi_helper.utils.job import run


def delete_environment(name, automatic_yes=False, quiet=False):
    command = ["conda", "remove", "--name", name, "--all"]

    if automatic_yes:
        command.extend(["-y"])

    if quiet:
        command.extend(["-q"])

    return run(command, format_output_str=True, capture_output=quiet)
