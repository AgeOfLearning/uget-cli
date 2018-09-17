# -*- coding: utf-8 -*-

"""Console script for ugetcli."""
import sys
import click
import nuget
import os
import utils
import csproj


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.option('-q', '--quiet', type=bool, default=False)
@click.pass_context
def cli(ctx, debug, quiet):
    ctx.obj['DEBUG'] = debug
    ctx.obj['QUIET'] = quiet


@cli.command('build', help='Builds Unity Package (.unitypackage)')
@click.pass_context
def build(ctx):
    click.echo("building...")
    return 0


@cli.command('pack', help='Packs Unity Package (.unitypackage) into uGet package (.nupkg) using NuGet')
@click.option('-p', '--path', type=click.Path(), default=".", help='Path to Visual Studio project or .nuspec file.')
@click.option('-o', '--output-dir', type=click.Path(), default='.', help='Output NuGet package directory.')
@click.option('-n', '--nuget-path', type=click.Path(), default=None, envvar='NUGET_PATH', help='Path to nuget executable.')
@click.option('-u', '--unitypackage-path', type=click.File(), default=None, help='Path to .unitypackage.')
@click.option('-c', '--configuration', type=click.Choice(['Debug', 'Release']), default='Debug', help='Build configuration.')
@click.pass_context
def pack(ctx, path, output_dir, nuget_path, unitypackage_path, configuration):
    debug, quiet = ctx.obj['DEBUG'], ctx.obj['QUIET']

    if not csproj.get_nuspec_at_path(path) and not csproj.get_csproj_at_path(path):
        raise click.UsageError('path must be a valid path to .csproj file, .nuspec file, '
                               'or a directory containing either')
    # Locate nuget executable
    if not nuget_path:
        nuget_path = _locate_nuget_path(quiet)

    # Locate built .unitypackage
    if not unitypackage_path:
        package_id = csproj.get_package_id(path)
        version = csproj.get_package_version(path)
        if not package_id:
            raise click.UsageError("Failed to identify package id.")
        if not version:
            raise click.UsageError("Failed to identify package version.")

        unitypackage_name = utils.get_unitypackage_filename(package_id, version, configuration)
        unitypackage_path = os.path.join(path, 'Output', unitypackage_name)

    return nuget.pack(path, nuget_path, output_dir, unitypackage_path, configuration, debug)


@cli.command('push', help='Push uGet Package (.nupkg) to the NuGet feed.')
@click.option('-p', '--path', type=click.Path(), required=True, help='Path to NuGet Package (.nupkg) or Visual Studio project.')
@click.option('-f', '--feed', type=str, callback=utils.validate_url_param, help='NuGet Feed URL')
@click.option('-n', '--nuget-path', type=click.Path(), default=None, envvar='NUGET_PATH', help='Path to nuget executable.')
@click.option('-a', '--api-key', type=str, default=None, envvar='NUGET_API_KEY', help='NuGet Api Key.')
@click.pass_context
def push(ctx, path, feed, nuget_path, api_key):
    debug, quiet = ctx.obj['DEBUG'], ctx.obj['QUIET']

    nupkg_path = _get_nupkg_at_path(path)

    # Locate nuget executable
    if not nuget_path:
        nuget_path = _locate_nuget_path(quiet)

    return nuget.push(nupkg_path, nuget_path, feed, api_key, debug)


def _locate_nuget_path(quiet=False):
    """ Locates nuget executable path from user input or nuget facade. Throws exception when fails to locate """
    nuget_path = nuget.locate_nuget()
    if not nuget_path and not quiet:
        click.secho("NuGet executable not found.", blink=True, bold=True)
        nuget_path = click.prompt("Path to NuGet executable: ")
        if nuget_path and nuget.valid_nuget_executable(nuget_path):
            os.environ['NUGET_PATH'] = nuget_path

    if not nuget_path or not nuget.valid_nuget_executable(nuget_path):
        raise click.UsageError(nuget_path + " is not a valid NuGet executable.")
    return nuget_path


def _get_nupkg_at_path(path):
    """
    Finds .nupkg file at the provided path.
    If fails, finds .csproj and tries to locate most recent nuget package
    """
    if path.endswith(".nupkg"):
        if not os.path.isfile(path):
            raise click.FileError(path)
        return path

    csproj_path = csproj.get_csproj_at_path(path)

    if not csproj_path:
        raise click.UsageError("Failed to find Nuget Package (.nupkg) or Visual Studio project at path " + path)

    package_id = csproj.get_package_id(path)
    version = csproj.get_package_version(path)

    nupkg_filename = "{0}.{1}.nupkg".format(package_id, version)
    nupkg_path = os.path.join(os.path.dirname(path), nupkg_filename)

    if not os.path.isfile(nupkg_path):
        raise click.UsageError("Failed to find Nuget Package (.nupkg) or Visual Studio project at path " + path)

    return nupkg_path


if __name__ == "__main__":
    sys.exit(cli(obj={}))  # pragma: no cover
