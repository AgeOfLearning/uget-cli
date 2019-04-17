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

    def pack(self, path, output_dir, configuration, unitypackage_path, unitypackage_export_root, version):
        """ Runs NuGet to pack NuGet package """
        options = ["pack", path,
                   "-OutputDirectory", output_dir,
                   "-Version", version,
                   "-Verbosity", "detailed" if self.debug else "normal",
                   "-Properties", "\"unityPackagePath={0};unityPackageExportRoot={1};Configuration={2}\"".format(unitypackage_path, unitypackage_export_root, configuration)]

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
        command_list = [nuget_path] + options
        command_str = " ".join(command_list)
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
        properties_joined = ";".join(reversed(properties_strings))  # key=value;key2=value2
        return properties_joined

    @staticmethod
    def get_normalized_nuget_pack_version(version):
        """
        By default, nuget drops 4th digit if it's a 0
        This method does this so we can get correct nuget package name without parsing nuget tool output
        For more info, see:
        https://github.com/NuGet/Home/issues/5225
        https://github.com/NuGet/Home/issues/3050
        https://github.com/NuGet/Home/issues/2039
        :param version:
        :return: Normalized version, which nuget pack is expected to output
        """
        numbers = version.split(".")
        if len(numbers) < 4:
            return version  # No need to normalize
        elif len(numbers) > 4:
            raise click.UsageError("Invalid package version {0}. Package version can not contain more than 4 numbers.")
        elif numbers[3] == "0":
            return ".".join(numbers[:3])  # 4 numbers and last number is a zero, which we should drop
        else:
            return version  # No need to normalize
