#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Functional tests for `ugetcli` package - `push` command.
Tests functionality of the cli push command with various options.
"""

import unittest
import os
import json
from click.testing import CliRunner
from mock import MagicMock, patch

from ugetcli import cli
from ugetcli.utils import create_empty_file


class TestUGetCliPush(unittest.TestCase):
    """Tests for `ugetcli` package - pack command."""
    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.NuGetRunner')
    def test_cli_uget_push(
        self, nuget_runner_mock, csproj_mock):
        """Test cli: uget pack with default values when path contains .csproj"""
        nuget_runner_instance = MagicMock()
        nuget_runner_mock.return_value = nuget_runner_instance
        nuget_runner_mock.locate_nuget.return_value = "nuget.exe"

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.2.3"
        csproj_mock.return_value = csproj_instance
        csproj_mock.get_csproj_at_path.return_value = "TestProject.csproj"

        runner = CliRunner(env={"NUGET_PATH": None, "NUGET_API_KEY": None})
        with runner.isolated_filesystem():
            create_empty_file("TestProject.1.2.3.nupkg")
            result = runner.invoke(cli.ugetcli, ['push'], obj={})

        assert result.exit_code == 0, result
        nuget_runner_mock.assert_called_with('nuget.exe', False)
        nuget_runner_instance.push.assert_called_with(os.path.normpath("TestProject.1.2.3.nupkg"), None, None)

    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.NuGetRunner')
    def test_cli_uget_push_path_csproj(
        self, nuget_runner_mock, csproj_mock):
        """Test cli: uget pack with default values when path directly points to .csproj"""
        nuget_runner_instance = MagicMock()
        nuget_runner_mock.return_value = nuget_runner_instance
        nuget_runner_mock.locate_nuget.return_value = "nuget.exe"

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.2.3"
        csproj_mock.return_value = csproj_instance
        csproj_mock.get_csproj_at_path.return_value = "TestProject.csproj"

        runner = CliRunner(env={"NUGET_PATH": None, "NUGET_API_KEY": None})
        with runner.isolated_filesystem():
            create_empty_file("TestProject.1.2.3.nupkg")
            result = runner.invoke(cli.ugetcli, ['push', '--path', 'TestProject.csproj'], obj={})

        assert result.exit_code == 0, result
        nuget_runner_mock.assert_called_with('nuget.exe', False)
        nuget_runner_instance.push.assert_called_with(os.path.normpath("TestProject.1.2.3.nupkg"), None, None)
        csproj_mock.get_csproj_at_path.assert_called_with('TestProject.csproj')

    @patch('ugetcli.uget.NuGetRunner')
    def test_cli_uget_push_path_nupkg(
        self, nuget_runner_mock):
        """Test cli: uget pack with default values when path points to a .nupkg file"""
        nuget_runner_instance = MagicMock()
        nuget_runner_mock.return_value = nuget_runner_instance
        nuget_runner_mock.locate_nuget.return_value = "nuget.exe"

        runner = CliRunner(env={"NUGET_PATH": None, "NUGET_API_KEY": None})
        with runner.isolated_filesystem():
            create_empty_file("myproject.nupkg")
            result = runner.invoke(cli.ugetcli, ['push', '--path', 'myproject.nupkg'], obj={})

        assert result.exit_code == 0, result
        nuget_runner_mock.assert_called_with('nuget.exe', False)
        nuget_runner_instance.push.assert_called_with(os.path.normpath("myproject.nupkg"), None, None)

    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.NuGetRunner')
    def test_cli_uget_push_path_csproj_with_output_dir(
        self, nuget_runner_mock, csproj_mock):
        """Test cli: uget pack with default values when path directly points to .csproj and --output-dir is set"""
        nuget_runner_instance = MagicMock()
        nuget_runner_mock.return_value = nuget_runner_instance
        nuget_runner_mock.locate_nuget.return_value = "nuget.exe"

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.2.3"
        csproj_mock.return_value = csproj_instance
        csproj_mock.get_csproj_at_path.return_value = "TestProject.csproj"

        runner = CliRunner(env={"NUGET_PATH": None, "NUGET_API_KEY": None})
        with runner.isolated_filesystem():
            os.makedirs("MyOutput")
            create_empty_file("MyOutput/TestProject.1.2.3.nupkg")
            result = runner.invoke(cli.ugetcli, ['push', '--path', 'TestProject.csproj', '--output-dir', 'MyOutput'],
                                   obj={})

        assert result.exit_code == 0, result
        nuget_runner_mock.assert_called_with('nuget.exe', False)
        nuget_runner_instance.push.assert_called_with(os.path.normpath("MyOutput/TestProject.1.2.3.nupkg"), None, None)
        csproj_mock.get_csproj_at_path.assert_called_with('TestProject.csproj')

    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.NuGetRunner')
    def test_cli_uget_push_with_feed(
        self, nuget_runner_mock, csproj_mock):
        """Test cli: uget pack with --feed"""
        nuget_runner_instance = MagicMock()
        nuget_runner_mock.return_value = nuget_runner_instance
        nuget_runner_mock.locate_nuget.return_value = "nuget.exe"

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.2.3"
        csproj_mock.return_value = csproj_instance
        csproj_mock.get_csproj_at_path.return_value = "TestProject.csproj"

        runner = CliRunner(env={"NUGET_PATH": None, "NUGET_API_KEY": None})
        with runner.isolated_filesystem():
            create_empty_file("TestProject.1.2.3.nupkg")
            result = runner.invoke(cli.ugetcli, ['push', '--feed', 'http://test.com/feed'], obj={})

        assert result.exit_code == 0, result
        nuget_runner_mock.assert_called_with('nuget.exe', False)
        nuget_runner_instance.push.assert_called_with(
            os.path.normpath("TestProject.1.2.3.nupkg"), 'http://test.com/feed', None)

    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.NuGetRunner')
    def test_cli_uget_push_with_nuget_path(
        self, nuget_runner_mock, csproj_mock):
        """Test cli: uget pack with --nuget-path"""
        nuget_runner_instance = MagicMock()
        nuget_runner_mock.return_value = nuget_runner_instance
        nuget_runner_mock.locate_nuget.return_value = "custom_nuget.exe"

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.2.3"
        csproj_mock.return_value = csproj_instance
        csproj_mock.get_csproj_at_path.return_value = "TestProject.csproj"

        runner = CliRunner(env={"NUGET_PATH": None, "NUGET_API_KEY": None})
        with runner.isolated_filesystem():
            create_empty_file("TestProject.1.2.3.nupkg")
            result = runner.invoke(cli.ugetcli, ['push', '--nuget-path', 'custom_nuget.exe'], obj={})

        assert result.exit_code == 0, result
        nuget_runner_mock.assert_called_with('custom_nuget.exe', False)
        nuget_runner_mock.locat_nuget.assert_called_with("custom_nuget.exe")
        nuget_runner_instance.push.assert_called_with(
            os.path.normpath("TestProject.1.2.3.nupkg"), None, None)

    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.NuGetRunner')
    def test_cli_uget_push_with_nuget_path(
        self, nuget_runner_mock, csproj_mock):
        """Test cli: uget pack with NUGET_PATH env variable set"""
        nuget_runner_instance = MagicMock()
        nuget_runner_mock.return_value = nuget_runner_instance
        nuget_runner_mock.valid_nuget_executable.return_value = True

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.2.3"
        csproj_mock.return_value = csproj_instance
        csproj_mock.get_csproj_at_path.return_value = "TestProject.csproj"

        runner = CliRunner(env={"NUGET_PATH": "custom_nuget.exe", "NUGET_API_KEY": None})
        with runner.isolated_filesystem():
            create_empty_file("TestProject.1.2.3.nupkg")
            result = runner.invoke(cli.ugetcli, ['push'], obj={})

        assert result.exit_code == 0, result
        nuget_runner_mock.assert_called_with('custom_nuget.exe', False)
        nuget_runner_mock.valid_nuget_executable.assert_called_with("custom_nuget.exe")
        nuget_runner_instance.push.assert_called_with(
            os.path.normpath("TestProject.1.2.3.nupkg"), None, None)

    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.NuGetRunner')
    def test_cli_uget_push_with_api_key(
        self, nuget_runner_mock, csproj_mock):
        """Test cli: uget pack with --api-key"""
        nuget_runner_instance = MagicMock()
        nuget_runner_mock.return_value = nuget_runner_instance
        nuget_runner_mock.locate_nuget.return_value = "nuget.exe"

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.2.3"
        csproj_mock.return_value = csproj_instance
        csproj_mock.get_csproj_at_path.return_value = "TestProject.csproj"

        runner = CliRunner(env={"NUGET_PATH": None, "NUGET_API_KEY": None})
        with runner.isolated_filesystem():
            create_empty_file("TestProject.1.2.3.nupkg")
            result = runner.invoke(cli.ugetcli, ['push', '--api-key', 'myapikey'], obj={})

        assert result.exit_code == 0, result
        nuget_runner_mock.assert_called_with('nuget.exe', False)
        nuget_runner_instance.push.assert_called_with(
            os.path.normpath("TestProject.1.2.3.nupkg"), None, "myapikey")

    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.NuGetRunner')
    def test_cli_uget_push_with_api_key_env(
        self, nuget_runner_mock, csproj_mock):
        """Test cli: uget pack with API_KEY env variable"""
        nuget_runner_instance = MagicMock()
        nuget_runner_mock.return_value = nuget_runner_instance
        nuget_runner_mock.locate_nuget.return_value = "nuget.exe"

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.2.3"
        csproj_mock.return_value = csproj_instance
        csproj_mock.get_csproj_at_path.return_value = "TestProject.csproj"

        runner = CliRunner(env={"NUGET_PATH": None, "NUGET_API_KEY": "myapikey"})
        with runner.isolated_filesystem():
            create_empty_file("TestProject.1.2.3.nupkg")
            result = runner.invoke(cli.ugetcli, ['push'], obj={})

        assert result.exit_code == 0, result
        nuget_runner_mock.assert_called_with('nuget.exe', False)
        nuget_runner_instance.push.assert_called_with(
            os.path.normpath("TestProject.1.2.3.nupkg"), None, "myapikey")

    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.NuGetRunner')
    def test_cli_uget_push_with_config_json(
        self, nuget_runner_mock, csproj_mock):
        """Test cli: uget pack with config json"""
        nuget_runner_instance = MagicMock()
        nuget_runner_mock.return_value = nuget_runner_instance
        nuget_runner_mock.locate_nuget.return_value = "nuget.exe"

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.2.3"
        csproj_mock.return_value = csproj_instance
        csproj_mock.get_csproj_at_path.return_value = "TestProject.csproj"

        config_data = {
            "output_dir": "CustomOutput",
            "feed": "http://test.com/nuget",
            "nuget_path": "custom_nuget.exe",
            "api_key": "myapikey123"
        }

        runner = CliRunner(env={"NUGET_PATH": None, "NUGET_API_KEY": None})
        with runner.isolated_filesystem():
            os.makedirs("CustomOutput")
            create_empty_file("CustomOutput/TestProject.1.2.3.nupkg")
            result = runner.invoke(cli.ugetcli, ['push', '--config', json.dumps(config_data)], obj={})

        assert result.exit_code == 0, result
        nuget_runner_mock.assert_called_with('custom_nuget.exe', False)
        nuget_runner_instance.push.assert_called_with(
            os.path.normpath("CustomOutput/TestProject.1.2.3.nupkg"), "http://test.com/nuget", "myapikey123")



    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.NuGetRunner')
    def test_cli_uget_push_with_config_file(
        self, nuget_runner_mock, csproj_mock):
        """Test cli: uget pack with config file"""
        nuget_runner_instance = MagicMock()
        nuget_runner_mock.return_value = nuget_runner_instance
        nuget_runner_mock.locate_nuget.return_value = "nuget.exe"

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.2.3"
        csproj_mock.return_value = csproj_instance
        csproj_mock.get_csproj_at_path.return_value = "TestProject.csproj"

        config_data = {
            "output_dir": "CustomOutput",
            "feed": "http://test.com/nuget",
            "nuget_path": "custom_nuget.exe",
            "api_key": "myapikey123"
        }

        runner = CliRunner(env={"NUGET_PATH": None, "NUGET_API_KEY": None})
        with runner.isolated_filesystem():
            with open('config_test.json', 'w') as f:
                json.dump(config_data, f)
            os.makedirs("CustomOutput")
            create_empty_file("CustomOutput/TestProject.1.2.3.nupkg")
            result = runner.invoke(cli.ugetcli, ['push', '--config-path', 'config_test.json'], obj={})

        assert result.exit_code == 0, result
        nuget_runner_mock.assert_called_with('custom_nuget.exe', False)
        nuget_runner_instance.push.assert_called_with(
            os.path.normpath("CustomOutput/TestProject.1.2.3.nupkg"), "http://test.com/nuget", "myapikey123")


