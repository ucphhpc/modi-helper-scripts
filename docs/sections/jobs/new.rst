Submitting a Job
================

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

As is shown in the help message, the only required arguments is the path to the ``JOB_FILE`` that is to be executed.

The ``--job-args`` option can be used to pass arguments to the ``JOB_FILE`` when it is executed. These arguments will be passed to the ``JOB_FILE`` as positional arguments.

The ``--runtime-directory`` option can be used to specify the runtime directory in which the job is to be executed. This directory must be within the scratch space directory which is also validated at runtime.
Furthermore, the ``JOB_FILE`` must reside inside the runtime directory when the new job is submitted.

The ``--scratch-space-directory`` option can be used to specify the scratch space directory. This directory is where within the runtime directory must either be equal or reside.

The ``--generate-job-scripts`` option can be used to generate job scripts that execute the ``JOB_FILE`` as a job. This is useful if the ``JOB_FILE`` is not a job script itself.
In addition, the ``--generate-job-scripts`` can be used in conjunction with the two following arguments, to ensure that the job is executed within a specific container environment.

The ``--generate-container-wrap`` option can be used to generate job scripts that wrap the ``JOB_FILE`` execution in a container environment. This is useful if the ``JOB_FILE`` is not a job script itself.

The ``--container-wrap-image`` option can be used to specify the container image to use when generating the job scripts. The default is the ``ucphhpc/hpc-notebook:22.05.9`` image.

Examples
--------

The following examples show how to a simple Hello World script as a new job in MODI.

Create a simple script file, that will be your job::

    ~/modi_mount/hello_world$ cat hello_world.sh
    #!/bin/bash

    echo "Hello World"

Ensure that the script file is executable::

    ~/modi_mount/hello_world$ chmod +x hello_world.sh

Submit the script file as job::
    ~/modi_mount/hello_world$ modi-new-job hello_world.sh 
    Submitted batch job 1376

Which will return the job id of the submitted job. The output will be produced to a standard SLURM output file in the defined ``--runtime-directory`` path.
