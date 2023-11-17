import click
import os
from modi_helper.utils.io import exists
from modi_helper.environment.initialize import (
    get_environment_directories,
)
from modi_helper.environment.create import (
    add_environment_directory,
)


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "--environment-dir",
    "-ed",
    default=os.path.join("~", "modi_mount", "my_conda_environments"),
    show_default=True,
    help="The directory in which the environments are located.",
)
@click.option("--quiet", "-q", is_flag=True, default=False, show_default=True)
def main(environment_dir, quiet):
    if not exists(environment_dir):
        print("The designated environment directory does not exist")
        exit(-1)

    found, environment_directories = get_environment_directories()
    if found:
        if environment_dir in environment_directories:
            if not quiet:
                print(
                    "The environment directory: {} is already in the list of environment directories: {}".format(
                        environment_dir, environment_directories
                    )
                )
            exit(0)

    # Ensure that the destionation directory is added as a conda environment directory
    # This is done to ensure that the environment can be activated from anywhere
    # in the file system by name.
    added = add_environment_directory(environment_dir)
    if not added:
        print(
            "Failed to add environment directory: {} - {}".format(
                environment_dir, added
            )
        )
        exit(-5)


if __name__ == "__main__":
    main()
