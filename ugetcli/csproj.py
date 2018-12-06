import os
import re
import xml.etree.ElementTree as ET
from ugetcli import utils

"""
Helper module that provides access to NuGet methods
"""


class CsProj:
    """
    Facade class that provides access to access Visual C# Project information
    """
    xml_namespace = "{http://schemas.microsoft.com/developer/msbuild/2003}"
    xml_element_property_group = xml_namespace+"PropertyGroup"
    xml_element_assembly_name = xml_namespace+"AssemblyName"
    xml_element_output_path = xml_namespace+"OutputPath"

    def __init__(self, path, debug=False):
        self.path = CsProj.get_csproj_at_path(path)
        if self.path is None:
            raise IOError("Failed to locate .csproj at path: " + path)

        self.debug = debug

    def get_assembly_name(self):
        tree = ET.parse(self.path)
        root = tree.getroot()

        for property_group in root.findall(self.xml_element_property_group):
            assembly_name = property_group.find(self.xml_element_assembly_name)
            if assembly_name is not None:
                return assembly_name.text
        return None

    def get_output_path(self,  configuration):
        tree = ET.parse(self.path)
        root = tree.getroot()

        condition = " '$(Configuration)|$(Platform)' == '{0}|AnyCPU' ".format(configuration)

        for property_group in root.findall(self.xml_element_property_group):
            output_path = property_group.find(self.xml_element_output_path)
            if output_path is not None and property_group.attrib["Condition"] == condition:
                return output_path.text
        return None

    def get_assembly_version(self):
        """ Extracts assembly version from AssemblyInfo.cs """
        csproj_dir = os.path.dirname(self.path)
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

    @staticmethod
    def get_csproj_at_path(path):
        """
        If path is a .csproj file, return path. If path is a directory, finds .csproj file in that directory
        """
        if CsProj.path_is_csproj_file(path):
            return path
        elif os.path.isdir(path):
            return utils.dir_find_file_with_extension(path, '.csproj')
        return None

    @staticmethod
    def path_is_csproj_file(path):
        """
        If path is a csproj file, returns true, otherwise returns False
        """
        return os.path.isfile(path) and path.endswith('.csproj')
