Loading Environments
====================

When creating environements via the ``modi-new-environment`` tool,
the environment is installed into a predetermined destination directory,
that is either the defined default (As shown here) or a custom user specified path.

Therefore, when starting a new session on MODI, the underlying environment manager, such
as conda might not be aware of the custom directory where the environment was installed.

To mitigate this, the ``modi-helper-scripts`` provide the ``modi-load-environments`` tool
to inform the environment manager that it should load any available environment from a specified directory::

    $ modi-load-environments --help
        Usage: modi-load-environments [OPTIONS]

        Options:
        -ed, --environment-dir TEXT  The directory in which the environments are
                                    located.  [default:
                                    ~/modi_mount/my_conda_environments]
        -q, --quiet
        --extra-conda-args TEXT      Extra arguments to pass to conda
        -h, --help                   Show this message and exit.

The ``-ed`` argument as explained in the help message can be used to specify which
directory the tool should try to load environments from.
