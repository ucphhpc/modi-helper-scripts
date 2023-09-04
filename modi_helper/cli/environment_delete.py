import click
from modi_helper.environment.initialize import initialize_conda
from modi_helper.environment.delete import delete_environment


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.argument("name", type=click.STRING)
@click.option(
    "--automatic-yes",
    "-y",
    default=True,
    help="Whether the environment deletion should automatically proceed without user input.",
)
@click.option("--quiet", "-q", is_flag=True, default=False, show_default=True)
def main(name, automatic_yes, quiet):
    # Ensure that conda is initialized
    initialized, output = initialize_conda(quiet=quiet)
    if not initialized:
        print(output)
        exit(-2)

    deleted = delete_environment(
        name,
        automatic_yes=automatic_yes,
        quiet=quiet,
    )
    if deleted["returncode"] != "0":
        print("Failed to delete environment: {} - {}".format(name, deleted))
        exit(-3)


if __name__ == "__main__":
    main()
