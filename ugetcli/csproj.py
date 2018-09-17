import os
import re
import xml.etree.ElementTree as ET
import utils


def get_package_id(path):
    """
    Returns package id if path is a .nuspec file, .csproj file or a directory containing either.
    Otherwise, returns None
    """
    nuspec_file_path = get_nuspec_at_path(path)

    if nuspec_file_path:  # got .nuspec, try to read package id
        package_id = _get_nuspec_package_id(nuspec_file_path)
        if package_id:
            return package_id

    # try to read .csproj
    csproj_file_path = get_csproj_at_path(path)
    if csproj_file_path:
        assembly_name = _get_csproj_assembly_name(csproj_file_path)
        if assembly_name:
            return assembly_name

    return None


def get_package_version(path):
    """
    Returns package version if path is a .nuspec file, .csproj file or a directory containing either.
    Otherwise, returns None
    """
    nuspec_file_path = get_nuspec_at_path(path)

    if nuspec_file_path:  # got .nuspec, try to read package id
        package_id = _get_nuspec_package_version(nuspec_file_path)
        if package_id:
            return package_id

    # try to read .csproj
    csproj_file_path = get_csproj_at_path(path)
    if csproj_file_path:
        assembly_name = _get_csproj_assembly_version(csproj_file_path)
        if assembly_name:
            return assembly_name

    return None


def get_nuspec_at_path(path):
    """ If path is a .nuspec file, return path. If path is a directory, finds .nuspec file in that directory """
    if _path_is_nuspec_file(path):
        return path
    elif os.path.isdir(path):
        return utils.dir_find_file_with_extension(path, '.nuspec')
    return None


def get_csproj_at_path(path):
    """ If path is a .csproj file, return path. If path is a directory, finds .csproj file in that directory """
    if _path_is_csproj_file(path):
        return path
    elif os.path.isdir(path):
        return utils.dir_find_file_with_extension(path, '.csproj')
    return None


def _path_is_nuspec_file(path):
    return os.path.isfile(path) and path.endswith('.nuspec')


def _path_is_csproj_file(path):
    return os.path.isfile(path) and path.endswith('.csproj')


def _get_nuspec_package_id(nuspec_file_path):
    tree = ET.parse(nuspec_file_path)
    metadata = tree.find('metadata')
    if not metadata:
        return None
    package_id = metadata.find('id')
    if not package_id:
        return None
    if package_id.text.startswith('$'):
        return None  # variable

    return package_id.text


def _get_nuspec_package_version(nuspec_file_path):
    tree = ET.parse(nuspec_file_path)
    metadata = tree.find('metadata')

    if not metadata:
        return None
    version = metadata.find('version')
    if not version:
        return None
    if version.text.startswith('$'):
        return None  # variable

    return version.text


def _get_csproj_assembly_name(csproj_file_path):
    tree = ET.parse(csproj_file_path)
    root = tree.getroot()

    xml_element_property_group = "{http://schemas.microsoft.com/developer/msbuild/2003}PropertyGroup"
    xml_element_assembly_name = "{http://schemas.microsoft.com/developer/msbuild/2003}AssemblyName"

    for child in root.findall(xml_element_property_group):
        assembly_name = child.find(xml_element_assembly_name)
        if assembly_name is not None:
            return assembly_name.text

    return None


def _get_csproj_assembly_version(csproj_file_path):
    """ Extracts assembly version from AssemblyInfo.cs """
    csproj_dir = os.path.dirname(csproj_file_path)
    assembly_info_path = os.path.join(csproj_dir, 'Properties', 'AssemblyInfo.cs')
    if not os.path.isfile(assembly_info_path):
        return None

    with open(assembly_info_path, 'r') as assembly_info:
        text = assembly_info.read()

    matches = re.findall('\[assembly: AssemblyVersion\("([\d.]+)"\)\]', text)
    if len(matches) == 0:
        raise ValueError("Failed to extract AssemblyVersion from {0}".format(assembly_info_path))
    else:
        version = matches[0]
        return version

