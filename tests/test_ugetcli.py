#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `ugetcli` package."""

import unittest
from click.testing import CliRunner
from unittest.mock import MagicMock, patch

from ugetcli import cli


class TestUGetCli(unittest.TestCase):
    """Tests for `ugetcli` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_cli_uget_help(self):
        """Test cli: uget help"""
        runner = CliRunner()
        result = runner.invoke(cli.ugetcli, ['--help'], obj={})
        assert result.exit_code == 0
        assert '--help' in  result.output
        assert 'Show this message and exit.' in result.output

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

    @patch('nuget.valid_nuget_executable')
    @patch('nuget._run_nuget')
    @patch('nuget.locate_nuget')
    def test_cli_uget_push(
        self, locate_nuget_mock, nuget_run, valid_nuget_executable_mock):
        """Test cli: uget push """
        locate_nuget_mock.return_value = False
        nuget_run.return_value = 0
        valid_nuget_executable_mock.return_value = True

        runner = CliRunner()
        with runner.isolated_filesystem():
            with open('test.nupkg', 'w') as f:
                f.write('mock_nuget_package_content')
            args = ['push', '--path', 'test.nupkg', '--nuget-path', 'custom_nuget.exe', '--feed', 'http://test.com/']
            result = runner.invoke(cli.ugetcli, args, obj={})
            assert result.exit_code == 0
            expected_args = ['push', 'test.nupkg', '-Verbosity', 'normal', '-Source', 'http://test.com/']
            assert nuget_run.called_with('custom_nuget.exe', expected_args)
