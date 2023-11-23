import os
import json
from modi_helper.utils.job import run


def list_environments(extra_conda_args=None):
    command = ["conda", "env", "list", "--json"]
    if extra_conda_args:
        if isinstance(extra_conda_args, (list, tuple, set)):
            command.extend(extra_conda_args)
        elif isinstance(extra_conda_args, str):
            extra_conda_args_list = extra_conda_args.split(" ")
            command.extend(extra_conda_args_list)

    environment_results = run(command, format_output_str=True, capture_output=True)
    if not environment_results:
        return False, []

    if "error" in environment_results and environment_results["error"]:
        print(
            "Failed to list the environments, error: {}".format(
                environment_results["error"]
            )
        )
        return False, []

    if "returncode" in environment_results and environment_results["returncode"] != "0":
        print(
            "Failed to list the environments, returncode: {}".format(
                environment_results["returncode"]
            )
        )
        return False, []

    if "output" not in environment_results or not environment_results["output"]:
        print("Failed to list the environments, output: {}".format(environment_results))
        return False, []

    json_output = json.loads(environment_results["output"])
    environments = []
    for environment in json_output["envs"]:
        new_environment = {}
        environment_name = os.path.basename(environment)
        new_environment["name"] = environment_name
        new_environment["path"] = environment
        environments.append(new_environment)

    return True, environments
