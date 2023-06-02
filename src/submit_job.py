import click
import os
from job.initialize import check_job_paths
from job.run import run_job
from utils.io import exists, expanduser


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.argument("job-file")
@click.option(
    "--runtime-directory",
    "-rd",
    default=os.path.join("~", "modi_mount"),
    help="""
    The path to the runtime directory in which the job is to be executed.
    This directory must be within the scratch space directory.
    """,
)
@click.option(
    "--scratch-space-directory",
    "-ssd",
    default=os.path.join("~", "modi_mount"),
    help="""
    The path to the scratch space directory.
    """,
)
def main(job_file, runtime_directory, scratch_space_directory):
    job_file = expanduser(job_file)
    runtime_directory = expanduser(runtime_directory)
    scratch_space_directory = expanduser(scratch_space_directory)

    if not exists(job_file):
        print(
            "Failed to find the job-file: {} - are you sure it exists?".format(job_file)
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

    job_output = run_job(job_file, runtime_directory)
    if job_output["returncode"] != "0":
        print("Failed to execute the job: {} - {}".format(job_file, job_output))
        exit(-2)


if __name__ == "__main__":
    main()
