import os


def makedirs(path):
    try:
        os.makedirs(expanduser(path))
        return True, "Created: {}".format(path)
    except Exception as err:
        return False, "Failed to create the directory path: {} - {}".format(path, err)
    return False, "Failed to create the directory path: {}".format(path)

def write(path, content, mode="w", mkdirs=False):
    dir_path = os.path.dirname(path)
    if not exists(dir_path) and mkdirs:
        if not makedirs(dir_path):
            return False
    try:
        with open(path, mode) as fh:
            fh.write(content)
        return True
    except Exception as err:
        print("Failed to save file: {} - {}".format(path, err))
    return False


def load(path, mode="r", readlines=False):
    try:
        with open(path, mode) as fh:
            if readlines:
                return fh.readlines()
            return fh.read()
    except Exception as err:
        print("Failed to load file: {} - {}".format(path, err))
    return False


def exists(path):
    return os.path.exists(expanduser(path))


def normpath(path):
    return os.path.normpath(expanduser(path))


def expanduser(path):
    return os.path.expanduser(path)
