import os
import sys
import glob
from subprocess import call, DEVNULL, Popen

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

    def build(self, project_path, configuration):
        options = [
            project_path,
            '/p:"Configuration={0}"'.format(configuration),
            '/verbosity:{0}'.format("detailed" if self.debug else "normal")
        ]
        return self._run_msbuild(options)

    def _run_msbuild(self, options):
        process = Popen([self.msbuild_path] + options)
        return process.wait()

    @staticmethod
    def locate_msbuild():
        """
        Attempts to find msbuild executable in the local filesystem
        """
        if MsBuildRunner.valid_msbuild_executable("msbuild"):
            return "msbuild"
        if sys.platform == 'win32':
            # On windows, default msbuild locations are .NET installation folder and Visual Studio installation folder
            msbuild_search_patterns = [
                os.environ['WINDIR'] + "\\Microsoft.NET\\Framework\\*\\msbuild.exe",
                os.environ["ProgramFiles"] + "\\Microsoft Visual Studio\\*\\Community\\MSBuild\\*\\Bin\\MSBuild.exe"
            ]
            for pattern in msbuild_search_patterns:
                for location in glob.glob(pattern):
                    if MsBuildRunner.valid_msbuild_executable(location):
                        return location
        return None

    @staticmethod
    def valid_msbuild_executable(msbuild_path):
        """
        Returns True if path is a valid msbuild executable, otherwise False
        """
        try:
            return call(msbuild_path + " /?", shell=True, stderr=DEVNULL, stdout=DEVNULL) == 0
        except FileNotFoundError:
            return False
