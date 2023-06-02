from utils.job import run


def run_job(runtime_directory, job_file):
    command = ["sbatch", job_file]
    return run(command, cwd=runtime_directory)
