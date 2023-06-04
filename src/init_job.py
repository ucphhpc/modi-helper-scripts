import click
import os
from job.initialize import check_job_paths, write_job_script
from job.run import run_job
from utils.io import exists, expanduser


@click.command(
    "cli",
    context_settings=dict(
        help_option_names=["-h", "--help"],
        show_default=True)
)
@click.argument("job-file")
@click.option(
    "--job-args",
    "-ja",
    multiple=True,
    help="""
    The list of arguments that should be passed to the `job-file`.
    """,
)
@click.option(
    "--runtime-directory",
    "-rd",
    default=os.path.join("~", "modi_mount"),
    help="""The path to the runtime directory in which the job is to be executed.
    This directory must be within the scratch space directory.""",
)
@click.option(
    "--scratch-space-directory",
    "-ssd",
    default=os.path.join("~", "modi_mount"),
    help="""The path to the scratch space directory.""",
)
@click.option(
    "--generate-job-scripts",
    "-gjs",
    default=False,
    help="""
    Whether the script should generate job script files that execute the `job_file` as a job.
    """
)
@click.option(
    "--generate-container-wrap",
    "-gcw",
    default=False,
    help="""
    Whether the generate job scripts should wrap the `job_file` execution in a container environment.
    """
)
@click.option(
    "--container-wrap-image",
    "-cwi",
    default=os.getenv("MODI_DEFAULT_IMAGE", None)
    help="""
    The container image to use when generating the job scripts.
    """
)
def main(job_file, job_args, runtime_directory, scratch_space_directory, generate_job_scripts, generate_container_wrap, container_wrap_image):
    job_file = expanduser(job_file)
    runtime_directory = expanduser(runtime_directory)
    scratch_space_directory = expanduser(scratch_space_directory)

    if not exists(job_file):
        print(
            "Failed to find the job-file:'{}' are you sure it exists?".format(job_file)
        )
        exit(-1)

    if not exists(runtime_directory):
        print("The specified runtime directory does not exist.")
        exit(-1)

    if not exists(scratch_space_directory):
        print("The specified scratch space directory does not exist.")
        exit(-1)

    correct_directories = check_job_paths(scratch_space_directory, runtime_directory)
    if not correct_directories:
        print(
            "Your `runtime-directory`: {} must reside inside the `scratch-space-directory`".format(
                runtime_directory, scratch_space_directory
            )
        )
        exit(-2)

    correct_job = check_job_paths(runtime_directory, job_file)
    if not correct_job:
        print(
            "Your `job-file`: {} must reside inside the `runtime-directory`: {}".format(
                job_file, runtime_directory
            )
        )
        exit(-2)

    if generate_job_scripts:
        write_job_script(runtime_directory, job_file, generate_container_wrap=generate_container_wrap, container_wrap_image=container_wrap_image)

    job_output = run_job(runtime_directory, job_file, *job_args)
    if job_output["returncode"] != "0":
        print("Failed to execute the job: {} - {}".format(job_file, job_output))
        exit(-2)


if __name__ == "__main__":
    main()
