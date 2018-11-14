#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Functional tests for `ugetcli` package - `build` command.
Tests functionality of the cli command with various options.
"""

import unittest
import json
import uget
from click.testing import CliRunner
from unittest.mock import MagicMock, patch

from ugetcli import cli


class TestUGetCliBuild(unittest.TestCase):
    """Functional Tests for `ugetcli` package - build command."""

    @patch('uget.MsBuildRunner')
    @patch('uget.CsProj.get_csproj_at_path')
    def test_cli_uget_build_csproj(
        self, csproj_get_csproj_at_path_mock, msbuild_runner_mock):
        """Test cli: uget build with path containing valid csproj"""
        csproj_get_csproj_at_path_mock.return_value = 'TestProject.csproj'
        msbuild_runner_instance = MagicMock()
        msbuild_runner_instance.valid_msbuild_executable.return_value = True
        msbuild_runner_mock.return_value = msbuild_runner_instance
        msbuild_runner_mock.locate_msbuild.return_value = 'msbuild'

        runner = CliRunner()
        result = runner.invoke(cli.ugetcli, ['build'], obj={})

        assert result.exit_code == 0, result.output
        msbuild_runner_mock.assert_called_with('msbuild', False)
        msbuild_runner_instance.build.assert_called_with('TestProject.csproj', 'Release', False)

    @patch('uget.MsBuildRunner')
    @patch('uget.CsProj.get_csproj_at_path')
    def test_cli_uget_build_csproj_with_path_directory(
        self, csproj_get_csproj_at_path_mock, msbuild_runner_mock):
        """Test cli: uget build with path being a directory containing valid csproj"""
        csproj_get_csproj_at_path_mock.return_value = 'TestProject.csproj'
        msbuild_runner_instance = MagicMock()
        msbuild_runner_instance.valid_msbuild_executable.return_value = True
        msbuild_runner_mock.return_value = msbuild_runner_instance

        runner = CliRunner(env={'MSBUILD_PATH': 'custom_msbuild_exe'})
        result = runner.invoke(cli.ugetcli, ['build', '--path', 'some/path'], obj={})

        assert result.exit_code == 0, result.output

        csproj_get_csproj_at_path_mock.assert_called_with('some/path')
        msbuild_runner_mock.assert_called_with('custom_msbuild_exe', False)
        msbuild_runner_instance.build.assert_called_with('TestProject.csproj', 'Release', False)
    @patch('uget.MsBuildRunner')
    @patch('uget.CsProj.get_csproj_at_path')
    def test_cli_uget_build_csproj_with_configuration(
        self, csproj_get_csproj_at_path_mock, msbuild_runner_mock):
        """Test cli: uget build with --configuration"""
        csproj_get_csproj_at_path_mock.return_value = 'TestProject.csproj'
        msbuild_runner_instance = MagicMock()
        msbuild_runner_instance.valid_msbuild_executable.return_value = True
        msbuild_runner_mock.return_value = msbuild_runner_instance

        runner = CliRunner(env={'MSBUILD_PATH': 'custom_msbuild_exe'})
        result = runner.invoke(cli.ugetcli, ['build', '--configuration', 'Debug'], obj={})

        assert result.exit_code == 0, result.output
        msbuild_runner_mock.assert_called_with('custom_msbuild_exe', False)
        msbuild_runner_instance.build.assert_called_with('TestProject.csproj', 'Debug', False)

    @patch('uget.MsBuildRunner')
    @patch('uget.CsProj.get_csproj_at_path')
    def test_cli_uget_build_csproj_with_msbuild_executable(
        self, csproj_get_csproj_at_path_mock, msbuild_runner_mock):
        """Test cli: uget build with --msbuild-path"""
        csproj_get_csproj_at_path_mock.return_value = 'TestProject.csproj'
        msbuild_runner_instance = MagicMock()
        msbuild_runner_instance.valid_msbuild_executable.return_value = True
        msbuild_runner_mock.return_value = msbuild_runner_instance

        runner = CliRunner()
        result = runner.invoke(cli.ugetcli, ['build', '--msbuild-path', 'custom_msbuild_exe'], obj={})

        assert result.exit_code == 0, result.output
        msbuild_runner_mock.assert_called_with('custom_msbuild_exe', False)
        msbuild_runner_instance.build.assert_called_with('TestProject.csproj', 'Release', False)

    @patch('uget.MsBuildRunner')
    @patch('uget.CsProj.get_csproj_at_path')
    def test_cli_uget_build_csproj_with_custom_msbuild_env(
        self, csproj_get_csproj_at_path_mock, msbuild_runner_mock):
        """Test cli: uget build with MSBUILD_PATH in env"""
        csproj_get_csproj_at_path_mock.return_value = 'TestProject.csproj'
        msbuild_runner_instance = MagicMock()
        msbuild_runner_instance.valid_msbuild_executable.return_value = True
        msbuild_runner_mock.return_value = msbuild_runner_instance

        runner = CliRunner(env={'MSBUILD_PATH': 'custom_msbuild_exe'})
        result = runner.invoke(cli.ugetcli, ['build'], obj={})

        assert result.exit_code == 0, result.output
        msbuild_runner_mock.assert_called_with('custom_msbuild_exe', False)
        msbuild_runner_instance.build.assert_called_with('TestProject.csproj', 'Release', False)

    @patch('uget.MsBuildRunner')
    @patch('uget.CsProj.get_csproj_at_path')
    def test_cli_uget_build_csproj_with_rebuild(
        self, csproj_get_csproj_at_path_mock, msbuild_runner_mock):
        """Test cli: uget build with --rebuild"""
        csproj_get_csproj_at_path_mock.return_value = 'TestProject.csproj'
        msbuild_runner_instance = MagicMock()
        msbuild_runner_instance.valid_msbuild_executable.return_value = True
        msbuild_runner_mock.return_value = msbuild_runner_instance

        runner = CliRunner(env={'MSBUILD_PATH': 'custom_msbuild_exe'})
        result = runner.invoke(cli.ugetcli, ['build', '--rebuild'], obj={})

        assert result.exit_code == 0, result.output
        msbuild_runner_mock.assert_called_with('custom_msbuild_exe', False)
        msbuild_runner_instance.build.assert_called_with('TestProject.csproj', 'Release', True)

    @patch('uget.MsBuildRunner')
    @patch('uget.CsProj.get_csproj_at_path')
    def test_cli_uget_build_csproj_with_config_file(
        self, csproj_get_csproj_at_path_mock, msbuild_runner_mock):
        """Test cli: uget build with options loaded via config file"""
        csproj_get_csproj_at_path_mock.return_value = 'TestProject.csproj'
        msbuild_runner_instance = MagicMock()
        msbuild_runner_instance.valid_msbuild_executable.return_value = True
        msbuild_runner_mock.return_value = msbuild_runner_instance

        runner = CliRunner(env={'MSBUILD_PATH': 'custom_msbuild_exe'})

        config_data = {
            "configuration": "Debug",
            "msbuild_path": "msbuild_custom_exe",
            "rebuild": True
        }

        with runner.isolated_filesystem():
            with open('config_test.json', 'w') as f:
                json.dump(config_data, f)

            result = runner.invoke(cli.ugetcli, ['build', '--config', 'config_test.json'], obj={})

        assert result.exit_code == 0, result.output
        msbuild_runner_mock.assert_called_with('msbuild_custom_exe', False)
        msbuild_runner_instance.build.assert_called_with('TestProject.csproj', 'Debug', True)
