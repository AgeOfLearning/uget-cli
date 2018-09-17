import os
from subprocess import call, DEVNULL, Popen


def pack(path, nuget_path, output_dir, configuration, unitypackage_path, debug):
    """ Runs NuGet to pack NuGet package"""
    nuget_properties = {
        "unityPackagePath": unitypackage_path,
        "Configuration": configuration
    }
    options = ["pack", path,
               "-OutputDirectory", output_dir,
               "-Properties", _build_nuget_properties_str(nuget_properties),
               "-Verbosity", "detailed" if debug else "normal"]
    return _run_nuget(nuget_path, options)


def push(path, nuget_path, source_url, api_key, debug):
    """ Runs NuGet to push NuGet package to the provided feed """
    options = ["push", path,
               "-Verbosity", "detailed" if debug else "normal"]
    if source_url:
        options += ["-Source", source_url]
    if api_key:
        options += ["-ApiKey", api_key]

    return _run_nuget(nuget_path, options)


def locate_nuget():
    """ Attempts to find NuGet executable """
    if "NUGET_PATH" in os.environ and os.environ["NUGET_PATH"] and valid_nuget_executable(os.environ["NUGET_PATH"]):
        return os.environ["NUGET_PATH"]
    if valid_nuget_executable("nuget"):
        return "nuget"

    return None


def valid_nuget_executable(nuget_path):
    """ Returns True if path is a valid NuGet executable, otherwise False """
    try:
        return call(nuget_path + " help", shell=True, stderr=DEVNULL, stdout=DEVNULL) == 0
    except FileNotFoundError:
        return False


def _run_nuget(path, options):
    process = Popen([path] + options)
    return process.wait()


def _build_nuget_properties_str(properties):
    """
    Builds NuGet compliant property list string
    Example: Property=Value;Property2=Value2
    """
    properties_strings = [str(k)+"="+str(v) for (k, v) in properties.items()]  # key=value
    properties_joined = ";".join(properties_strings)  # key=value;key2=value2
    return properties_joined

