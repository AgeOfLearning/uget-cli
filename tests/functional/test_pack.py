#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `ugetcli` package."""

import unittest
from click.testing import CliRunner
from unittest.mock import MagicMock, patch

from ugetcli import cli


class TestUGetCli(unittest.TestCase):
    """Tests for `ugetcli` package."""

    @patch('nuget.valid_nuget_executable')
    @patch('nuget._run_nuget')
    @patch('nuget.locate_nuget')
    @patch('csproj.get_package_version')
    @patch('csproj.get_package_id')
    @patch('csproj.get_csproj_at_path')
    @patch('csproj.get_nuspec_at_path')
    def test_cli_uget_pack_propmt_nuget_path(
        self, get_nuspec_at_path_mock, get_csproj_at_path_mock, get_package_id, get_package_version, locate_nuget_mock,
        nuget_run, valid_nuget_executable_mock):
        """Test cli: uget pack with nuget.exe input"""
        locate_nuget_mock.return_value = False
        nuget_run.return_value = 0
        get_package_id.return_value = "test"
        get_package_version.return_value = "1.0.0"
        valid_nuget_executable_mock.return_value = True

        runner = CliRunner()
        result = runner.invoke(cli.ugetcli, ['pack'], input='custom_nuget.exe\n', obj={})
        assert result.exit_code == 0
        expected_args = ['pack', '.', "-OutputDirectory", '.', "-Properties",
                         'unityPackagePath=test_1.0.0_Debug.unitypackage;Configuration=Debug', "-Verbosity", "normal"]
        assert nuget_run.called_with('custom_nuget.exe', expected_args)

    @patch('nuget.valid_nuget_executable')
    @patch('nuget._run_nuget')
    @patch('nuget.locate_nuget')
    @patch('csproj.get_package_version')
    @patch('csproj.get_package_id')
    @patch('csproj.get_csproj_at_path')
    @patch('csproj.get_nuspec_at_path')
    def test_cli_uget_pack_env_nuget_path(
        self, get_nuspec_at_path_mock, get_csproj_at_path_mock, get_package_id, get_package_version, locate_nuget_mock,
        nuget_run, valid_nuget_executable_mock):
        """Test cli: uget pack with nuget.exe input"""
        locate_nuget_mock.return_value = False
        nuget_run.return_value = 0
        get_package_id.return_value = "test"
        get_package_version.return_value = "1.0.0"
        valid_nuget_executable_mock.return_value = True

        runner = CliRunner(env={'NUGET_PATH': 'custom_nuget.exe'})
        result = runner.invoke(cli.ugetcli, ['pack'], obj={})
        assert result.exit_code == 0
        expected_args = ['pack', '.', "-OutputDirectory", '.', "-Properties",
                         'unityPackagePath=test_1.0.0_Debug.unitypackage;Configuration=Debug', "-Verbosity", "normal"]
        assert nuget_run.called_with('custom_nuget.exe', expected_args)
