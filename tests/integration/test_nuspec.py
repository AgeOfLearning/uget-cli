#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Integration tests for `ugetcli` package - `nuspec` module.
Tests functionality of the NuSpec helper integration
"""
import unittest
import os
import shutil

from ugetcli.utils import temp_dir
from ugetcli.nuspec import NuSpec


_FIXTURE_DIR = "_fixtures/nuspec/test_nuspec/"
_TEST_NUSPEC = "MyProject.nuspec"


def get_fixture_dir():
    return os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), _FIXTURE_DIR))


class TestUGetCliNuSpec(unittest.TestCase):
    """Tests for `ugetcli` package - `nuspec` module"""

    def test_nuspec_get_nuspec_at_path_when_path_is_nuspec_file(self):
        """Test NuSpec.get_nuspec_at_path when path is a nuspec file"""
        with temp_dir() as tmp_root_dir:
            nuspec_root = os.path.join(tmp_root_dir, "test")
            shutil.copytree(get_fixture_dir(), nuspec_root)
            nuspec_path = os.path.join(nuspec_root, _TEST_NUSPEC)
            assert NuSpec.get_nuspec_at_path(nuspec_path) == nuspec_path

    def test_nuspec_get_nuspec_at_path_when_path_is_a_directory_with_nuspec_file(self):
        """Test NuSpec.get_nuspec_at_path when path is a nuspec file"""
        with temp_dir() as tmp_root_dir:
            nuspec_root = os.path.join(tmp_root_dir, "test")
            shutil.copytree(get_fixture_dir(), nuspec_root)
            nuspec_path = os.path.join(nuspec_root, _TEST_NUSPEC)
            assert NuSpec.get_nuspec_at_path(nuspec_root) == nuspec_path

    def test_nuspec_path_is_nuspec_file(self):
        """Test NuSpec.get_nuspec_at_path when path is a nuspec file"""
        with temp_dir() as tmp_root_dir:
            nuspec_root = os.path.join(tmp_root_dir, "test")
            shutil.copytree(get_fixture_dir(), nuspec_root)
            nuspec_path = os.path.join(nuspec_root, _TEST_NUSPEC)
            assert NuSpec.path_is_nuspec_file(nuspec_path)

    def test_nuspec_get_package_id(self):
        """Test NuSpec.get_package_id """
        with temp_dir() as tmp_root_dir:
            nuspec_root = os.path.join(tmp_root_dir, "test")
            shutil.copytree(get_fixture_dir(), nuspec_root)
            nuspec_path = os.path.join(nuspec_root, _TEST_NUSPEC)
            nuspec = NuSpec(nuspec_path)
            assert nuspec.get_package_id() == "MyProject"  # Set to "MyProject" in fixture .nuspec file

    def test_nuspec_get_package_version(self):
        """Test NuSpec.get_package_version """
        with temp_dir() as tmp_root_dir:
            nuspec_root = os.path.join(tmp_root_dir, "test")
            shutil.copytree(get_fixture_dir(), nuspec_root)
            nuspec_path = os.path.join(nuspec_root, _TEST_NUSPEC)
            nuspec = NuSpec(nuspec_path)
            assert nuspec.get_package_version() == "1.0.0"  # Set to "1.0.0" in fixture .nuspec file
