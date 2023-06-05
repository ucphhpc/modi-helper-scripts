# Generate a unit test file for the submit_job.py script.
import os
import unittest
from modi_helper.utils.job import run
from modi_helper.utils.io import (
    write,
    remove,
    exists,
    makedirs,
    copy,
    recursive_remove,
)

TEST_RESOURCE_DIR = os.path.join(os.path.dirname(__file__), "res")


class TestSubmitJob(unittest.TestCase):
    def setUp(self):
        self.hello_world_job_file_name = "hello_world.sh"
        self.hello_world_python_name = "hello_world.py"

        self.hello_world_job_file = os.path.join(
            TEST_RESOURCE_DIR, self.hello_world_job_file_name
        )
        self.hello_world_python = os.path.join(
            TEST_RESOURCE_DIR, self.hello_world_python_name
        )

        # Create the runtime and scratch space directories
        self.test_scratch_space_directory = os.path.join(TEST_RESOURCE_DIR, "scratch")
        self.test_runtime_directory = os.path.join(
            self.test_scratch_space_directory, "runtime"
        )
        created, msg = makedirs(self.test_scratch_space_directory)
        self.assertTrue(created, msg)
        created, msg = makedirs(self.test_runtime_directory)
        self.assertTrue(created, msg)

        # Install the cli
        args = ["pip3", "install", ".", "-q"]
        result = run(args)
        self.assertIsNotNone(result)
        self.assertIn("returncode", result)
        self.assertEqual(result["returncode"], 0)
        return super().setUp()

    def tearDown(self):
        if exists(self.hello_world_job_file):
            assert remove(self.hello_world_job_file)
        if exists(self.hello_world_python):
            assert remove(self.hello_world_python)

        if exists(self.test_runtime_directory):
            self.assertTrue(recursive_remove(self.test_runtime_directory))
        if exists(self.test_scratch_space_directory):
            self.assertTrue(recursive_remove(self.test_scratch_space_directory))
        return super().tearDown()

    def test_submit_job(self):
        self.assertTrue(
            write(self.hello_world_job_file, "#!/bin/bash\necho 'Hello World!'")
        )
        self.assertTrue(copy(self.hello_world_job_file, self.test_runtime_directory))

        runtime_job_file_path = os.path.join(
            self.test_runtime_directory, self.hello_world_job_file_name
        )
        self.assertTrue(exists(runtime_job_file_path))

        args = [
            "modi-new-job",
            runtime_job_file_path,
            "--scratch-space-directory",
            self.test_scratch_space_directory,
            "--runtime-directory",
            self.test_runtime_directory,
        ]
        result = run(args, format_output_str=True)
        assert result["output"] == "Hello World!\n"

    def test_submit_job_with_generate_job_scripts(self):
        self.assertTrue(
            write(
                self.hello_world_python, "#!/usr/bin/env python3\nprint('Hello World!')"
            )
        )
        self.assertTrue(copy(self.hello_world_python, self.test_runtime_directory))

        runtime_job_file_path = os.path.join(
            self.test_runtime_directory, self.hello_world_python_name
        )
        self.assertTrue(exists(runtime_job_file_path))

        args = [
            "modi-new-job",
            runtime_job_file_path,
            "--generate-job-scripts",
            "--scratch-space-directory",
            self.test_scratch_space_directory,
            "--runtime-directory",
            self.test_runtime_directory,
        ]
        result = run(args, format_output_str=True)
        assert result["output"] == "Hello World!\n"
