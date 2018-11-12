import os
import json
import click
import csproj
import utils
import nuspec
from click import BadParameter
from uget import UGetCli


# Click Validators
def _validate_path_csproj(ctx, param, value):
    """ Checks if given parameter is a path to .csproj """
    if not csproj.CsProj.get_csproj_at_path(value):
        raise BadParameter('{0} must be a valid path to .csproj file, or a directory containing one')
    return value


def _validate_path_nupkg_or_csproj(ctx, param, value):
    """ Checks if given parameter is a path to .csproj or .nuspec """
    if not nuspec.NuSpec.get_nuspec_at_path(value) and not csproj.CsProj.get_csproj_at_path(value):
        raise BadParameter('{0} must be a valid path to .csproj file, .nuspec file, or a directory containing either')
    return value


def _validate_url_param(ctx, param, value):
    """ Checks if parameter is a URL """
    if utils.validate_url(value):
        return value
    raise BadParameter('Invalid url format')


# Helper method for a command
def _create_command_class(config_path_param_name, config_base_dir_param_name):
    """Creates click.Command subclass that overrides values from config file at the provided path
    :param config_path_param_name: Parameter name for config file path
    :param config_base_dir_param_name: Parameter name for base directory to which config path is relative.
    :return: Copy of UGetCommand class
    """
    class UGetCommand(click.Command):
        def invoke(self, ctx):
            config_file_path = ctx.params[config_path_param_name] or "build.config.json"
            config_file_base_dir = ctx.params[config_base_dir_param_name] or ""
            if not os.path.isabs(config_file_path):
                config_file_path = os.path.join(config_file_base_dir, config_file_path)
            if os.path.isfile(config_file_path):
                with open(config_file_path) as f:
                    config_data = json.load(f)
                    for param, value in ctx.params.items():
                        if param in config_data:
                            ctx.params[param] = config_data[param]
            return super(UGetCommand, self).invoke(ctx)
    return UGetCommand


# uGet Command Group
@click.group()
def ugetcli():
    pass


# uGet Commands
@ugetcli.command('build', cls=_create_command_class('config', 'path'),
                 help='Builds Unity Package (.unitypackage)')
@click.option('-p', '--path', type=click.Path(), default=".", callback=_validate_path_csproj,
              help="Path to Visual Studio project (.csproj).")
@click.option('-o', '--output-dir', type=click.Path(), default='Output',
              help='Output .unitypackage directory.')
@click.option('-c', '--configuration', type=click.Choice(['Debug', 'Release']), default='Release',
              help='Build configuration.')
@click.option('-m', '--msbuild-path', type=click.Path(), default=None, envvar='MSBUILD_PATH',
              help="Path to msbuild executable.")
@click.option('-u', '--unity-path', type=click.Path(), default=None, envvar='UNITY_PATH',
              help='Path to Unity editor executable.')
@click.option('-t', '--unity-project-path', type=click.Path(), default=None,
              help='Path to the Unity project used to build .unitypackage. Project can contain optional assets.')
@click.option('-r', '--root-directory', type=click.Path(), default=None,
              help="Root directory inside the Unity Project into which assembly is copied. Used to export .unitypackage"
                   "If not provided, project name is used.")
@click.option('-c', '--clean', is_flag=True,
              help="If set, cleans other .unitypackage files with the same configuration at the output location.")
@click.option('--config', type=click.Path(),
              help="Config file path.")
@click.option('-d', '--debug', is_flag=True, help="Enable verbose debug.")
@click.option('-q', '--quiet', is_flag=True, help="Does not prompt for user input and hides extra info messages.")
@click.pass_context
def build(ctx, path, output_dir, configuration, msbuild_path, unity_path, unity_project_path, root_directory, clean, config, debug, quiet):
    uget = UGetCli(debug, quiet)
    return uget.build(path, output_dir, configuration, msbuild_path, unity_path, unity_project_path, root_directory, clean)


@ugetcli.command('pack', cls=_create_command_class('config', 'path'),
                 help='Packs NuGet package (.nupkg) using NuGet. Includes Unity Package (.unitypackage) into it.')
@click.option('-p', '--path', type=click.Path(), default='.', callback=_validate_path_nupkg_or_csproj,
              help='Path to Visual Studio project (.csproj) or .nuspec file.')
@click.option('-o', '--output-dir', type=click.Path(), default='.',
              help='Output NuGet package directory.')
@click.option('-n', '--nuget-path', type=click.Path(), default=None, envvar='NUGET_PATH',
              help='Path to NuGet executable.')
@click.option('-u', '--unitypackage-path', type=click.File(), default=None,
              help='Path to .unitypackage.')
@click.option('-c', '--configuration', type=click.Choice(['Debug', 'Release']), default='Release',
              help='Build configuration.')
@click.option('--config', type=click.Path(),
              help="Config file path.")
@click.option('-d', '--debug', is_flag=True, help="Enable verbose debug.")
@click.option('-q', '--quiet', is_flag=True, help="Does not prompt for user input and hides extra info messages.")
@click.pass_context
def pack(ctx, path, output_dir, nuget_path, unitypackage_path, configuration, config, debug, quiet):
    uget = UGetCli(debug, quiet)
    return uget.pack(path, output_dir, nuget_path, unitypackage_path, configuration)


@ugetcli.command('push', cls=_create_command_class('config', 'path'),
                 help='Push uGet Package (.nupkg) to the NuGet feed.')
@click.option('-p', '--path', type=click.Path(), default='.',
              help='Path to NuGet Package (.nupkg) or Visual Studio project.')
@click.option('-f', '--feed', type=str, callback=_validate_url_param,
              help='NuGet Feed URL')
@click.option('-n', '--nuget-path', type=click.Path(), default=None, envvar='NUGET_PATH',
              help='Path to nuget executable.')
@click.option('-a', '--api-key', type=str, default=None, envvar='NUGET_API_KEY',
              help='NuGet Api Key.')
@click.option('--config', type=click.Path(),
              help="Config file path.")
@click.option('-d', '--debug', is_flag=True, help="Enable verbose debug.")
@click.option('-q', '--quiet', is_flag=True, help="Does not prompt for user input and hides extra info messages.")
@click.pass_context
def push(ctx, path, feed, nuget_path, api_key, config, debug, quiet):
    uget = UGetCli(debug, quiet)
    return uget.push(path, feed, nuget_path, api_key)
