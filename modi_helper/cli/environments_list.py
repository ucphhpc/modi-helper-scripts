import click
from modi_helper.environment.initialize import initialize_conda
from modi_helper.environment.list import list_environments


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
        exit(-2)

    success, environments = list_environments(extra_conda_args=extra_conda_args)
    if not success:
        print("Failed to list environments")
        exit(-1)
    print(environments)
