import click
import os
from modi_helper.defaults import CONTAINER_WRAP, REGULAR
from modi_helper.job.initialize import (
    check_job_paths,
    write_job_script,
    make_job_script_content,
    extract_extra_job_settings,
)
from modi_helper.job.run import run_job
from modi_helper.utils.io import exists, expanduser, set_execute_permissions


@click.command(
    "cli", context_settings=dict(help_option_names=["-h", "--help"], show_default=True)
)
@click.argument("job-file")
@click.option(
    "--job-runner",
    "-jr",
    default="srun",
    help="""
    The executable that is used to execute the container image if the --generate-container-wrap is used.
    """,
)
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
    default=os.getcwd(),
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
    is_flag=True,
    help="""
    Whether the script should generate job script files that execute the `job_file` as a job.
    """,
)
@click.option(
    "--generate-container-wrap",
    "-gcw",
    default=False,
    is_flag=True,
    help="""
    Whether the generate job scripts should wrap the `job_file` execution in a container environment.
    """,
)
@click.option(
    "--container-wrap-image",
    "-cwi",
    default=os.path.join(
        "~",
        "modi_images",
        os.getenv("MODI_DEFAULT_IMAGE", "ucphhpc/slurm-notebook:latest"),
    ),
    help="""
    The container image to use when generating the job scripts.
    """,
)
def main(
    job_file,
    job_runner,
    job_args,
    runtime_directory,
    scratch_space_directory,
    generate_job_scripts,
    generate_container_wrap,
    container_wrap_image,
):
    job_file = expanduser(job_file)
    runtime_directory = expanduser(runtime_directory)
    scratch_space_directory = expanduser(scratch_space_directory)

    # Prepend the current working directory to the job file path if no subpath is specified
    if not os.path.dirname(job_file):
        job_file = os.path.join(os.getcwd(), job_file)

    if not exists(job_file):
        print(
            "Failed to find the job-file:'{}' are you sure it exists?".format(job_file)
        )
        exit(-1)

    if not os.access(job_file, os.X_OK):
        print(
            "The job-file:'{}' does not have the executable permission set.".format(
                job_file
            )
        )
        # Set execute permissions on the job file
        print("Trying to set execute permissions on the job file: {}".format(job_file))
        if not set_execute_permissions(job_file):
            exit(-1)
        print(
            "Succeeded in giving the job file: {} execute permissions.".format(job_file)
        )

    if not exists(runtime_directory):
        print("The specified runtime directory does not exist.")
        exit(-1)

    if not exists(scratch_space_directory):
        print("The specified scratch space directory does not exist.")
        exit(-1)

    correct_directories = check_job_paths(scratch_space_directory, runtime_directory)
    if not correct_directories:
        print(
            "Your `runtime-directory`: {} must reside inside the `scratch-space-directory`: {}".format(
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
        # We set the jobs_args to "$@" so that the new job script can pass the arguments to the job file
        template_kwargs = {
            "job_runner": job_runner,
            "job_file": job_file,
            "job_args": "$@",
        }
        if generate_container_wrap:
            template_file_name = CONTAINER_WRAP + ".j2"
            new_job_file_name = "{}.{}".format(
                os.path.basename(job_file), CONTAINER_WRAP
            )
            template_kwargs["container_wrap_image"] = container_wrap_image
        else:
            template_file_name = REGULAR + ".j2"
            new_job_file_name = "{}.{}".format(os.path.basename(job_file), REGULAR)

        # Check if the original job file sets extra_job_settings
        # If so, then we need to pass these to the new job script
        # so that the new job script can set the same settings.
        extra_job_settings = extract_extra_job_settings(job_file)
        if extra_job_settings:
            template_kwargs["extra_job_settings"] = extra_job_settings

        new_job_file_path = os.path.join(runtime_directory, new_job_file_name)
        job_script_content = make_job_script_content(
            template_file_name, template_kwargs=template_kwargs
        )
        wrote_job_script = write_job_script(new_job_file_path, job_script_content)
        if not wrote_job_script:
            print(
                "Failed to write the generated job script: {}".format(new_job_file_name)
            )
            exit(-2)
        # Ensure the new job script has the executable permission set
        if not set_execute_permissions(new_job_file_path):
            print(
                "Failed to set the execute permission on generated new job script: {}".format(
                    new_job_file_path
                )
            )
            exit(-2)
        job_file = new_job_file_path

    job_output = run_job(runtime_directory, job_file, *job_args)
    print(
        "Your job output will be placed in the runtime directory: {}".format(
            runtime_directory
        )
    )
    if job_output["returncode"] != "0":
        print("Failed to execute the job: {} - {}".format(job_file, job_output))
        exit(-2)


if __name__ == "__main__":
    main()
