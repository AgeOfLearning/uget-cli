import os
import json
import click
from ugetcli.uget import UGetCli


# Helper method for a command and pre-load value from the config file
def _create_command_class(config_option_key, config_path_option_key):
    """Creates click.Command subclass that overrides values from config file at the provided path
    :param config_option_key: Option key for config json
    :param config_path_option_key: Option key for config json file path
    :return: Copy of UGetCommand class
    """
    class UGetCommand(click.Command):
        def invoke(self, ctx):
            config_data = {}

            # Read file first
            config_file_path = ctx.params[config_path_option_key] or "uget.config.json"
            if os.path.isfile(config_file_path):
                with open(config_file_path) as f:
                    try:
                        data = json.load(f)
                    except ValueError:
                        raise click.BadOptionUsage(config_option_key, "Failed to deserialize json from " + config_file_path)
                    config_data.update(data)

            # Read from json string
            if config_option_key in ctx.params and ctx.params[config_option_key] is not None:
                config_json = ctx.params[config_option_key]
                try:
                    data = json.loads(config_json)
                except ValueError:
                    raise click.BadOptionUsage(config_option_key, "Failed to deserialize config json.")
                config_data.update(data)

            # Update command values
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
@ugetcli.command('build', cls=_create_command_class('config', 'config_path'),
                 help='Builds CSharp project (.csproj)')
@click.option('-p', '--path', type=click.Path(), default=".",
              help="Path to Visual Studio project (.csproj).")
@click.option('-c', '--configuration', type=click.Choice(['Debug', 'Release']), default='Release',
              help='Build configuration.')
@click.option('-m', '--msbuild-path', type=click.Path(), default=None, envvar='MSBUILD_PATH',
              help="Path to msbuild executable.")
@click.option('-r', '--rebuild', is_flag=True, default=False,
              help="If set, cleans project before rebuilding.")
@click.option('--config', type=click.Path(), help="Config json.")
@click.option('--config-path', type=str, help="Config json.")
@click.option('-d', '--debug', is_flag=True, help="Enable verbose debug.")
@click.option('-q', '--quiet', is_flag=True, help="Does not prompt for user input and hides extra info messages.")
@click.pass_context
def build(ctx, path, configuration, msbuild_path, rebuild, config, config_path, debug, quiet):
    uget = UGetCli(debug, quiet)
    return uget.build(path, configuration, msbuild_path, rebuild)


@ugetcli.command('create', cls=_create_command_class('config', 'config_path'),
                 help='Creates Unity Package (.unitypackage)')
@click.option('-p', '--path', type=click.Path(), default=".",
              help="Path to Visual Studio project (.csproj).")
@click.option('-o', '--output-dir', type=click.Path(), default='Output',
              help='Output .unitypackage directory.')
@click.option('-c', '--configuration', type=click.Choice(['Debug', 'Release']), default='Release',
              help='Build configuration.')
@click.option('-u', '--unity-path', type=click.Path(), default=None, envvar='UNITY_PATH',
              help='Path to Unity editor executable.')
@click.option('-t', '--unity-project-path', type=click.Path(), default="UnityProject",
              help='Path to the Unity project used to build .unitypackage. Project can contain optional assets.')
@click.option('-r', '--root-dir', type=click.Path(), default=None,
              help="Root directory inside the Unity Project into which assembly is copied. Used to export .unitypackage"
                   "If not provided, project name is used.")
@click.option('-c', '--clean', is_flag=True,
              help="If set, cleans other .unitypackage files with the same configuration at the output location.")
@click.option('--unity-username', type=str, default=None, envvar='UNITY_USERNAME',
              help='Username passed into Unity command line.')
@click.option('--unity-password', type=str, default=None, envvar='UNITY_PASSWORD',
              help='Username passed into Unity command line.')
@click.option('--unity-serial', type=str, default=None, envvar='UNITY_SERIAL',
              help='Username passed into Unity command line.')
@click.option('--config', type=click.Path(), help="Config json.")
@click.option('--config-path', type=str, help="Config json.")
@click.option('-d', '--debug', is_flag=True, help="Enable verbose debug.")
@click.option('-q', '--quiet', is_flag=True, help="Does not prompt for user input and hides extra info messages.")
@click.pass_context
def create(ctx, path, output_dir, configuration, unity_path, unity_project_path, root_dir, clean,
          unity_username, unity_password, unity_serial, config, config_path, debug, quiet):
    if not unity_path:
        raise click.BadOptionUsage("Unity path must be present. Please use -u/--unity-path option or set UNITY_PATH "
                                   "env variable")
    uget = UGetCli(debug, quiet)
    return uget.create(path, output_dir, configuration, unity_path, unity_project_path, root_dir, clean,
                       unity_username, unity_password, unity_serial)


@ugetcli.command('pack', cls=_create_command_class('config', 'config_path'),
                 help='Packs NuGet package (.nupkg) using NuGet. Includes Unity Package (.unitypackage) into it.')
@click.option('-p', '--path', type=click.Path(), default='.',
              help='Path to Visual Studio project (.csproj) or .nuspec file.')
@click.option('-o', '--output-dir', type=click.Path(), default='Output',
              help='Output NuGet package directory.')
@click.option('-n', '--nuget-path', type=click.Path(), default=None, envvar='NUGET_PATH',
              help='Path to NuGet executable.')
@click.option('-u', '--unitypackage-path', type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
              default=None, help='Path to .unitypackage.')
@click.option('-c', '--configuration', type=click.Choice(['Debug', 'Release']), default='Release',
              help='Build configuration.')
@click.option('--config', type=click.Path(), help="Config json.")
@click.option('--config-path', type=str, help="Config json.")
@click.option('-d', '--debug', is_flag=True, help="Enable verbose debug.")
@click.option('-q', '--quiet', is_flag=True, help="Does not prompt for user input and hides extra info messages.")
@click.pass_context
def pack(ctx, path, output_dir, nuget_path, unitypackage_path, configuration, config, config_path, debug, quiet):
    uget = UGetCli(debug, quiet)
    return uget.pack(path, output_dir, nuget_path, unitypackage_path, configuration)


@ugetcli.command('push', cls=_create_command_class('config', 'config_path'),
                 help='Push uGet Package (.nupkg) to the NuGet feed.')
@click.option('-p', '--path', type=click.Path(), default='.',
              help='Path to NuGet Package (.nupkg) or Visual Studio project.')
@click.option('-o', '--output-dir', type=click.Path(), default='.',
              help='Provides directory in which Nuget Package is being looked for. '
                   'Used only if path is a .csproj or a directory that contains one (optional).')
@click.option('-f', '--feed', type=str,
              help='NuGet Feed URL')
@click.option('-n', '--nuget-path', type=click.Path(), default=None, envvar='NUGET_PATH',
              help='Path to nuget executable.')
@click.option('-a', '--api-key', type=str, default=None, envvar='NUGET_API_KEY',
              help='NuGet Api Key.')
@click.option('--config', type=click.Path(), help="Config json.")
@click.option('--config-path', type=str, help="Config json.")
@click.option('-d', '--debug', is_flag=True, help="Enable verbose debug.")
@click.option('-q', '--quiet', is_flag=True, help="Does not prompt for user input and hides extra info messages.")
@click.pass_context
def push(ctx, path, output_dir, feed, nuget_path, api_key, config, config_path, debug, quiet):
    uget = UGetCli(debug, quiet)
    return uget.push(path, output_dir, feed, nuget_path, api_key)
