import os
import json
from modi_helper.utils.job import run


def initialize_conda(quiet=False):
    conda_dir = os.getenv("CONDA_DIR", None)
    if not conda_dir:
        return (
            False,
            "The CONDA_DIR environment variable was not set, could not initialize conda",
        )

    # Source the conda script into the current shell
    command = ["conda", "init", "--all"]
    if quiet:
        command.extend(["-q"])
    return True, run(command, format_output_str=False, capture_output=quiet)


def get_environment_directories():
    command = ["conda", "config", "--get", "envs_dirs", "--json"]
    environment_dir_result = run(command, capture_output=True, format_output_str=True)
    if not environment_dir_result:
        print(
            "Failed to get the environment directories, result: {}".format(
                environment_dir_result
            )
        )
        return False, []

    if "error" in environment_dir_result and environment_dir_result["error"]:
        print(
            "Failed to get the environment directories, error: {}".format(
                environment_dir_result["error"]
            )
        )
        return False, []

    if (
        "returncode" in environment_dir_result
        and environment_dir_result["returncode"] != "0"
    ):
        print(
            "Failed to get the environment directories, returncode: {}".format(
                environment_dir_result["returncode"]
            )
        )
        return False, []

    if "output" not in environment_dir_result or not environment_dir_result["output"]:
        print(
            "Failed to get the environment directories, output: {}".format(
                environment_dir_result["output"]
            )
        )
        return False, []

    json_output = json.loads(environment_dir_result["output"])
    if "envs_dirs" not in json_output:
        return True, {}

    environment_directories = json_output["get"]["envs_dirs"]
    return True, environment_directories
