import click
import sys
from modi_helper.environment.initialize import initialize_conda
from modi_helper.environment.list import list_environments
from modi_helper.cli.return_codes import (
    SUCCESS,
    EXECUTE_ERROR,
    SETUP_ERROR,
)


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
# Make a click option for extra conda args
@click.option(
    "--extra-conda-args",
    default=None,
    show_default=True,
    help="Extra arguments to pass to conda",
)
def main(extra_conda_args):
    # Ensure that conda is initialized
    initialized, output = initialize_conda(quiet=True)
    if not initialized:
        print(output)
        return SETUP_ERROR

    success, environments = list_environments(
        extra_conda_args=extra_conda_args
    )
    if not success:
        print("Failed to list environments")
        return EXECUTE_ERROR
    print(environments)
    return SUCCESS


def cli():
    sys.exit(main())


if __name__ == "__main__":
    sys.exit(main())
