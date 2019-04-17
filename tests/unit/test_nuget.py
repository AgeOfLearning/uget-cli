#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for `ugetcli` package - `utils` module.
Tests functionality of the nuget helper module
"""
import unittest
import os

from ugetcli.nuget import NuGetRunner


class TestNugetRunner(unittest.TestCase):
    """Tests for `ugetcli` package - `nuget` module"""

    def test_nuget_runner_get_normalized_nuget_pack_version(self):
        """Test NuGetRunner.get_normalized_nuget_pack_version """
        assert NuGetRunner.get_normalized_nuget_pack_version("1.0.0") == "1.0.0"  # Does not change
        assert NuGetRunner.get_normalized_nuget_pack_version("1.0.0.1") == "1.0.0.1"  # Does not change
        assert NuGetRunner.get_normalized_nuget_pack_version("1.2.3.4") == "1.2.3.4"  # Does not change

        assert NuGetRunner.get_normalized_nuget_pack_version("1.0.0.0") == "1.0.0"  # Drops last zero
        assert NuGetRunner.get_normalized_nuget_pack_version("1.0.2.0") == "1.0.2"  # Drops last zero
        assert NuGetRunner.get_normalized_nuget_pack_version("1.1.0.0") == "1.1.0"  # Drops last zero
        assert NuGetRunner.get_normalized_nuget_pack_version("0.1.2.0") == "0.1.2"  # Drops last zero
