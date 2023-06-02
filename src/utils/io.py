import os


def makedirs(path):
    try:
        os.makedirs(expanduser(path))
        return True, "Created: {}".format(path)
    except Exception as err:
        return False, "Failed to create the directory path: {} - {}".format(path, err)
    return False, "Failed to create the directory path: {}".format(path)


def exists(path):
    return os.path.exists(expanduser(path))


def normpath(path):
    return os.path.normpath(expanduser(path))


def expanduser(path):
    return os.path.expanduser(path)
