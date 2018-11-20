#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Integration tests for `ugetcli` package - `utils` module.
Tests functionality of the utils helper module
"""
import unittest
import os

from ugetcli.utils import temp_dir, validate_url, copy_replace_directory


class TestUGetCliUtils(unittest.TestCase):
    """Tests for `ugetcli` package - `utils` module"""

    def test_utils_validate_url(self):
        """Test utils.validate_url """
        assert validate_url("http://test.com/nuget")
        assert validate_url("https://test.com/nuget")
        assert validate_url("http://test.com/nuget/")
        assert validate_url("https://test.com/nuget")
        assert validate_url("http://test.com")
        assert validate_url("http://test.com:8080")
        assert validate_url("http://test.com:8080/nuget")
        assert validate_url("protocol://test.com/nuget")
        assert not validate_url("invalid/string")
        assert not validate_url("invalid")

    def test_utils_copy_replace_directory(self):
        """Test utils.copy_replace_directory """
        with temp_dir() as tmp_dir_path:
            dir_old = os.path.normpath("old/path")
            dir_new = os.path.normpath("new/path")
            file_name = "my_file.txt"
            old_dir_path = os.path.join(tmp_dir_path, dir_old)
            new_dir_path = os.path.join(tmp_dir_path, dir_new)
            old_file_path = os.path.normpath(os.path.join(old_dir_path, file_name))
            new_file_path = os.path.normpath(os.path.join(new_dir_path, file_name))
            os.makedirs(old_dir_path)
            os.makedirs(new_dir_path)

            with open(old_file_path, "w+") as f:
                f.write("Old Text")

            with open(new_file_path, "w+") as f:
                f.write("New Text")

            copy_replace_directory(new_dir_path, old_dir_path)

            with open(old_file_path, "r") as f:
                old_text = f.read()
                assert old_text == "New Text", "Text did not get replaced."

            with open(new_file_path, "r") as f:
                old_text = f.read()
                assert old_text == "New Text", "Wrong file was replaced."


