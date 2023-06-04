import os
from jinja2 import Template, Environment
import importlib.resources as pkg_resources
from . import templates
from utils.io import expanduser, write


def check_job_paths(runtime_directory, job_file):
    """The job_file must exist within the runtime_directory.
    If not, the cluster nodes will not be able to access it."""
    return expanduser(job_file).startswith(expanduser(runtime_directory))


def get_package_top_directory(package_name):
    package_module = __import__(package_name)
    package_file = package_module.__file__
    top_directory = os.path.dirname(package_file)
    return top_directory


def get_template_file(template_type):
    return pkg_resources.files(templates, template_type)

def make_job_script_content(template_file, template_kwargs=None):
    """Generate the job sripts based on the given template and its associated kwargs."""
    if not template_kwargs:
        return False

    # Make the wrapper script.
    templateLoader = Template.FileSystemLoader()
    templateEnv = Environment(loader=templateLoader)
    template = templateEnv.get_template(template_file)
    new_content = template.render(**template_kwargs)  # this is where to put args to the template renderer
    return new_content


def write_job_script(runtime_directory, name, content):
    """
    Generate the set of job scripts that are required to execute
    a given binary/program.
    """
    
    job_script_path = os.path.join(runtime_directory, name)
    return write(job_script_path, content, mode="w", mkdirs=True)
