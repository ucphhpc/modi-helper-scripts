Submitting a Job
================

To submit a new job in MODI, the modi-helper-scripts provide the following CLI tool::

    $ modi-new-job --help
        Usage: modi-new-job [OPTIONS] JOB_FILE

        Options:
        -jr, --job-runner TEXT          The executable that is used to execute the
                                        container image if the --generate-container-
                                        wrap is used.  [default: srun]
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
                                        ~/modi_images/ucphhpc/hpc-notebook:22.05.11]
        -h, --help                      Show this message and exit.

As is shown in the help message, the only required arguments is the path to the ``JOB_FILE`` that is to be executed.

The ``--job-runner`` option can be used to specify the executable that is used to execute the job. The option also define how a particular container image should be executed if it is paired with ``--generate-container-wrap``. The default is ``srun``.

The ``--job-args`` option can be used to pass arguments to the ``JOB_FILE`` when it is executed. These arguments will be passed to the ``JOB_FILE`` as positional arguments.

The ``--runtime-directory`` option can be used to specify the runtime directory in which the job is to be executed. This directory must be within the scratch space directory which is also validated at runtime.
Furthermore, the ``JOB_FILE`` must reside inside the runtime directory when the new job is submitted.

The ``--scratch-space-directory`` option can be used to specify the scratch space directory. This directory is where within the runtime directory must either be equal or reside.

The ``--generate-job-scripts`` option can be used to generate job scripts that execute the ``JOB_FILE`` as a job. This is useful if the ``JOB_FILE`` is not a job script itself.
In addition, the ``--generate-job-scripts`` can be used in conjunction with the two following arguments, to ensure that the job is executed within a specific container environment.

The ``--generate-container-wrap`` option can be used to generate job scripts that wrap the ``JOB_FILE`` execution in a container environment. This is useful if the ``JOB_FILE`` is not a job script itself.

The ``--container-wrap-image`` option can be used to specify the container image to use when generating the job scripts. The default is the ``ucphhpc/hpc-notebook:22.05.9`` image.

The following examples show how to submit a new job in MODI.

Hello World
-----------

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


Selecting a MODI SLURM partition
--------------------------------

By default, the a job submission on MODI will use the default ``modi_devel`` partition.
If you want to submit a job to a different partition, you can set the ``#SBATCH --partition <partition_name>`` directive in the job file.

For instance, if you want to submit a job to the ``modi_short`` partition, you can create a job file with the following content::

    ~/modi_mount/hello_world$ cat hello_world_partition.sh
    #!/bin/bash
    #SBATCH --partition modi_short

    # Sleep such that you have time to check the queue for its partition
    sleep 15
    echo "Hello World"

After this has been set, you can submit the job as usual::

    ~/modi_mount/hello_world$ modi-new-job hello_world_partition.sh
    Submitted batch job 1377


Job with Custom Environment
---------------------------

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


Running a Python job
--------------------
The following example shows how to run a simple Python program as a new job in MODI.

First, create an enviornment where we will install our Python packages::

    ~$ modi-new-environment my-python-env -q

Secondly, we create a directory to put our Python program and job file in::

    ~$ mkdir ~/modi_mount/python_example && cd ~/modi_mount/python_example

Hereafter, we can create a Python program that will contain the code which we will want executed as a job::

    ~/modi_mount/python_example$ cat example.py
    import numpy as np

    a = np.array([1, 2, 3, 4, 5])
    b = np.array([5, 4, 3, 2, 1])

    print(a + b)

Now we are almost ready to submit the Python program as a job. The second to last bit is that we need is to create
a job script file that will execute our Python program::

    ~/modi_mount/python_example$ cat slurm_python_job.sh
    #!/bin/bash

    # Refresh which environments are available and activate the required one
    source $CONDA_DIR/etc/profile.d/conda.sh
    modi-load-environments
    conda activate my-python-env

    python3 example.py

Finally, we use the ``modi-new-job`` CLI tool to submit the job::

    ~/modi_mount/python_example$ modi-new-job --generate-job-scripts --generate-container-wrap slurm_python_job.sh
    Submitted batch job 1378


Running an R job
----------------

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

    v1 <- c(1,2,3,4,5,6,7,8,9,10)
    v2 <- c(1,2,3,4,5,6,7,8,9,10)

    print(v1 + v2)

Now we are almost ready to submit the R script as a job. The second to last bit is that we need is to create
a job script file that will execute our R script::
    
        (R-env) ~/modi_mount/r_example$ cat slurm_r_job.sh
        #!/bin/bash
    
        # Refresh which environments are available and activate the required one
        source $CONDA_DIR/etc/profile.d/conda.sh
        modi-load-environments
        conda activate R-env
    
        Rscript example.R

Finally, we use the ``modi-new-job`` CLI tool to submit the job::

    (R-env) ~/modi_mount/r_example$ modi-new-job --generate-job-scripts --generate-container-wrap slurm_r_job.sh
    Submitted batch job 1377

You will then be able to find the SLURM output files in the directory in which you executed the ``modi-new-job`` CLI tool.


Running a Notebook file as a job
---------------------------------

The following example shows how to run a Jupyter Notebook file as a new job in MODI.

First, create an enviornment where we will install our Jupyter and Python packages::

    ~$ modi-new-environment my-jupyter-env -q

