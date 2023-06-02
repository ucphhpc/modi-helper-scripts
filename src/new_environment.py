import click
import os
from utils.io import exists, makedirs
from environment.initialize import initialize_conda
from environment.create import (
    create_environment,
    activate_environment,
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
    "--automatic-proceed",
    "-ap",
    default=True,
    help="Whether the environment creation should automatically proceed without user input.",
)
@click.option("--activate", "-a", is_flag=True, default=True, show_default=True)
def main(name, destination_dir, automatic_proceed, activate):
    if not exists(destination_dir):
        created, msg = makedirs(destination_dir)
        if not created:
            print(msg)
            exit(-1)

    # Ensure that conda is initialized
    initialized, output = initialize_conda()
    if not initialized:
        print(output)
        exit(-2)

    created = create_environment(
        name, destination=destination_dir, automatic_proceed=automatic_proceed
    )
    if created["returncode"] != "0":
        print("Failed to create environment: {} - {}".format(name, created))
        exit(-3)

    if activate:
        activated = activate_environment(name)
        if not activated:
            print("Failed to activate environment: {} - {}".format(name, activated))
            exit(-4)
    exit(0)


if __name__ == "__main__":
    main()
