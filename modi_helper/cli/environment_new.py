import click
import os
from modi_helper.utils.io import exists, makedirs
from modi_helper.environment.initialize import initialize_conda
from modi_helper.environment.create import (
    create_environment,
    activate_environment,
    add_environment_directory,
)


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.argument("name", type=click.STRING)
@click.option(
    "--destination-dir",
    "-dd",
    default=os.path.join("~", "modi_mount", "my_conda_environments"),
    show_default=True,
    help="The directory in which the environment will be created",
)
@click.option(
    "--automatic-yes",
    "-y",
    default=True,
    is_flag=True,
    help="Whether the environment creation should automatically proceed without user input.",
)
@click.option("--activate", "-a", is_flag=True, default=True, show_default=True)
@click.option("--quiet", "-q", is_flag=True, default=False, show_default=True)
# Make a click option for extra conda args
@click.option(
    "--extra-conda-args",
    default=None,
    show_default=True,
    help="Extra arguments to pass to conda",
)
def main(name, destination_dir, automatic_yes, activate, quiet, extra_conda_args):
    if not exists(destination_dir):
        created, msg = makedirs(destination_dir)
        if not created:
            print(msg)
            exit(-1)

    # Ensure that conda is initialized
    initialized, output = initialize_conda(quiet=quiet)
    if not initialized:
        print(output)
        exit(-2)

    created = create_environment(
        name,
        destination=destination_dir,
        automatic_yes=automatic_yes,
        quiet=quiet,
        extra_conda_args=extra_conda_args,
    )
    if created["returncode"] != "0":
        print("Failed to create environment: {} - {}".format(name, created))
        exit(-3)

    if activate:
        activated = activate_environment(name)
        if not activated:
            print("Failed to activate environment: {} - {}".format(name, activated))
            exit(-4)

    # Ensure that the destionation directory is added as a conda environment directory
    # This is done to ensure that the environment can be activated from anywhere
    # in the file system by name.
    added = add_environment_directory(destination_dir)
    if not added:
        print("Failed to add environment directory: {} - {}".format(name, added))
        exit(-5)


if __name__ == "__main__":
    main()
