import os
import xml.etree.ElementTree as ET
from ugetcli import utils

"""
Helper module that provides access to .nuspec file helper methods
"""


class NuSpec:
    """
    Helper class that provides access to .nuspec file properties
    """
    def __init__(self, path, debug=False):
        self.path = NuSpec.get_nuspec_at_path(path)
        if not self.path:
            raise IOError("Failed to locate .nuspec file at path " + path)
        self.debug = debug

    def get_package_id(self):
        tree = ET.parse(self.path)
        metadata = tree.find('metadata')
        if not metadata:
            return None
        package_id = metadata.find('id')
        if package_id is None or not package_id.text:
            return None
        if package_id.text.startswith('$'):
            return None  # variable

        return package_id.text

    def get_package_version(self):
        tree = ET.parse(self.path)
        metadata = tree.find('metadata')

        if not metadata:
            return None
        version = metadata.find('version')
        if version is None or not version.text:
            return None
        if version.text.startswith('$'):
            return None  # variable

        return version.text

    @staticmethod
    def get_nuspec_at_path(path):
        """
        If path is a .nuspec file, return path.
        If path is a directory, finds .nuspec file in that directory.
        Otherwise, returns None
        """
        if NuSpec.path_is_nuspec_file(path):
            return path
        elif os.path.isdir(path):
            return utils.dir_find_file_with_extension(path, '.nuspec')
        return None

    @staticmethod
    def path_is_nuspec_file(path):
        """Checks if provided path is a .nuspec file
        :param path:
        :return: True if file is a valid NuSpec file
        """
        return os.path.isfile(path) and path.endswith('.nuspec')
