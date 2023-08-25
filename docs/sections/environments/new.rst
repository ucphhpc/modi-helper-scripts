Creating an Environment
=======================

To create new environments on MODI, the modi-helper-scripts provide the following CLI tool::

    $ modi-new-environment --help
        Usage: modi-new-environment [OPTIONS] NAME

        Options:
        -dd, --destination-dir TEXT  The directory in which the environment will be
                                    created  [default:
                                    ~/modi_mount/my_conda_environments]
        -y, --automatic-yes          Whether the environment creation should
                                    automatically proceed without user input.
        -a, --activate               [default: True]
        -q, --quiet
        --extra-conda-args TEXT      Extra arguments to pass to conda
        -h, --help                   Show this message and exit.

As it shows in the help, the only required argument is the name of the environment to create.
The other arguments are optional.

The default destination directory where the new environment will be created is ``~/modi_mount/my_conda_environments``, but it can be changed with the ``--destination-dir`` argument.

The ``--automatic-yes`` argument is useful for scripting, as it will automatically answer yes to all questions asked by conda.

The ``--activate`` argument is used to specify whether the environment should be activated after creation. It is activated by default.

The ``--quiet`` argument is used to specify whether the output of conda should be hidden. It is shown by default.

The ``--extra-conda-args`` argument is used to specify extra arguments to pass to conda. It is empty by default.

Examples
--------

To create a new environment named ``my_env`` in the default directory, and activate it after creation::

    $ modi-new-environment my_env


To create a new environment named ``my_env`` in the default directory, and not activate it after creation::
    
    $ modi-new-environment my_env --activate False
