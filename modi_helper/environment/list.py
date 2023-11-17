import os
from modi_helper.utils.job import run


def list_environments(extra_conda_args=None):
    command = ["conda", "env", "list", "--json"]
    if extra_conda_args:
        if isinstance(extra_conda_args, (list, tuple, set)):
            command.extend(extra_conda_args)
        elif isinstance(extra_conda_args, str):
            extra_conda_args_list = extra_conda_args.split(" ")
            command.extend(extra_conda_args_list)

    environment_results = run(command, format_output_str=True)
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

    environments = {}
    for environment in environment_results["envs"]:
        environment_name = os.path.basename(environment)
        environments["name"] = environment_name
        environments["path"] = environment
    return True, environments
