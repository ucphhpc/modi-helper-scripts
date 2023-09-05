Deleting an Environment
=======================

To delete an environment on MODI, the ``modi-helper-scripts`` provide the ``modi-delete-environment`` CLI::

    modi-delete-environment --help
        Usage: modi-delete-environment [OPTIONS] NAME

        Options:
        -y, --automatic-yes BOOLEAN  Whether the environment deletion should
                                    automatically proceed without user input.
        -q, --quiet
        -h, --help                   Show this message and exit

As is shown here, the tool can be used to delete an environment created
with the ``modi-new-environment`` tool with support for a set of arguments.

Examples
--------

For instance, we could first create a python conda environment called ``my_env`` via::

    $ modi-new-environment my_env --activate False

The ``my_env`` environment can then be deleted via::

    $ modi-delete-environment my_env

