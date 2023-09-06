import os
import shutil


def makedirs(path):
    try:
        os.makedirs(expanduser(path))
        return True, "Created: {}".format(path)
    except IOError as err:
        return False, "Failed to create the directory path: {} - {}".format(path, err)


def write(path, content, mode="w", mkdirs=False):
    dir_path = os.path.dirname(path)
    if not exists(dir_path) and mkdirs:
        if not makedirs(dir_path):
            return False
    try:
        with open(path, mode) as fh:
            fh.write(content)
        return True
    except IOError as err:
        print("Failed to save file: {} - {}".format(path, err))
    return False


def copy(file_path, destination_directory):
    try:
        shutil.copy(file_path, destination_directory)
        return True
    except IOError as err:
        print("Failed to copy file: {} - {}".format(file_path, err))
    return False


def copy_recursive(source_directory, destination_directory):
    try:
        shutil.copytree(source_directory, destination_directory)
        return True
    except IOError as err:
        print("Failed to copy directory: {} - {}".format(source_directory, err))
    return False


def load(path, mode="r", readlines=False):
    try:
        with open(path, mode) as fh:
            if readlines:
                return fh.readlines()
            return fh.read()
    except IOError as err:
        print("Failed to load file: {} - {}".format(path, err))
    return False


def remove(path):
    try:
        if os.path.exists(path):
            os.remove(path)
            return True
    except IOError as err:
        print("Failed to remove file: {} - {}".format(path, err))
    return False


def removedirs(path):
    try:
        if os.path.exists(path):
            os.removedirs(path)
            return True
    except IOError as err:
        print("Failed to remove directory: {} - {}".format(path, err))
    return False


def recursive_remove(path):
    try:
        if os.path.exists(path):
            shutil.rmtree(path)
            return True
    except IOError as err:
        print("Failed to remove directory: {} - {}".format(path, err))
    return False


def exists(path):
    return os.path.exists(expanduser(path))


def normpath(path):
    return os.path.normpath(expanduser(path))


def expanduser(path):
    return os.path.expanduser(path)


def load_content(path):
    try:
        with open(path, "r") as fh:
            return fh.read()
    except IOError as err:
        print("Failed to read file: {} - {}".format(path, err))
    return False


def set_execute_permissions(path):
    try:
        os.chmod(path, 0o755)
        return True
    except IOError as err:
        print("Failed to set execute permissions on file: {} - {}".format(path, err))
    return False
