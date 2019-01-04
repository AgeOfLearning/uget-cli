import os
import re
import sys
import tempfile
import shutil
import click
from ugetcli import utils
from ugetcli.msbuild import MsBuildRunner
from ugetcli.nuget import NuGetRunner
from ugetcli.unitypackage import UnityPackageRunner
from ugetcli.nuspec import NuSpec
from ugetcli.csproj import CsProj


class UGetCli:
    """
    Main application module - uGet cli methods
    """
    UNITYPACKAGE_FORMAT = "{name}_{version}_{configuration}.unitypackage"
    UNITYPACKAGE_REGEX = "(.*)_(.*)_(.*).unitypackage"

    def __init__(self, debug, quiet):
        self.debug = debug
        self.quiet = quiet

    def build(self, csproj_path, configuration, msbuild_path, rebuild):
        """
        Builds C Sharp project (.csproj). Simply wraps msbuild command.
        :param path: Path to the .csproj or a directory containing one
        :param configuration: Build configuration - Debug/Release
        :param msbuild_path: Path to the msbuild executable
        :param rebuild: If set, forces msbuild to rebuild the project
        :return:
        """
        csproj_path = self._locate_csproj_at_path(csproj_path)
        msbuild_path = self._locate_msbuild_path(msbuild_path)
        msbuild = MsBuildRunner(msbuild_path, self.debug)
        return msbuild.build(csproj_path, configuration, rebuild)

    def create(self, csproj_path, output_dir, configuration, unity_project_path,
               root_dir, assembly_relative_dir, clean):
        """
        Creates .unitypackage that contains project assembly and assets
        :param path: Path to .csproj
        :param output_dir: Output directory into which .unitypackage is being built
        :param configuration: Debug or Release
        :param unity_project_path: Path to the unity project used to build .unitypackage
        :param root_dir: Root path inside a unity_project_path used to export .unitypackage
        :param assembly_relative_dir: Relative path from $unity_project_path/$root_dir to export assemblies.
        :param clean: If set, other Unity Packages will be removed from the output folder if they match configuration
        """
        csproj = CsProj(csproj_path)

        # Read csproj properties - assembly name, version and output directory
        assembly_name = csproj.get_assembly_name()
        if not assembly_name:
            raise click.UsageError("Failed to identify package id.")

        version = csproj.get_assembly_version()
        if not version:
            raise click.UsageError("Failed to identify package version.")

        csproj_dir_path = os.path.dirname(csproj.path)
        csproj_output_dir = os.path.join(csproj_dir_path, csproj.get_output_path(configuration))
        if not csproj_output_dir or not os.path.isdir(csproj_output_dir):
            raise click.UsageError('Output directory {0} not found'.format(csproj_output_dir))

        dll_name = assembly_name + ".dll"
        pdb_name = assembly_name + ".pdb"

        dll_path = os.path.join(csproj_output_dir, dll_name)
        pdb_path = os.path.join(csproj_output_dir, pdb_name)

        # Copy output dll and pdb into unity project folder
        if not os.path.isfile(dll_path):
            raise RuntimeError('Assembly not found at path {0}. Did you forget to build the project?'.format(dll_path))
        if not os.path.isfile(pdb_path):
            raise RuntimeError('Debug symbols not found at path {0}. Make sure project is set up to generate debug '
                               'symbols.'.format(pdb_path))

        if not root_dir:
            root_dir = assembly_name

        unitypackage_export_root = self._get_unity_package_export_root(unity_project_path, root_dir)
        assembly_export_root = os.path.join(unitypackage_export_root, assembly_relative_dir)

        if not os.path.exists(unitypackage_export_root):
            os.makedirs(unitypackage_export_root)
        elif not os.path.isdir(unitypackage_export_root):
            raise IOError("Can't copy assembly into Unity Project; path is not a valid directory: {0}"
                          .format(unitypackage_export_root))

        shutil.copyfile(dll_path, os.path.join(assembly_export_root, dll_name))
        shutil.copyfile(pdb_path, os.path.join(assembly_export_root, pdb_name))

        # Copy unity project folder into a temporary build location
        unitypackage_name = self.UNITYPACKAGE_FORMAT.format(name=assembly_name, version=version,
                                                            configuration=configuration)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        unitypackage_path = os.path.join(output_dir, unitypackage_name)

        # Create .unitypackage
        unity_runner = UnityPackageRunner(self.debug)
        click.secho("Exporting Unitypackage: {0}".format(unitypackage_name))
        unity_runner.export_unitypackage(unitypackage_export_root, unitypackage_path)

        if not os.path.isfile(unitypackage_path):
            raise RuntimeError("UnityPackage not found at path: " + unitypackage_path)
        click.secho("Unity package has successfully been built: " + unitypackage_path)

        # If clean flag is provided, remove other unity packages located at the output directory
        if clean:
            self._remove_old_unitypackages(output_dir, assembly_name, configuration, version)

    def pack(self, path, output_dir, nuget_path, unitypackage_path, configuration, unity_project_path, unitypackage_root_path_relative):
        """
        Packs NuGet Package.
        :param path: Path to the .csproj or .nuspec, or a directory containing either
        :param output_dir: Output directory - this is where .nupkg file will be built
        :param nuget_path: Path to the NuGet executable
        :param unitypackage_path: Path to the .unitypackge
        :param configuration: Configuration - Debug/Release
        :return: Exit code of the NuGet Pack command
        """
        # Locate nuget executable
        nuget_path = self._locate_nuget_path(nuget_path)
        nuget_runner = NuGetRunner(nuget_path, self.debug)

        # Locate project name and version
        csproj_file_path = CsProj.get_csproj_at_path(path)
        if csproj_file_path is not None:
            csproj = CsProj(path, self.debug)
            package_id = csproj.get_assembly_name()
            version = csproj.get_assembly_version()
        else:
            nuspec_file_path = NuSpec.get_nuspec_at_path(path)
            if nuspec_file_path is not None:
                nuspec = NuSpec(path, self.debug)
                package_id = nuspec.get_package_id()
                version = nuspec.get_package_version()
            else:
                raise click.UsageError("Path must be a valid path to .nuspec, .csproj, or directory containing either")

        if not package_id:
            raise click.UsageError("Failed to identify package id.")
        if not version:
            raise click.UsageError("Failed to identify package version.")

        if not unitypackage_path:
            unitypackage_name = utils.get_unitypackage_filename(package_id, version, configuration)
            unitypackage_path = os.path.join(output_dir, unitypackage_name)

        if not unitypackage_root_path_relative:
            unitypackage_root_path_relative = package_id

        unitypackage_export_root = self._get_unity_package_export_root(unity_project_path, unitypackage_root_path_relative)

        return nuget_runner.pack(path, output_dir, configuration, unitypackage_path, unitypackage_export_root)

    def push(self, path, output_dir, feed, nuget_path, api_key):
        """
        Pushes NuGet package on to the NuGet feed.
        :param path: Path to the NuGet Package
        :param output_dir: Output directory in which NuGet package will be searched, if it's not explicitly provided.
        :param feed: NuGet feed URI
        :param nuget_path: Path to the NuGet executable
        :param api_key: NuGet Api Key
        :return: Exit code of the NuGet push command
        """
        nupkg_path = self._locate_nupkg_at_path(path, output_dir)
        nuget_path = self._locate_nuget_path(nuget_path)
        nuget = NuGetRunner(nuget_path, self.debug)
        return nuget.push(nupkg_path, feed, api_key)

    def _get_unity_package_export_root(self, unity_project_path, unitypackage_root_path_relative):
        """
        Generates the path of the folder to export as unitypackage.
        :param package_id:
        :param unity_project_path:
        :param unitypackage_root_path_relative:
        :return:
        """
        if not unitypackage_root_path_relative.startswith("Assets" + os.sep):  # Package root should always start with "Assets/"
            unitypackage_root_path_relative = os.path.join("Assets", unitypackage_root_path_relative)

        return os.path.join(unity_project_path, unitypackage_root_path_relative)

    def _locate_msbuild_path(self, msbuild_path):
        """
        Locates mbuild executable path from user input or MsBuild facade.
        @:raises click.UsageError
        """
        # If Msbuild path is provided, check if it's valid
        if msbuild_path:
            if not MsBuildRunner.valid_msbuild_executable(msbuild_path):
                raise click.UsageError(msbuild_path + " is not a valid msbuild executable.")
            else:
                return msbuild_path

        # Msbuild path was not provided, locate
        msbuild_path = MsBuildRunner.locate_msbuild()
        if msbuild_path:
            return msbuild_path

        if not self.quiet:
            click.secho('Failed to locate msbuild executable.')
            click.secho('You can install msbuild as part of the Visual Studio package: '
                        'https://visualstudio.microsoft.com/vs/')
        raise click.UsageError('Failed to locate msbuild executable.')

    def _locate_nuget_path(self, nuget_path):
        """
        Locates NuGet executable path from user input or NuGet facade.
        @:raises click.UsageError
        """
        # If NuGet path is provided, check if it's valid
        if nuget_path:
            if not NuGetRunner.valid_nuget_executable(nuget_path):
                raise click.UsageError(nuget_path + " is not a valid NuGet executable.")
            else:
                return nuget_path

        # NuGet is not provided, locate
        nuget_path = NuGetRunner.locate_nuget()
        if nuget_path:
            return nuget_path

        # Failed to locate
        if not self.quiet:
            if sys.platform == 'win32':
                click.secho('You can install NuGet from the official website: https://www.nuget.org/downloads')
                click.secho('You might need to add NuGet installation folder to your PATH variable.')
            elif sys.platform == 'darwin':
                click.secho('You can install NuGet using Homebrew ("brew install nuget") or '
                            'download from the official website')
                click.secho('You might need to add NuGet installation folder to your PATH variable.')
        raise click.UsageError('Failed to locate NuGet executable.')

    def _locate_nupkg_at_path(self, path, output_dir):
        """
        Finds .nupkg file.
        If no explicit path to the .nupkg file is provided, .csproj file will be searched for in path.
        .csproj will be used to determine name and version of the package, while package itself will be seached
        in the output_dir.
        """
        if path.endswith(".nupkg"):
            if not os.path.isfile(path):
                raise click.FileError(path)
            return path

        csproj_path = CsProj.get_csproj_at_path(path)

        if not csproj_path:
            raise click.UsageError("Failed to find Nuget Package (.nupkg) or Visual Studio project at path " + path)

        csproj = CsProj(csproj_path)

        assembly_name = csproj.get_assembly_name()
        version = csproj.get_assembly_version()

        nupkg_filename = "{0}.{1}.nupkg".format(assembly_name, version)
        nupkg_path = os.path.normpath(os.path.join(output_dir, nupkg_filename))

        if not os.path.isfile(nupkg_path):
            raise click.UsageError("Failed to find Nuget Package (.nupkg) or Visual Studio project at path " + path)

        return nupkg_path

    def _locate_csproj_at_path(self, path):
        """
        Finds .csproj file at the provided path
        :param path:
        :return:
        """
        if path.endswith(".csproj"):
            if not os.path.isfile(path):
                raise click.FileError(path)
            return path

        csproj_path = CsProj.get_csproj_at_path(path)

        if not csproj_path:
            raise click.UsageError("Failed to find Nuget Package (.nupkg) or Visual Studio project at path " + path)

        return csproj_path

    def _get_ignore_unityproject_patterns(self):
        """
        Returns shutils ignore patterns to exclude lock files from unity project
        :return: Ignore patterns
        """
        return shutil.ignore_patterns("UnityLockfile", "db.lock")

    def _remove_old_unitypackages(self, directory, name, configuration, except_version=None):
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

                if name == package_name and configuration == package_configuration and \
                    (except_version is None or package_version != except_version):
                    unitypackage_path = os.path.join(directory, filename)
                    os.remove(unitypackage_path)
                    click.secho("Removed old .unitypackage at " + unitypackage_path)
