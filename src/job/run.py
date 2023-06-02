from utils.job import run


def run_job(job_file, runtime_directory):
    command = ["sbatch", job_file]
    return run(command, cwd=runtime_directory)
