import os
import sys
import glob
from subprocess import call, Popen

"""
Helper module that provides access to MSBuild methods
"""


class MsBuildRunner:
    """
    Facade class that provides access to run msbuild executable
    """
    def __init__(self, msbuild_path, debug=False):
        self.msbuild_path = msbuild_path
        self.debug = debug

    def build(self, project_path, configuration, clean=False):
        options = [
            project_path,
            '/p:"Configuration={0}"'.format(configuration),
            '/verbosity:{0}'.format("detailed" if self.debug else "normal")
        ]
        if clean:
            options.append('/t:Clean')

        return self._run_msbuild(options)

    def _run_msbuild(self, options):
        process = Popen([self.msbuild_path] + options, shell=True)
        return process.wait()

    @staticmethod
    def locate_msbuild():
        """
        Attempts to find msbuild executable in the local filesystem
        """
        # By default, Mono install on Windows might not have 3.5 target installed and mono msbuild would fail.
        # Attempt to find Visual Studio installation first, then fall back to msbuild from PATH
        if sys.platform == 'win32':
            # On windows, default msbuild locations are Visual Studio installation folder and .NET installation folder
            msbuild_search_patterns = [
                os.environ["ProgramFiles"] + "\\Microsoft Visual Studio\\*\\Community\\MSBuild\\*\\Bin\\MSBuild.exe",
                os.environ['WINDIR'] + "\\Microsoft.NET\\Framework\\*\\msbuild.exe"
            ]
            for pattern in msbuild_search_patterns:
                for location in glob.glob(pattern):
                    if MsBuildRunner.valid_msbuild_executable(location):
                        return location
        if MsBuildRunner.valid_msbuild_executable("msbuild"):  # Try from PATH
            return "msbuild"

        return None

    @staticmethod
    def valid_msbuild_executable(msbuild_path):
        """
        Returns True if path is a valid msbuild executable, otherwise False
        """
        with open(os.devnull, "w") as devnull:
            try:
                return call(msbuild_path + " /?", shell=True, stderr=devnull, stdout=devnull) == 0
            except FileNotFoundError:
                return False
