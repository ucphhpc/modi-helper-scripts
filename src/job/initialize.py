from utils.io import expanduser


def check_job_paths(runtime_directory, job_file):
    """The job_file must exist within the runtime_directory.
    If not, the cluster nodes will not be able to access it."""
    return expanduser(job_file).startswith(expanduser(runtime_directory))
