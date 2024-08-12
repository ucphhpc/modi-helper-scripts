import click
import os
import sys
from modi_helper.defaults import CONTAINER_WRAP, REGULAR
from modi_helper.job.initialize import (
    check_job_paths,
    write_job_script,
    make_job_script_content,
    extract_extra_job_settings,
)
from modi_helper.job.run import run_job
from modi_helper.utils.io import (
    exists,
    expanduser,
    set_execute_permissions,
)
from modi_helper.cli.return_codes import (
    SUCCESS,
    PATH_NOT_FOUND,
    PERMISSIONS_ERROR,
    SETUP_ERROR,
    WRITE_ERROR,
    EXECUTE_ERROR,
)


@click.command(
    "cli",
    context_settings=dict(
        help_option_names=["-h", "--help"], show_default=True
    ),
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
    default=[],
    help="""
    The list of arguments that should be passed to the JOB_FILE.
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
    Whether the script should generate job script files that execute the JOB_FILE as a job.
    """,
)
@click.option(
    "--generate-container-wrap",
    "-gcw",
    default=False,
    is_flag=True,
    help="""
    Whether the generate job scripts should wrap the JOB_FILE execution in a container environment.
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
@click.option(
    "--verbose",
    "-v",
    default=False,
    is_flag=True,
    help="""
    Whether to print verbose output.
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
    verbose,
):
    job_file = expanduser(job_file)
    runtime_directory = expanduser(runtime_directory)
    scratch_space_directory = expanduser(scratch_space_directory)

    # Prepend the current working directory to the JOB_FILE path if no subpath is specified
    if not os.path.dirname(job_file):
        job_file = os.path.join(os.getcwd(), job_file)

    if not exists(job_file):
        print(
            "Failed to find the JOB_FILE:'{}' are you sure it exists?".format(
                job_file
            )
        )
        return PATH_NOT_FOUND

    if not os.access(job_file, os.X_OK):
        print(
            "The JOB_FILE:'{}' does not have the executable permission set.".format(
                job_file
            )
        )
        # Set execute permissions on the JOB_FILE
        print(
            "Trying to set execute permissions on the JOB_FILE: {}".format(
                job_file
            )
        )
        if not set_execute_permissions(job_file):
            return PERMISSIONS_ERROR
        print(
            "Succeeded in giving the JOB_FILE: {} execute permissions.".format(
                job_file
            )
        )

    if not exists(runtime_directory):
        print("The specified runtime directory does not exist.")
        return PATH_NOT_FOUND

    if not exists(scratch_space_directory):
        print("The specified scratch space directory does not exist.")
        return PATH_NOT_FOUND

    correct_directories = check_job_paths(
        scratch_space_directory, runtime_directory
    )
    if not correct_directories:
        print(
            "Your `runtime-directory`: {} must reside inside the `scratch-space-directory`: {}".format(
                runtime_directory, scratch_space_directory
            )
        )
        return SETUP_ERROR

    correct_job = check_job_paths(runtime_directory, job_file)
    if not correct_job:
        print(
            "Your JOB_FILE: {} must reside inside the `runtime-directory`: {}".format(
                job_file, runtime_directory
            )
        )
        return SETUP_ERROR

    if verbose:
        print(
            "Submitting JOB_FILE: {} with the following settings".format(
                job_file
            )
        )
        print("Job Runner: {}".format(job_runner))
        print("Job Args: {}".format(job_args))
        print("Runtime Directory: {}".format(runtime_directory))
        print("Scratch Space Directory: {}".format(scratch_space_directory))
        if generate_job_scripts:
            print("Generate Job Scripts: {}".format(generate_job_scripts))
        if generate_container_wrap:
            print(
                "Generate Container Wrap: {}".format(generate_container_wrap)
            )
            print("Container Wrap Image: {}".format(container_wrap_image))

    if generate_job_scripts:
        # We set the jobs_args to "$@" so that the new job script can pass the arguments to the JOB_FILE
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
            new_job_file_name = "{}.{}".format(
                os.path.basename(job_file), REGULAR
            )

        # Check if the original JOB_FILE sets extra_job_settings
        # If so, then we need to pass these to the new job script
        # so that the new job script can set the same settings.
        extra_job_settings = extract_extra_job_settings(job_file)
        if extra_job_settings:
            template_kwargs["extra_job_settings"] = extra_job_settings

        new_job_file_path = os.path.join(runtime_directory, new_job_file_name)
        job_script_content = make_job_script_content(
            template_file_name, template_kwargs=template_kwargs
        )
        wrote_job_script = write_job_script(
            new_job_file_path, job_script_content
        )
        if not wrote_job_script:
            print(
                "Failed to write the generated job script: {}".format(
                    new_job_file_name
                )
            )
            return WRITE_ERROR
        if verbose:
            print(
                "Successfully generated new job script: {} from template: {}".format(
                    new_job_file_name, template_file_name
                )
            )
        # Ensure the new job script has the executable permission set
        if not set_execute_permissions(new_job_file_path):
            print(
                "Failed to set the execute permission on generated new job script: {}".format(
                    new_job_file_path
                )
            )
            return PERMISSIONS_ERROR
        job_file = new_job_file_path

    if verbose:
        print(
            "Executing JOB_FILE: {} with the following arguments: {}".format(
                job_file, job_args
            )
        )
    job_output = run_job(runtime_directory, job_file, *job_args)
    print(
        "Your job output will be placed in the runtime directory: {}".format(
            runtime_directory
        )
    )
    if job_output["returncode"] != "0":
        print(
            "Failed to execute the JOB_FILE: {} - {}".format(
                job_file, job_output
            )
        )
        return EXECUTE_ERROR
    if verbose:
        print("Job executed successfully.")
    return SUCCESS


def cli():
    sys.exit(main())


if __name__ == "__main__":
    sys.exit(main())
