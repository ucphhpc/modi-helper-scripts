Getting Started
===============

The modi-helper-scripts can be installed in a number of ways, including:

Via pypi::

    pip install modi-helper-scripts

Via the GitHub repository::

    pip install git+https://github.com/ucphhpc/modi-helper-scripts.git

Or via cloning and installing it yourself::

    git clone https://github.com/ucphhpc/modi-helper-scripts.git
    cd modi-helper-scripts
    make install

Either of these methods will install a number of CLI tools, all of which can typically be expanded in a shell environment, given that their installed
destination directory is included in your current PATH::

    $ modi-
    modi-delete-environment  modi-new-environment     modi-new-job
