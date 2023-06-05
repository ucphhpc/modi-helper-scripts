from modi_helper.utils.job import run


def run_job(runtime_directory, job_file, *args, **kwargs):
    command = ["sbatch", job_file]
    if args:
        command.extend(*args)
    return run(command, cwd=runtime_directory, format_output_str=True)
