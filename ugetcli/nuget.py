import os
from subprocess import call, Popen
import click
from ugetcli.utils import escape_exe_path

"""
Helper module that provides access to NuGet methods
"""


class NuGetRunner:
    """
    Facade class that provides access to run NuGet executable
    """

    def __init__(self, nuget_path, debug=False):
        self.nuget_path = nuget_path
        self.debug = debug

    def pack(self, path, output_dir, configuration, unitypackage_path):
        """ Runs NuGet to pack NuGet package """
        nuget_properties = {
            "unityPackagePath": unitypackage_path,
            "Configuration": configuration
        }
        options = ["pack", path,
                   "-OutputDirectory", output_dir,
                   "-Properties", self._build_nuget_properties_str(nuget_properties),
                   "-Verbosity", "detailed" if self.debug else "normal"]
        return self._run_nuget(options)

    def push(self, path, source_url, api_key):
        """ Runs NuGet to push NuGet package to the provided feed """
        options = ["push", path,
                   "-Verbosity", "detailed" if self.debug else "normal"]
        if source_url:
            options += ["-Source", source_url]
        if api_key:
            options += ["-ApiKey", api_key]

        return self._run_nuget(options)

    def _run_nuget(self, options):
        nuget_path = escape_exe_path(self.nuget_path)
        command_str = " ".join([nuget_path] + options)
        if self.debug:
            click.secho("Running " + command_str)

        process = Popen(command_str, shell=True)
        return process.wait()

    @staticmethod
    def locate_nuget():
        """
        Attempts to find NuGet executable in the local filesystem
        """
        if NuGetRunner.valid_nuget_executable("nuget"):
            return "nuget"
        return None

    @staticmethod
    def valid_nuget_executable(nuget_path):
        """
        Returns True if path is a valid NuGet executable, otherwise False
        """
        with open(os.devnull, "w") as devnull:
            try:
                return call(escape_exe_path(nuget_path) + " help", shell=True, stderr=devnull, stdout=devnull) == 0
            except:
                return False

    @staticmethod
    def _build_nuget_properties_str(properties):
        """
        Builds NuGet compliant property list string
        Example: Property=Value;Property2=Value2
        """
        properties_strings = [str(k) + "=" + str(v) for (k, v) in properties.items()]  # key=value
        # Sorted is used to preserve consistency between python 2.7 and 3.6, mainly for unit testing purposes
        properties_joined = ";".join(sorted(properties_strings))  # key=value;key2=value2
        return properties_joined