Secondly, we can activate and install the required packages in our shell environment::
    
        ~$ conda activate my-jupyter-env
        (my-jupyter-env) ~$ conda install jupyter -y

Next, we create a directory to put our Jupyter Notebook file in::
    
        (my-jupyter-env) ~$ mkdir ~/modi_mount/jupyter_example && cd ~/modi_mount/jupyter_example
    
Hereafter, we can create a Jupyter Notebook file that will contain the code which we will want executed as a job.
We can create this file via the JupyterLab interface in MODI inside the ~/modi_mount/jupyter_example directory.

.. toctree::
    :maxdepth: 2
    :caption: Notebook Example:

    notebooks/example1.ipynb

After creating the Jupyter Notebook file, we can see it in the ~/modi_mount/jupyter_example directory::

        my-jupyter-env) ~/modi_mount/jupyter_example$ ls -la
        total 148
        drwxr-xr-x  3 user_id users   4096 Mar 21 09:11 .
        drwxr-xr-x 35 user_id users   4096 Mar 21 08:25 ..
        drwxr-xr-x  2 user_id users   4096 Sep  8  2023 .ipynb_checkpoints
        -rw-r--r--  1 user_id users 133720 Mar 21 09:07 notebook.ipynb
        -rwxr-xr-x  1 user_id users    221 Sep  8  2023 slurm_jupyter_job.sh


After coping in the Jupyter Notebook to the ~/modi_mount/jupyter_example directory, we can create a job script file that will execute our Jupyter Notebook::
    
        (my-jupyter-env) ~/modi_mount/jupyter_example$ cat slurm_jupyter_job.sh
        #!/bin/bash
    
        # Refresh which environments are available and activate the required one
        source $CONDA_DIR/etc/profile.d/conda.sh
        modi-load-environments
        conda activate my-jupyter-env
    
        # This will execute the given Jupyter Notebook file and produce an output Jupyter Notebook file
        # in the directory it was executed in
        jupyter nbconvert --execute --to notebook notebook.ipynb

Finally, we use the ``modi-new-job`` CLI tool to submit the job::
    
        (my-jupyter-env) ~/modi_mount/jupyter_example$ modi-new-job --generate-job-scripts --generate-container-wrap slurm_jupyter_job.sh
        Submitted batch job 1277

After the job has completed, you should be able to see an output Jupyter Notebook file in the ~/modi_mount/jupyter_example directory 
with the name ``notebook.nbconvert.ipynb``::

    (my-jupyter-env) ~/modi_mount/jupyter_example$ ls -la
    total 288
    drwxr-xr-x  3 user_id users   4096 Mar 21 09:22 .
    drwxr-xr-x 35 user_id users   4096 Mar 21 08:25 ..
    drwxr-xr-x  2 user_id users   4096 Mar 21 09:19 .ipynb_checkpoints
    -rw-r--r--  1 user_id users 133720 Mar 21 09:07 notebook.ipynb
    -rw-r--r--  1 user_id users 135799 Mar 21 09:21 notebook.nbconvert.ipynb
    -rwxr-xr-x  1 user_id users    238 Mar 21 09:16 slurm_jupyter_job.sh
    -rwxr-xr-x  1 user_id users    143 Mar 21 09:19 slurm_jupyter_job.sh.container_wrap

which you can then open and view the result of in the JupyterLab interface in MODI.


Running an OpenMPI job
----------------------

To execute an OpenMPI job via the ``modi-new-job`` CLI tool, you will need to adjust the default job runner that the tool uses to execute the job file.
Specifically, the ``--job-runner``/``-jr`` argument must be set to the mpi command that you want to use to execute the job file.

For example, if you want to run the following Hello World OpenMPI C program on MODI::

        #include <stdio.h>
        #include <mpi.h>

        int main(int argc, char** argv) {
            MPI_Init(&argc, &argv);

            // setup size
            int world_size;
            MPI_Comm_size(MPI_COMM_WORLD, &world_size);

            // setup rank
            int world_rank;
            MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

            // get name
            char processor_name[MPI_MAX_PROCESSOR_NAME];

            int name_len;
            MPI_Get_processor_name(processor_name, &name_len);
            // output combined id
            printf("Hello world from processor %s, "
                "rank %d out of %d processors\n", processor_name , world_rank , world_size);
            MPI_Finalize();
        }

After having succesfully compiled the code, you will be able to submit the job via the ``modi-new-job`` CLI tool by creating
a job executable script such as::

    ~/modi_mount/openmpi_example$ cat openmpi_job.sh
    #!/bin/bash
    #SBATCH --nodes=2
    #SBATCH --ntasks=2

    ./main

Ensure that the script file is executable::

    ~/modi_mount/openmpi_example$ chmod +x openmpi_job.sh

And then finally submit the job to the SLURM sbatch queue via the ``modi-new-job`` CLI tool::

    ~/modi_mount/openmpi_example$ modi-new-job --job-runner mpirun --generate-job-scripts --generate-container-wrap openmpi_job.sh
    Submitted batch job 1278

You can also use the short form of these arguments to achive the same result:::

    ~/modi_mount/openmpi_example$ modi-new-job -jr mpirun -gjs -gcw openmpi_job.sh
    Submitted batch job 1279
