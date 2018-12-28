import os
from upackage.upackage import UPackage


"""
Helper module that provides access to UnityPackage methods
"""


class UnityPackageRunner:
    """
    Facade module that provides access to create UnityPackage files
    """
    def __init__(self, debug=False):
        self.debug = debug

    def export_unitypackage(self, package_root, output_path):
        UPackage.preprocess_assets(package_root)
        UPackage.generate_package(package_root, output_path)

