List Environments
=================

You can list the available set of environments via the ``modi-list-environments`` tool.
This will show you the current list of available environments.
To ensure that custom created environments, such as those created via ``modi-new-environment``, it is prudent
to run ``modi-load-environments`` to refresh the system about which enviornments that are available.

The usage of ``modi-list-environments`` can be seen below::

    $ modi-list-environments --help
        Usage: modi-list-environments [OPTIONS]

        Options:
        --extra-conda-args TEXT  Extra arguments to pass to conda
        -h, --help               Show this message and exit.
