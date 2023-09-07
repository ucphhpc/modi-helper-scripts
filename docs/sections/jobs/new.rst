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

Hello World
~~~~~~~~~~~

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

This will return the job id of the submitted job.
The job's output will be produced/placed to a standard SLURM output file in the directory specified by the ``--runtime-directory`` argument, which by default sets it to the current working directory::

    ~/modi_mount/hello_world$ cat slurm-1376.out
    Hello World


Job with Custom Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to submit a job within a custom conda environment, you can utilize the precreated enviorments via the ``modi-new-environment`` CLI tool.
For instance, if we want to use torch's CPU version to accomplish some compute, we can first create an environment where we can installed the required packages::

    # -q to enable quiet mode to supress some of the conda output junk
    ~$ modi-new-environment torch_cpu -q

Hereafter, we can activate and install the required packages in our shell environment::

    ~$ conda activate torch_cpu
    (torch_cpu) ~$ conda install pytorch torchvision torchaudio cpuonly -c pytorch -y

After a substantial amount of time where the packages are installed, we can create the torch analysis script and the additional job file to execute it.
The torch program will just be a simple tutorial example extracted from https://pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html::

    # First, we create a directory to put our touch program and job file in
    (torch_cpu) ~$ mkdir ~/torch_analysis && cd ~/torch_analysis

    # Secondly, we create a torch_program.py with the mentioned content
    (torch_cpu) ~$ cat torch_program.py
    import torch
    from torch import nn
    from torch.utils.data import DataLoader
    from torchvision import datasets
    from torchvision.transforms import ToTensor
    ...

    # Thirdly, we create a SLURM job file that will use our created torch_cpu environemnt and execute the torch program
    (torch_cpu) ~$ cat slurm_torch_job.sh
    #!/bin/bash

    # Refresh which environments are available and activate the required one
    source $CONDA_DIR/etc/profile.d/conda.sh
    modi-load-environments
    conda activate torch_cpu

    python3 torch_program.py

    # Finally, we can submit the job via the ``modi-new-job`` CLI tool.
    (torch_cpu) ~$ conda deactivate
    ~$ modi-new-job --generate-job-scripts --generate-container-wrap slurm_torch_job.sh


Running an R job
~~~~~~~~~~~~~~~~

The following example shows how to run a simple R script as a new job in MODI.

First, create an enviornment where we will install our R packages::
    
        ~$ modi-new-environment R-env -q

Secondly, we can activate and install the required packages in our shell environment::
    
    ~$ conda activate R-env
    (R-env) ~$ conda install -c conda-forge r-base r-essentials -y

Next, we create a directory to put our R script in::

    (R-env) ~$ mkdir ~/modi_mount/r_example && cd ~/modi_mount/r_example

Hereafter, we can create an R script that will contain the code which we will want executed as a job::

    (R-env) ~/modi_mount/r_example$ cat example.R

    # Get a random log-normal distribution
    r <- rlnorm(1000)

    # Get the distribution without plotting it using tighter breaks
    h <- hist(r, plot=F, breaks=c(seq(0,max(r)+1, .1)))

    # Plot the distribution using log scale on both axes, and use
    # blue points
    plot(h$counts, log="xy", pch=20, col="blue",
    main="Log-normal distribution",
    xlab="Value", ylab="Frequency")

    # Define cars vector with 5 values
    cars <- c(1, 3, 6, 4, 9)

    # Create a pie chart for cars
    pie(cars)

Now we are almost ready to submit the R script as a job. The final bit we need is to create
a job script file that will execute our R script::
    
        (R-env) ~/modi_mount/r_example$ cat slurm_r_job.sh
        #!/bin/bash
    
        # Refresh which environments are available and activate the required one
        source $CONDA_DIR/etc/profile.d/conda.sh
        modi-load-environments
        conda activate R-env
    
        Rscript example.R
    
        # Finally, we can submit the job via the ``modi-new-job`` CLI tool.
        (R-env) ~/modi_mount/r_example$ modi-new-job --generate-job-scripts --generate-container-wrap slurm_r_job.sh
