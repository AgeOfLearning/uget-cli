import os
import re
import sys
import utils
import tempfile
import shutil
import click
from msbuild import MsBuildRunner
from nuget import NuGetRunner
from unity import UnityRunner
from nuspec import NuSpec
from csproj import CsProj


class UGetCli:
    """
    Main application module - uGet cli methods
    """
    UNITYPACKAGE_FORMAT = "{name}_{version}_{configuration}.unitypackage"
    UNITYPACKAGE_REGEX = "(.*)_(.*)_(.*).unitypackage"

    def __init__(self, debug, quiet):
        self.debug = debug
        self.quiet = quiet

    def build(self, csproj_path, output_dir, configuration, msbuild_path, unity_path, unity_project_path,
              unitypackage_root, clean):
        """Builds .unitypackage that contains project assembly and assets
        :param path: Path to .csproj
        :param output_dir: Output directory into which .unitypackage is being built
        :param configuration: Debug or Release
        :param msbuild_path: Path to msbuild executable
        :param unity_path: Path to the Unity editor executable
        :param unity_project_path: Path to the unity project used to build .unitypackage
        :param unitypackage_root: Root path inside a unity_project_path used to export .unitypackage
        :param clean: If set, other Unity Packages will be removed from the output folder if they match configuration
        :return:
        """
        csproj = CsProj(csproj_path)

        # Read csproj properties - assembly name, version and output direcotry
        assembly_name = csproj.get_assembly_name()
        if not assembly_name:
            raise click.UsageError("Failed to identify package id.")

        version = csproj.get_assembly_version()
        if not version:
            raise click.UsageError("Failed to identify package version.")

        csproj_output_dir = csproj.get_output_path(configuration)
        if not os.path.isdir(csproj_output_dir):
            raise click.UsageError('Output directory {0} not found'.format(csproj_output_dir))

        dll_path = os.path.join(csproj_output_dir, assembly_name + ".dll")
        pdb_path = os.path.join(csproj_output_dir, assembly_name + ".pdb")

        # Build csproj using msbuild
        # Should perform "if not os.path.isfile(dll_path):" ?
        self._build_csproj(msbuild_path, csproj_path, configuration)

        # Copy output dll and pdb into unity project folder
        if not os.path.isfile(dll_path):
            raise RuntimeError('Assembly not found at path {0}'.format(dll_path))
        if not os.path.isfile(pdb_path):
            raise RuntimeError('Assembly symbols not found at path {0}'.format(pdb_path))

        unitypackage_export_root = os.path.join(unity_project_path, unitypackage_root)
        shutil.copyfile(dll_path, os.path.join(unitypackage_export_root, dll_path))
        shutil.copyfile(pdb_path, os.path.join(unitypackage_export_root, pdb_path))

        # Copy unity project folder into a temporary build location
        unitypackage_name = self.UNITYPACKAGE_FORMAT.format(assembly_name, version, configuration)
        unitypackage_path = os.path.join(output_dir, unitypackage_name)

        with utils.temp_dir() as temp_dir:
            # Clone output into temp directory that will guaranteed to be removed
            unity_project_temp_path = os.path.join(temp_dir, os.path.dirname(unity_project_path))
            shutil.copytree(unity_project_path, unity_project_temp_path, ignore=self._get_ignore_unityproject_patterns())

            # Export .unitypackage
            logs_dir_path = tempfile.mkdtemp()  # Temporary directory that would not be removed after we are done
            unity_runner = UnityRunner(unity_path, self.debug)
            click.secho("Running Unity to build {0}".format(unitypackage_name))
            exit_code = unity_runner.export_unitypackage(unity_project_temp_path, unitypackage_root, unitypackage_path, logs_dir_path)
            if exit_code != 0:
                raise RuntimeError("Unity failed with non-zero exit code: " + str(exit_code) +
                                   ". Check log files located at: " + logs_dir_path)

            # Copy files back to the project
            shutil.copytree(unity_project_temp_path, unity_project_path, ignore=self._get_ignore_unityproject_patterns())

        # If clean flag is provided, remove other unity packages located at the output directory
        if clean:
            self._remove_old_unitypackages(output_dir, assembly_name, configuration)

    def pack(self, path, output_dir, nuget_path, unitypackage_path, configuration):
        # Locate nuget executable
        if not nuget_path:
            nuget_path = self._locate_nuget_path()
        nuget_runner = NuGetRunner(nuget_path, self.debug)

        # Locate project name and version
        if NuSpec.path_is_nuspec_file(path):
            nuspec = NuSpec(path, self.debug)
            package_id = nuspec.get_package_id()
            version = nuspec.get_package_version()
        elif CsProj.path_is_csproj_file(path):
            csproj = CsProj(path, self.debug)
            package_id = csproj.get_assembly_name()
            version = csproj.get_assembly_version()
        else:
            raise click.UsageError("path must be a valid path to .nuspec, .csproj, or directory containing either")

        if not unitypackage_path:
            if not package_id:
                raise click.UsageError("Failed to identify package id.")
            if not version:
                raise click.UsageError("Failed to identify package version.")

            unitypackage_name = utils.get_unitypackage_filename(package_id, version, configuration)
            unitypackage_path = os.path.join(path, 'Output', unitypackage_name)

        return nuget_runner.pack(path, output_dir, configuration, unitypackage_path)

    def push(self, path, feed, nuget_path, api_key):
        nupkg_path = self._locate_nupkg_at_path(path)
        if not nuget_path:
            nuget_path = self._locate_nuget_path()
        nuget = NuGetRunner(nuget_path)
        return nuget.push(nupkg_path, feed, api_key)

    def _locate_msbuild_path(self):
        """
        Locates mbuild executable path from user input or MsBuild facade.
        @:raises click.UsageError
        """
        msbuild_path = MsBuildRunner.locate_msbuild()
        if not msbuild_path and not self.quiet:
            click.secho('Failed to locate NuGet executable.')
            click.secho('You can install msbuild as part of the Visual Studio package: '
                        'https://visualstudio.microsoft.com/vs/')
            return -1
        if not msbuild_path or not MsBuildRunner.valid_msbuild_executable(msbuild_path):
            raise click.UsageError(msbuild_path + " is not a valid msbuild executable.")
        return msbuild_path

    def _locate_nuget_path(self):
        """
        Locates NuGet executable path from user input or NuGet facade.
        @:raises click.UsageError
        """
        nuget_path = NuGetRunner.locate_nuget()
        if not nuget_path and not self.quiet:
            click.secho('Failed to locate NuGet executable.')
            if sys.platform == 'win32':
                click.secho('You can install NuGet from the official website: https://www.nuget.org/downloads')
                click.secho('You might need to add NuGet installation folder to your PATH variable.')
            elif sys.platform == 'darwin':
                click.secho('You can install NuGet using Homebrew ("brew install nuget") or '
                            'download from the official website')
                click.secho('You might need to add NuGet installation folder to your PATH variable.')
            return -1
        if not nuget_path or not NuGetRunner.valid_nuget_executable(nuget_path):
            raise click.UsageError(nuget_path + " is not a valid NuGet executable.")
        return nuget_path

    def _locate_nupkg_at_path(self, path):
        """
        Finds .nupkg file at the provided path.
        If fails, finds .csproj and tries to locate most recent nuget package
        """
        if path.endswith(".nupkg"):
            if not os.path.isfile(path):
                raise click.FileError(path)
            return path

        csproj_path = CsProj.get_csproj_at_path(path)

        if not csproj_path:
            raise click.UsageError("Failed to find Nuget Package (.nupkg) or Visual Studio project at path " + path)

        assembly_name = CsProj.get_assembly_name(path)
        version = CsProj.get_assembly_version(path)

        nupkg_filename = "{0}.{1}.nupkg".format(assembly_name, version)
        nupkg_path = os.path.join(os.path.dirname(path), nupkg_filename)

        if not os.path.isfile(nupkg_path):
            raise click.UsageError("Failed to find Nuget Package (.nupkg) or Visual Studio project at path " + path)

        return nupkg_path

    def _get_ignore_unityproject_patterns(self):
        """
        Returns shutils ignore patterns to exclude lock files from unity project
        :return: Ignore patterns
        """
        return shutil.ignore_patterns("UnityLockfile", "db.lock")

    def _build_csproj(self, msbuild_path, csproj_path, configuration):
        """
        Builds .csproj file using msbuild
        :param msbuild_path: Path to msbuild executable
        :param csproj_path: Path to .csproj file or a directory containing one
        :param configuration: Build configuration
        :return:
        """
        if not msbuild_path:
            msbuild_path = self._locate_msbuild_path()
        msbuild = MsBuildRunner(msbuild_path, self.debug)
        exit_code = msbuild.build(csproj_path, configuration)
        if exit_code != 0:
            raise RuntimeError("msbuild failed with non-zero exit code: " + str(exit_code))

    def _remove_old_unitypackages(self, directory, name, configuration):
        """ Removes old .unitypackages with the same target name and configuration"""
        regex = re.compile(self.UNITYPACKAGE_REGEX)
        if os.path.isdir(directory):
            for filename in os.listdir(directory):
                match = regex.search(filename)
                match_valid = match and len(match.groups()) == 3
                if not match_valid:
                    continue

                package_name = match.group(1)
                package_version = match.group(2)
                package_configuration = match.group(3)

                if name == package_name and configuration == package_configuration:
                    os.remove(os.path.join(directory, filename))
