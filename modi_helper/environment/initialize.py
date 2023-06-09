import os
from modi_helper.utils.job import run


def initialize_conda(quiet=False):
    conda_dir = os.getenv("CONDA_DIR", None)
    if not conda_dir:
        return (
            False,
            "The CONDA_DIR environment variable was not set, could not initialize conda",
        )

    # Source the conda script into the current shell
    command = ["conda", "init","--all"]
    if quiet:
        command.extend(["-q"])

    return True, run(command, format_output_str=True)
