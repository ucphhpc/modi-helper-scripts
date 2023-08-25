New Job
=======

To submit a new job in MODI, the modi-helper-scripts provide the following CLI tool::

    $ modi-new-job --help
        Usage: modi-new-job [OPTIONS] JOB_FILE

        Options:
        -ja, --job-args TEXT            The list of arguments that should be passed
                                        to the `job-file`.
        -rd, --runtime-directory TEXT   The path to the runtime directory in which
                                        the job is to be executed. This directory
                                        must be within the scratch space directory.
                                        [default: ~/modi_mount]
        -ssd, --scratch-space-directory TEXT
                                        The path to the scratch space directory.
                                        [default: ~/modi_mount]
        -gjs, --generate-job-scripts    Whether the script should generate job
                                        script files that execute the `job_file` as
                                        a job.
        -gcw, --generate-container-wrap
                                        Whether the generate job scripts should wrap
                                        the `job_file` execution in a container
                                        environment.
        -cwi, --container-wrap-image TEXT
                                        The container image to use when generating
                                        the job scripts.  [default:
                                        ~/modi_images/ucphhpc/hpc-notebook:22.05.9]
        -h, --help                      Show this message and exit.

As is shown in the help message, the only required arguments is the path to the JOB_FILE that is to be executed.

The ``--job-args`` option can be used to pass arguments to the ``JOB_FILE`` when it is executed. These arguments will be passed to the ``JOB_FILE`` as positional arguments.

The ``--runtime-directory`` option can be used to specify the runtime directory in which the job is to be executed. This directory must be within the scratch space directory which is also validated at runtime.
