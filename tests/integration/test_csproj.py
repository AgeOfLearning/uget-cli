#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Integration tests for `ugetcli` package - `csproj` module.
Tests functionality of the .csproj reader integration
"""
import unittest
import os
import shutil

from ugetcli.utils import create_empty_file, temp_dir
from ugetcli.csproj import CsProj

_FIXTURE_DIR = "_fixtures/csproj/test_csproj/"
_TEST_CSPROJ = "MyProject.csproj"


def get_fixture_dir():
    return os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), _FIXTURE_DIR))


class TestUGetCliCsproj(unittest.TestCase):
    """Tests for `ugetcli` package - `csproj` module"""

    def test_csproj_get_csproj_at_path_when_path_is_a_csproj_file(self):
        """Test CsProj.get_csproj_at_path - returns path if path is a file"""
        file_name = "MyProject.csproj"
        with temp_dir() as tmp_root_dir:
            path = os.path.normpath(os.path.join(tmp_root_dir, file_name))
            create_empty_file(path)
            assert CsProj.get_csproj_at_path(path) == path

    def test_csproj_get_csproj_at_path_when_path_contains_csproj(self):
        """Test CsProj.get_csproj_at_path - returns path if path is a file"""
        file_name = "MyProject.csproj"
        with temp_dir() as tmp_root_dir:
            path = os.path.normpath(os.path.join(tmp_root_dir, file_name))
            create_empty_file(path)
            assert CsProj.get_csproj_at_path(tmp_root_dir) == path

    def test_csproj_path_is_csproj_file(self):
        """Test CsProj.path_is_csproj_file - returns true path is a .csproj file"""
        file_name = "MyProject.csproj"
        with temp_dir() as tmp_root_dir:
            path = os.path.normpath(os.path.join(tmp_root_dir, file_name))
            create_empty_file(path)
            assert CsProj.path_is_csproj_file(path)

    def test_csproj_get_assembly_name(self):
        """Test CsProj.get_assembly_name - returns assembly name from a csproj file """
        with temp_dir() as tmp_root_dir:
            csproj_root = os.path.join(tmp_root_dir, "test")
            shutil.copytree(get_fixture_dir(), csproj_root)
            csproj = CsProj(os.path.join(csproj_root, _TEST_CSPROJ))
            assert csproj.get_assembly_name() == "MyProject"

    def test_csproj_get_output_path(self):
        """Test CsProj.get_output_path - returns csproj output path from a csproj file """
        with temp_dir() as tmp_root_dir:
            csproj_root = os.path.join(tmp_root_dir, "test")
            shutil.copytree(get_fixture_dir(), csproj_root)
            csproj = CsProj(os.path.join(csproj_root, _TEST_CSPROJ))
            assert csproj.get_output_path("Debug") == "bin\\Debug\\"
            assert csproj.get_output_path("Release") == "bin\\Release\\"

    def test_csproj_get_assembly_version(self):
        """Test CsProj.get_assembly_version - returns assembly version path from a csproj / AssemblyInfo file """
        with temp_dir() as tmp_root_dir:
            csproj_root = os.path.join(tmp_root_dir, "test")
            shutil.copytree(get_fixture_dir(), csproj_root)
            csproj = CsProj(os.path.join(csproj_root, _TEST_CSPROJ))
            assert csproj.get_assembly_version() == "1.2.3"
