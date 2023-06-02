import click
import os
from job.initialize import check_job_paths
from job.run import run_job
from utils.io import exists


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.argument("job_file")
@click.option(
    "--runtime-directory",
    "-rd",
    default=os.path.join("~", "modi_mount"),
    help="The path to the runtime directory in which the job is to be executed",
)
def main(job_file, runtime_directory):
    if not exists(job_file):
        print(
            "Failed to find the job file: {} - are you sure it exists?".format(job_file)
        )
        exit(-1)

    correct_paths = check_job_paths(runtime_directory, job_file)
    if not correct_paths:
        print(
            "Your `job_file`: {} must reside inside the scratch_space directory: {}".format(
                job_file, runtime_directory
            )
        )
        exit(-3)

    job_output = run_job(job_file, runtime_directory)
    if job_output["returncode"] != "0":
        print("Failed to execute the job: {} - {}".format(job_file, job_output))
        exit(-2)


if __name__ == "__main__":
    main()
