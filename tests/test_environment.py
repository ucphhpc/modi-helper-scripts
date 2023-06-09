# Generate a unit test file for the submit_job.py script.
import os
import unittest
from modi_helper.utils.job import run

TEST_RESOURCE_DIR = os.path.join(os.path.dirname(__file__), "res")


class TestNewEnvironment(unittest.TestCase):
    def setUp(self) -> None:
        self.new_environment_name = "test_environment"
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_new_environment(self):
        args = [
            "modi-new-environment",
            self.new_environment_name,
            "-d",
            TEST_RESOURCE_DIR,
            "-y",
        ]
        result = run(args, format_output_str=True)
        assert result["output"] == ""