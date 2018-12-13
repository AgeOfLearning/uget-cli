import os
import click
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

    def __init__(self, unity_path, unity_username=None, unity_password=None, unity_serial=None, debug=False):
        self.unity_path = unity_path
        self.unity_username = unity_username
        self.unity_password = unity_password
        self.unity_serial = unity_serial
        self.debug = debug

    def export_unitypackage(self, project_path, package_root, output_path, log_directory):
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        editor_log_path = os.path.join(log_directory, UnityRunner.log_filename)
        stdout_log_path = os.path.join(log_directory, UnityRunner.stdout_filename)
        stderr_log_path = os.path.join(log_directory, UnityRunner.stderr_filename)

        arguments = ["-projectPath", project_path,
                     "-exportPackage", package_root, os.path.abspath(output_path),
                     "-logFile", editor_log_path,
                     "-batchmode",
                     "-quit"]

        if self.unity_username:
            arguments.extend(["-username", self.unity_username])

        if self.unity_password:
            arguments.extend(["-password", self.unity_password])

        if self.unity_serial:
            arguments.extend(["-serial", self.unity_serial])

        unity_exitcode = self._run_editor(arguments, stdout_log_path, stderr_log_path)

        if self.debug and unity_exitcode != 0:
            click.secho("Unity failed to run, printing log files contents in --debug mode")
            self._debug_print_unity_logs(editor_log_path, stderr_log_path, stderr_log_path)

        return unity_exitcode

    def _run_editor(self, options, stdout_log_path, stderr_log_path):
        command_list = [self.unity_path] + options
        if self.debug:
            command_str = " ".join(command_list)
            click.secho("Running " + command_str)

        with open(stdout_log_path, "wb") as stdout, open(stderr_log_path, "wb") as stderr:
            process = Popen(command_list, stderr=stderr, stdout=stdout)
            return process.wait()

    @staticmethod
    def _debug_print_unity_logs(editor_log_path, stdout_log_path, stderr_log_path):
        UnityRunner._debug_print_unity_log(editor_log_path)
        UnityRunner._debug_print_unity_log(stdout_log_path)
        UnityRunner._debug_print_unity_log(stderr_log_path)

    @staticmethod
    def _debug_print_unity_log(log_path):
        click.secho("Begin log file contents " + log_path + ": ------------------------------")
        with open(log_path, "r") as logfile:
            for line in logfile:
                print(line)
        click.secho("End log file contents " + log_path + ": --------------------------------")

