import os
from utils.job import run


def initialize_conda():
    conda_dir = os.getenv("CONDA_DIR", None)
    if not conda_dir:
        return (
            False,
            "The CONDA_DIR environment variable was not set, could not initialize conda",
        )

    # Source the conda script into the current shell
    command = ["source", os.path.join(conda_dir, "etc", "profile.d", "conda.sh")]
    return True, run(command, shell=True, format_output_str=True)