import os
from subprocess import Popen

"""
Helper module that provides access to Unity methods
"""


class UnityRunner:
    """
    Facade module that provides access to Unity executable
    """
    log_filename = "unity.log"
    stdout_filename = "unity_stdout.log"
    stderr_filename = "unity_stderr.log"

    def __init__(self, unity_path, debug=False):
        self.unity_path = unity_path
        self.debug = debug

    def export_unitypackage(self, project_path, package_root, output_path, log_directory):
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        editor_log_path = os.path.join(log_directory, UnityRunner.log_filename)
        stdout_log_path = os.path.join(log_directory, UnityRunner.stdout_filename)
        stderr_log_path = os.path.join(log_directory, UnityRunner.stderr_filename)

        arguments = ["-projectPath", project_path,
                     "-exportPackage", package_root, output_path,
                     "-logFile", editor_log_path,
                     "-batchmode",
                     "-quit"]

        return self._run_editor(arguments, stdout_log_path, stderr_log_path)

    def _run_editor(self, options, stdout_log_path, stderr_log_path):
        with open(stdout_log_path, "wb") as stdout, open(stderr_log_path, "wb") as stderr:
            process = Popen([self.unity_path] + options, stderr=stderr, stdout=stdout)
            return process.wait()
