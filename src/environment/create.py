from utils.job import run


def create_environment(name, destination=None):
    command = ["conda", "create", "-n", name]
    if destination:
        command.extend(["-p", destination])
    return run(command)


def activate_environment(name):
    command = ["conda", "activate", name]
    return run(command)
