import os


def makedirs(path):
    try:
        os.makedirs(os.path.expanduser(path))
        return True, "Created: {}".format(path)
    except Exception as err:
        return False, "Failed to create the directory path: {} - {}".format(path, err)
    return False, "Failed to create the directory path: {}".format(path)


def exists(path):
    return os.path.exists(os.path.expanduser(path))
