import click
import os
from modi_helper.utils.io import exists, makedirs
from modi_helper.environment.initialize import initialize_conda
from modi_helper.environment.create import (
    create_environment,
    activate_environment,
    add_environment_directory
)


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "--environment-dir",
    "-ed",
    default=os.path.join("~", "modi_mount", "my_conda_environments"),
    show_default=True,
    help="The directory in which the environments are located.",
)
# Make a click option for extra conda args
@click.option("--extra-conda-args", default=None, show_default=True, help="Extra arguments to pass to conda")
def main(environment_dir, extra_conda_args):
    if not exists(environment_dir):
        print("The designated environment directory does not exist")
        exit(-1)

    # Ensure that conda is initialized
    initialized, output = initialize_conda()
    if not initialized:
        print(output)
        exit(-2)

    # Ensure that the destionation directory is added as a conda environment directory
    # This is done to ensure that the environment can be activated from anywhere
    # in the file system by name.
    added = add_environment_directory(environment_dir)
    if not added:
        print("Failed to add environment directory: {} - {}".format(name, added))
        exit(-5)

if __name__ == "__main__":
    main()
