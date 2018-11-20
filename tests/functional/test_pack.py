#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Functional tests for `ugetcli` package - `pack` command.
Tests functionality of the cli pack command with various options.
"""

import unittest
import os
import json
from click.testing import CliRunner
from mock import MagicMock, patch

from ugetcli import cli
from ugetcli.utils import create_empty_file


class TestUGetCliPack(unittest.TestCase):
    """Tests for `ugetcli` package - pack command."""
    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.NuGetRunner')
    def test_cli_uget_pack_with_path_containing_csproj(
        self, nuget_runner_mock, csproj_mock):
        """Test cli: uget pack with path containing a csproj"""
        nuget_runner_instance = MagicMock()
        nuget_runner_mock.return_value = nuget_runner_instance
        nuget_runner_mock.locate_nuget.return_value = "nuget.exe"

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.2.3"
        csproj_mock.return_value = csproj_instance
        csproj_mock.get_csproj_at_path.return_value = "TestProject.csproj"

        runner = CliRunner(env={"NUGET_PATH": None})
        with runner.isolated_filesystem():
            result = runner.invoke(cli.ugetcli, ['pack'], obj={})

        assert result.exit_code == 0, result
        nuget_runner_mock.assert_called_with('nuget.exe', False)
        nuget_runner_instance.pack.assert_called_with(
            ".", "Output", "Release", os.path.normpath("Output/TestProject_1.2.3_Release.unitypackage"))

    @patch('ugetcli.uget.NuSpec')
    @patch('ugetcli.uget.NuGetRunner')
    def test_cli_uget_pack_with_path_containing_nuspec(
        self, nuget_runner_mock, nuspec_mock):
        """Test cli: uget pack with path containing a csproj"""
        nuget_runner_instance = MagicMock()
        nuget_runner_mock.return_value = nuget_runner_instance
        nuget_runner_mock.locate_nuget.return_value = "nuget.exe"

        nuspec_instance = MagicMock()
        nuspec_mock.get_nuspec_at_path.return_value = "TestProject.nuspec"
        nuspec_mock.return_value = nuspec_instance
        nuspec_instance.get_package_id.return_value = "TestProject"
        nuspec_instance.get_package_version.return_value = "1.2.3"

        runner = CliRunner(env={"NUGET_PATH": None})
        with runner.isolated_filesystem():
            result = runner.invoke(cli.ugetcli, ['pack'], obj={})

        assert result.exit_code == 0, result
        nuget_runner_mock.assert_called_with('nuget.exe', False)
        nuget_runner_instance.pack.assert_called_with(
            ".", "Output", "Release", os.path.normpath("Output/TestProject_1.2.3_Release.unitypackage"))

    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.NuGetRunner')
    def test_cli_uget_pack_with_output_dir(
        self, nuget_runner_mock, csproj_mock):
        """Test cli: uget pack with output dir containing a csproj"""
        nuget_runner_instance = MagicMock()
        nuget_runner_mock.return_value = nuget_runner_instance
        nuget_runner_mock.locate_nuget.return_value = "nuget.exe"

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.2.3"
        csproj_mock.return_value = csproj_instance
        csproj_mock.get_csproj_at_path.return_value = "TestProject.csproj"

        runner = CliRunner(env={"NUGET_PATH": None})
        with runner.isolated_filesystem():
            result = runner.invoke(cli.ugetcli, ['pack', '--output-dir', 'MyOutput'], obj={})

        assert result.exit_code == 0, result
        nuget_runner_mock.assert_called_with('nuget.exe', False)
        nuget_runner_instance.pack.assert_called_with(
            ".", "MyOutput", "Release", os.path.normpath("MyOutput/TestProject_1.2.3_Release.unitypackage"))

    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.NuGetRunner')
    def test_cli_uget_pack_with_nuget_path(
        self, nuget_runner_mock, csproj_mock):
        """Test cli: uget pack with --nuget-path"""
        nuget_runner_instance = MagicMock()
        nuget_runner_mock.return_value = nuget_runner_instance
        nuget_runner_mock.valid_nuget_executable.return_value = True

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.2.3"
        csproj_mock.return_value = csproj_instance
        csproj_mock.get_csproj_at_path.return_value = "TestProject.csproj"

        runner = CliRunner(env={"NUGET_PATH": None})
        with runner.isolated_filesystem():
            result = runner.invoke(cli.ugetcli, ['pack', '--nuget-path', 'custom_nuget.exe'], obj={})

        assert result.exit_code == 0, result
        nuget_runner_mock.assert_called_with('custom_nuget.exe', False)
        nuget_runner_instance.pack.assert_called_with(
            ".", "Output", "Release", os.path.normpath("Output/TestProject_1.2.3_Release.unitypackage"))
        nuget_runner_mock.valid_nuget_executable.assert_called_with("custom_nuget.exe")

    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.NuGetRunner')
    def test_cli_uget_pack_with_nuget_path_env(
        self, nuget_runner_mock, csproj_mock):
        """Test cli: uget pack NUGET_PATH env variable"""
        nuget_runner_instance = MagicMock()
        nuget_runner_mock.return_value = nuget_runner_instance
        nuget_runner_mock.valid_nuget_executable.return_value = True

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.2.3"
        csproj_mock.return_value = csproj_instance
        csproj_mock.get_csproj_at_path.return_value = "TestProject.csproj"

        runner = CliRunner(env={"NUGET_PATH": "custom_nuget.exe"})
        with runner.isolated_filesystem():
            result = runner.invoke(cli.ugetcli, ['pack'], obj={})

        assert result.exit_code == 0, result
        nuget_runner_mock.assert_called_with('custom_nuget.exe', False)
        nuget_runner_instance.pack.assert_called_with(
            ".", "Output", "Release", os.path.normpath("Output/TestProject_1.2.3_Release.unitypackage"))
        nuget_runner_mock.valid_nuget_executable.assert_called_with("custom_nuget.exe")

    @patch('ugetcli.uget.NuGetRunner')
    def test_cli_uget_pack_with_unitypackage_path(
        self, nuget_runner_mock):
        """Test cli: uget pack with --unitypackage-path"""
        nuget_runner_instance = MagicMock()
        nuget_runner_mock.return_value = nuget_runner_instance
        nuget_runner_mock.valid_nuget_executable.return_value = True
        nuget_runner_mock.locate_nuget.return_value = "nuget.exe"

        runner = CliRunner(env={"NUGET_PATH": None})
        with runner.isolated_filesystem():
            create_empty_file('MyUnityPackage.unitypackage')
            result = runner.invoke(cli.ugetcli, ['pack', '--unitypackage-path', 'MyUnityPackage.unitypackage'], obj={})

        assert result.exit_code == 0, result
        nuget_runner_mock.assert_called_with('nuget.exe', False)
        nuget_runner_instance.pack.assert_called_with(
            ".", "Output", "Release", "MyUnityPackage.unitypackage")

    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.NuGetRunner')
    def test_cli_uget_pack_with_configuration(
        self, nuget_runner_mock, csproj_mock):
        """Test cli: uget pack with --configuration"""
        nuget_runner_instance = MagicMock()
        nuget_runner_mock.return_value = nuget_runner_instance
        nuget_runner_mock.valid_nuget_executable.return_value = True
        nuget_runner_mock.locate_nuget.return_value = "nuget.exe"

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.2.3"
        csproj_mock.return_value = csproj_instance
        csproj_mock.get_csproj_at_path.return_value = "TestProject.csproj"

        runner = CliRunner(env={"NUGET_PATH": None})
        with runner.isolated_filesystem():
            result = runner.invoke(cli.ugetcli, ['pack', '--configuration', 'Debug'], obj={})

        assert result.exit_code == 0, result
        nuget_runner_mock.assert_called_with('nuget.exe', False)
        nuget_runner_instance.pack.assert_called_with(
            ".", "Output", "Debug", os.path.normpath("Output/TestProject_1.2.3_Debug.unitypackage"))

    @patch('ugetcli.uget.NuGetRunner')
    def test_cli_uget_pack_with_config_json(
        self, nuget_runner_mock):
        """Test cli: uget pack with --config json"""
        nuget_runner_instance = MagicMock()
        nuget_runner_mock.return_value = nuget_runner_instance
        nuget_runner_mock.valid_nuget_executable.return_value = True
        nuget_runner_mock.locate_nuget.return_value = "custom_nuget.exe"

        config_data = {
            "output_dir": "CustomOutput",
            "nuget_path": "custom_nuget.exe",
            "unitypackage_path": "MyUnityPackage.unitypackage",
            "configuration": "Debug",
        }

        runner = CliRunner(env={"NUGET_PATH": None})
        with runner.isolated_filesystem():
            create_empty_file('MyUnityPackage.unitypackage')
            result = runner.invoke(cli.ugetcli, ['pack', '--config', json.dumps(config_data)], obj={})

        assert result.exit_code == 0, result
        nuget_runner_mock.assert_called_with('custom_nuget.exe', False)
        nuget_runner_instance.pack.assert_called_with(
            ".", "CustomOutput", "Debug", "MyUnityPackage.unitypackage")

    @patch('ugetcli.uget.NuGetRunner')
    def test_cli_uget_pack_with_config_file(
        self, nuget_runner_mock):
        """Test cli: uget pack with --config-path file"""
        nuget_runner_instance = MagicMock()
        nuget_runner_mock.return_value = nuget_runner_instance
        nuget_runner_mock.valid_nuget_executable.return_value = True
        nuget_runner_mock.locate_nuget.return_value = "custom_nuget.exe"

        config_data = {
            "output_dir": "CustomOutput",
            "nuget_path": "custom_nuget.exe",
            "unitypackage_path": "MyUnityPackage.unitypackage",
            "configuration": "Debug",
        }

        runner = CliRunner(env={"NUGET_PATH": None})
        with runner.isolated_filesystem():
            with open('config_test.json', 'w') as f:
                json.dump(config_data, f)

            create_empty_file('MyUnityPackage.unitypackage')
            result = runner.invoke(cli.ugetcli, ['pack', '--config-path', 'config_test.json'], obj={})

        assert result.exit_code == 0, result
        nuget_runner_mock.assert_called_with('custom_nuget.exe', False)
        nuget_runner_instance.pack.assert_called_with(
            ".", "CustomOutput", "Debug", "MyUnityPackage.unitypackage")
