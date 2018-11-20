#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Functional tests for `ugetcli` package - `create` command.
Tests functionality of the cli create command with various options.
"""

import os
import unittest
import json
from click.testing import CliRunner
from mock import MagicMock, patch

from ugetcli import cli
from ugetcli.utils import create_empty_file


class TestUGetCliCreate(unittest.TestCase):
    """Functional Tests for `ugetcli` package - `create` command."""

    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.UnityRunner')
    def test_cli_uget_create(
        self, unity_runner_mock, csproj_mock):
        """Test cli: uget create with default options"""

        # Mock running Unity to export unity package
        def export_unitypackage_mock(*args, **kwargs):
            assert 'UnityProject' in args[0]  # In temp folder
            assert args[1] == os.path.normpath('Assets/TestProject')
            assert args[2] == os.path.normpath('Output/TestProject_1.0.0_Release.unitypackage')
            create_empty_file(args[2])
            return 0

        unity_runner_instance = MagicMock()
        unity_runner_instance.export_unitypackage = export_unitypackage_mock
        unity_runner_mock.return_value = unity_runner_instance

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.0.0"
        csproj_instance.get_output_path.return_value = "bin/Output/Debug"
        csproj_mock.return_value = csproj_instance
        csproj_mock.get_csproj_at_path.return_value = "TestProject.csproj"

        runner = CliRunner(env={"UNITY_PATH": None, "UNITY_USERNAME": None, "UNITY_PASSWORD": None,
                                "UNITY_SERIAL": None})
        with runner.isolated_filesystem():
            os.makedirs("bin/Output/Debug")
            create_empty_file("bin/Output/Debug/TestProject.dll")
            create_empty_file("bin/Output/Debug/TestProject.pdb")
            result = runner.invoke(cli.ugetcli, ['create', '--unity-path', 'unity.exe'], obj={})

        assert result.exit_code == 0, result
        unity_runner_mock.assert_called_with('unity.exe', None, None, None, False)

    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.UnityRunner')
    def test_cli_uget_create_with_path(
        self, unity_runner_mock, csproj_mock):
        """Test cli: uget create with --path option"""

        # Mock running Unity to export unity package
        def export_unitypackage_mock(*args, **kwargs):
            assert 'UnityProject' in args[0]  # In temp folder
            assert args[1] == os.path.normpath('Assets/TestProject')
            assert args[2] == os.path.normpath('Output/TestProject_1.0.0_Release.unitypackage')
            create_empty_file(args[2])
            return 0

        unity_runner_instance = MagicMock()
        unity_runner_instance.export_unitypackage = export_unitypackage_mock
        unity_runner_mock.return_value = unity_runner_instance

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.0.0"
        csproj_instance.get_output_path.return_value = "bin/Output/Debug"
        csproj_mock.return_value = csproj_instance

        runner = CliRunner(env={"UNITY_PATH": None, "UNITY_USERNAME": None, "UNITY_PASSWORD": None,
                                "UNITY_SERIAL": None})
        with runner.isolated_filesystem():
            os.makedirs("bin/Output/Debug")
            create_empty_file("bin/Output/Debug/TestProject.dll")
            create_empty_file("bin/Output/Debug/TestProject.pdb")
            result = runner.invoke(cli.ugetcli, ['create', '--unity-path', 'unity.exe', '--path', 'custom/'], obj={})

        assert result.exit_code == 0, result
        unity_runner_mock.assert_called_with('unity.exe', None, None, None, False)
        csproj_mock.assert_called_with('custom/')

    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.UnityRunner')
    def test_cli_uget_create_with_output_dir(
        self, unity_runner_mock, csproj_mock):
        """Test cli: uget create with --output-dir option"""

        # Mock running Unity to export unity package
        def export_unitypackage_mock(*args, **kwargs):
            assert 'UnityProject' in args[0]  # In temp folder
            assert args[1] == os.path.normpath('Assets/TestProject')
            assert args[2] == os.path.normpath('out/TestProject_1.0.0_Release.unitypackage')
            create_empty_file(args[2])
            return 0

        unity_runner_instance = MagicMock()
        unity_runner_instance.export_unitypackage = export_unitypackage_mock
        unity_runner_mock.return_value = unity_runner_instance

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.0.0"
        csproj_instance.get_output_path.return_value = "bin/Output/Debug"
        csproj_mock.return_value = csproj_instance

        runner = CliRunner(env={"UNITY_PATH": None, "UNITY_USERNAME": None, "UNITY_PASSWORD": None,
                                "UNITY_SERIAL": None})
        with runner.isolated_filesystem():
            os.makedirs("bin/Output/Debug")
            create_empty_file("bin/Output/Debug/TestProject.dll")
            create_empty_file("bin/Output/Debug/TestProject.pdb")
            result = runner.invoke(cli.ugetcli, ['create', '--unity-path', 'unity.exe', '--output-dir', 'out'], obj={})

        assert result.exit_code == 0, result
        unity_runner_mock.assert_called_with('unity.exe', None, None, None, False)

    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.UnityRunner')
    def test_cli_uget_create_with_configuration(
        self, unity_runner_mock, csproj_mock):
        """Test cli: uget create with --configuration option"""

        # Mock running Unity to export unity package
        def export_unitypackage_mock(*args, **kwargs):
            assert 'UnityProject' in args[0]  # In temp folder
            assert args[1] == os.path.normpath('Assets/TestProject')
            assert args[2] == os.path.normpath('Output/TestProject_1.0.0_Debug.unitypackage')
            create_empty_file(args[2])
            return 0

        unity_runner_instance = MagicMock()
        unity_runner_instance.export_unitypackage = export_unitypackage_mock
        unity_runner_mock.return_value = unity_runner_instance

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.0.0"
        csproj_instance.get_output_path.return_value = "bin/Output/Debug"
        csproj_mock.return_value = csproj_instance

        runner = CliRunner(env={"UNITY_PATH": None, "UNITY_USERNAME": None, "UNITY_PASSWORD": None,
                                "UNITY_SERIAL": None})
        with runner.isolated_filesystem():
            os.makedirs("bin/Output/Debug")
            create_empty_file("bin/Output/Debug/TestProject.dll")
            create_empty_file("bin/Output/Debug/TestProject.pdb")
            result = runner.invoke(cli.ugetcli, ['create', '--unity-path', 'unity.exe', '--configuration', 'Debug'],
                                   obj={})

        assert result.exit_code == 0, result
        unity_runner_mock.assert_called_with('unity.exe', None, None, None, False)

    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.UnityRunner')
    def test_cli_uget_create_with_unity_path_env(
        self, unity_runner_mock, csproj_mock):
        """Test cli: uget create with UNITY_PATH set inside env variable"""

        # Mock running Unity to export unity package
        def export_unitypackage_mock(*args, **kwargs):
            assert 'UnityProject' in args[0]  # In temp folder
            assert args[1] == os.path.normpath('Assets/TestProject')
            assert args[2] == os.path.normpath('Output/TestProject_1.0.0_Release.unitypackage')
            create_empty_file(args[2])
            return 0

        unity_runner_instance = MagicMock()
        unity_runner_instance.export_unitypackage = export_unitypackage_mock
        unity_runner_mock.return_value = unity_runner_instance

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.0.0"
        csproj_instance.get_output_path.return_value = "bin/Output/Debug"
        csproj_mock.return_value = csproj_instance

        runner = CliRunner(env={"UNITY_PATH": "custom_unity.exe", "UNITY_USERNAME": None, "UNITY_PASSWORD": None,
                                "UNITY_SERIAL": None})
        with runner.isolated_filesystem():
            os.makedirs("bin/Output/Debug")
            create_empty_file("bin/Output/Debug/TestProject.dll")
            create_empty_file("bin/Output/Debug/TestProject.pdb")
            result = runner.invoke(
                cli.ugetcli, ['create'], obj={})

        assert result.exit_code == 0, result
        unity_runner_mock.assert_called_with('custom_unity.exe', None, None, None, False)

    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.UnityRunner')
    def test_cli_uget_create_with_unity_project_path(
        self, unity_runner_mock, csproj_mock):
        """Test cli: uget create with --unity-project-path"""

        # Mock running Unity to export unity package
        def export_unitypackage_mock(*args, **kwargs):
            assert 'MyUnityProject' in args[0]  # In temp folder
            assert args[1] == os.path.normpath('Assets/TestProject')
            assert args[2] == os.path.normpath('Output/TestProject_1.0.0_Release.unitypackage')
            create_empty_file(args[2])
            return 0

        unity_runner_instance = MagicMock()
        unity_runner_instance.export_unitypackage = export_unitypackage_mock
        unity_runner_mock.return_value = unity_runner_instance

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.0.0"
        csproj_instance.get_output_path.return_value = "bin/Output/Debug"
        csproj_mock.return_value = csproj_instance

        runner = CliRunner(env={"UNITY_PATH": None, "UNITY_USERNAME": None, "UNITY_PASSWORD": None,
                                "UNITY_SERIAL": None})
        with runner.isolated_filesystem():
            os.makedirs("bin/Output/Debug")
            create_empty_file("bin/Output/Debug/TestProject.dll")
            create_empty_file("bin/Output/Debug/TestProject.pdb")
            result = runner.invoke(
                cli.ugetcli, ['create', '--unity-path', 'unity.exe', '--unity-project-path', 'MyUnityProject'], obj={})

        assert result.exit_code == 0, result
        unity_runner_mock.assert_called_with('unity.exe', None, None, None, False)

    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.UnityRunner')
    def test_cli_uget_create_with_root_directory(
        self, unity_runner_mock, csproj_mock):
        """Test cli: uget create with --root-dir"""

        # Mock running Unity to export unity package
        def export_unitypackage_mock(*args, **kwargs):
            assert 'UnityProject' in args[0]  # In temp folder
            assert args[1] == os.path.normpath('Assets/MyUnityPackageRoot')
            assert args[2] == os.path.normpath('Output/TestProject_1.0.0_Release.unitypackage')
            create_empty_file(args[2])
            return 0

        unity_runner_instance = MagicMock()
        unity_runner_instance.export_unitypackage = export_unitypackage_mock
        unity_runner_mock.return_value = unity_runner_instance

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.0.0"
        csproj_instance.get_output_path.return_value = "bin/Output/Debug"
        csproj_mock.return_value = csproj_instance

        runner = CliRunner(env={"UNITY_PATH": None, "UNITY_USERNAME": None, "UNITY_PASSWORD": None,
                                "UNITY_SERIAL": None})
        with runner.isolated_filesystem():
            os.makedirs("bin/Output/Debug")
            create_empty_file("bin/Output/Debug/TestProject.dll")
            create_empty_file("bin/Output/Debug/TestProject.pdb")
            result = runner.invoke(
                cli.ugetcli, ['create', '--unity-path', 'unity.exe', '--root-dir', 'MyUnityPackageRoot'], obj={})

        assert result.exit_code == 0, result
        unity_runner_mock.assert_called_with('unity.exe', None, None, None, False)


    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.UnityRunner')
    def test_cli_uget_create_with_clean(
        self, unity_runner_mock, csproj_mock):
        """Test cli: uget create with --clean"""

        # Mock running Unity to export unity package
        def export_unitypackage_mock(*args, **kwargs):
            assert 'UnityProject' in args[0]  # In temp folder
            assert args[1] == os.path.normpath('Assets/TestProject')
            assert args[2] == os.path.normpath('Output/TestProject_1.0.0_Release.unitypackage')
            create_empty_file(args[2])
            return 0

        unity_runner_instance = MagicMock()
        unity_runner_instance.export_unitypackage = export_unitypackage_mock
        unity_runner_mock.return_value = unity_runner_instance

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.0.0"
        csproj_instance.get_output_path.return_value = "bin/Output/Debug"
        csproj_mock.return_value = csproj_instance

        runner = CliRunner(env={"UNITY_PATH": None, "UNITY_USERNAME": None, "UNITY_PASSWORD": None,
                                "UNITY_SERIAL": None})
        with runner.isolated_filesystem():
            os.makedirs("bin/Output/Debug")
            create_empty_file("bin/Output/Debug/TestProject.dll")
            create_empty_file("bin/Output/Debug/TestProject.pdb")
            os.makedirs("Output/")
            create_empty_file("Output/TestProject_0.1.0_Release.unitypackage")  # Should be removed
            create_empty_file("Output/TestProject_0.1.1_Release.unitypackage")  # Should be removed
            create_empty_file("Output/TestProject_0.1.0_Debug.unitypackage")  # Should NOT be removed
            result = runner.invoke(
                cli.ugetcli, ['create', '--unity-path', 'unity.exe', '--clean'], obj={})

            assert not os.path.isfile("Output/TestProject_0.1.0_Release.unitypackage")
            assert not os.path.isfile("Output/TestProject_0.1.1_Release.unitypackage")
            assert os.path.isfile("Output/TestProject_0.1.0_Debug.unitypackage")

        assert result.exit_code == 0, result
        unity_runner_mock.assert_called_with('unity.exe', None, None, None, False)

    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.UnityRunner')
    def test_cli_uget_create_with_unity_username(
        self, unity_runner_mock, csproj_mock):
        """Test cli: uget create with --unity-username"""

        # Mock running Unity to export unity package
        def export_unitypackage_mock(*args, **kwargs):
            assert 'UnityProject' in args[0]  # In temp folder
            assert args[1] == os.path.normpath('Assets/TestProject')
            assert args[2] == os.path.normpath('Output/TestProject_1.0.0_Release.unitypackage')
            create_empty_file(args[2])
            return 0

        unity_runner_instance = MagicMock()
        unity_runner_instance.export_unitypackage = export_unitypackage_mock
        unity_runner_mock.return_value = unity_runner_instance

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.0.0"
        csproj_instance.get_output_path.return_value = "bin/Output/Debug"
        csproj_mock.return_value = csproj_instance

        runner = CliRunner(env={"UNITY_PATH": None, "UNITY_USERNAME": None, "UNITY_PASSWORD": None,
                                "UNITY_SERIAL": None})
        with runner.isolated_filesystem():
            os.makedirs("bin/Output/Debug")
            create_empty_file("bin/Output/Debug/TestProject.dll")
            create_empty_file("bin/Output/Debug/TestProject.pdb")
            result = runner.invoke(
                cli.ugetcli, ['create', '--unity-path', 'unity.exe', '--unity-username', 'test_username'], obj={})

        assert result.exit_code == 0, result
        unity_runner_mock.assert_called_with('unity.exe', 'test_username', None, None, False)


    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.UnityRunner')
    def test_cli_uget_create_with_unity_username_env(
        self, unity_runner_mock, csproj_mock):
        """Test cli: uget create with UNITY_USERNAME env variable"""

        # Mock running Unity to export unity package
        def export_unitypackage_mock(*args, **kwargs):
            assert 'UnityProject' in args[0]  # In temp folder
            assert args[1] == os.path.normpath('Assets/TestProject')
            assert args[2] == os.path.normpath('Output/TestProject_1.0.0_Release.unitypackage')
            create_empty_file(args[2])
            return 0

        unity_runner_instance = MagicMock()
        unity_runner_instance.export_unitypackage = export_unitypackage_mock
        unity_runner_mock.return_value = unity_runner_instance

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.0.0"
        csproj_instance.get_output_path.return_value = "bin/Output/Debug"
        csproj_mock.return_value = csproj_instance

        runner = CliRunner(env={"UNITY_PATH": None, "UNITY_USERNAME": "test_username1", "UNITY_PASSWORD": None,
                                "UNITY_SERIAL": None})
        with runner.isolated_filesystem():
            os.makedirs("bin/Output/Debug")
            create_empty_file("bin/Output/Debug/TestProject.dll")
            create_empty_file("bin/Output/Debug/TestProject.pdb")
            result = runner.invoke(
                cli.ugetcli, ['create', '--unity-path', 'unity.exe'], obj={})

        assert result.exit_code == 0, result
        unity_runner_mock.assert_called_with('unity.exe', 'test_username1', None, None, False)

    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.UnityRunner')
    def test_cli_uget_create_with_unity_password(
        self, unity_runner_mock, csproj_mock):
        """Test cli: uget create with --unity-password"""

        # Mock running Unity to export unity package
        def export_unitypackage_mock(*args, **kwargs):
            assert 'UnityProject' in args[0]  # In temp folder
            assert args[1] == os.path.normpath('Assets/TestProject')
            assert args[2] == os.path.normpath('Output/TestProject_1.0.0_Release.unitypackage')
            create_empty_file(args[2])
            return 0

        unity_runner_instance = MagicMock()
        unity_runner_instance.export_unitypackage = export_unitypackage_mock
        unity_runner_mock.return_value = unity_runner_instance

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.0.0"
        csproj_instance.get_output_path.return_value = "bin/Output/Debug"
        csproj_mock.return_value = csproj_instance

        runner = CliRunner(env={"UNITY_PATH": None, "UNITY_USERNAME": None, "UNITY_PASSWORD": None,
                                "UNITY_SERIAL": None})
        with runner.isolated_filesystem():
            os.makedirs("bin/Output/Debug")
            create_empty_file("bin/Output/Debug/TestProject.dll")
            create_empty_file("bin/Output/Debug/TestProject.pdb")
            result = runner.invoke(
                cli.ugetcli, ['create', '--unity-path', 'unity.exe', '--unity-password', 'password'], obj={})

        assert result.exit_code == 0, result
        unity_runner_mock.assert_called_with('unity.exe', None, 'password', None, False)

    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.UnityRunner')
    def test_cli_uget_create_with_unity_password_env(
        self, unity_runner_mock, csproj_mock):
        """Test cli: uget create with UNITY_PASSWORD env variable"""

        # Mock running Unity to export unity package
        def export_unitypackage_mock(*args, **kwargs):
            assert 'UnityProject' in args[0]  # In temp folder
            assert args[1] == os.path.normpath('Assets/TestProject')
            assert args[2] == os.path.normpath('Output/TestProject_1.0.0_Release.unitypackage')
            create_empty_file(args[2])
            return 0

        unity_runner_instance = MagicMock()
        unity_runner_instance.export_unitypackage = export_unitypackage_mock
        unity_runner_mock.return_value = unity_runner_instance

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.0.0"
        csproj_instance.get_output_path.return_value = "bin/Output/Debug"
        csproj_mock.return_value = csproj_instance

        runner = CliRunner(env={"UNITY_PATH": None, "UNITY_USERNAME": None, "UNITY_PASSWORD": 'password',
                                "UNITY_SERIAL": None})
        with runner.isolated_filesystem():
            os.makedirs("bin/Output/Debug")
            create_empty_file("bin/Output/Debug/TestProject.dll")
            create_empty_file("bin/Output/Debug/TestProject.pdb")
            result = runner.invoke(
                cli.ugetcli, ['create', '--unity-path', 'unity.exe'], obj={})

        assert result.exit_code == 0, result
        unity_runner_mock.assert_called_with('unity.exe', None, 'password', None, False)

    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.UnityRunner')
    def test_cli_uget_create_with_unity_serial(
        self, unity_runner_mock, csproj_mock):
        """Test cli: uget create with --unity-serial"""

        # Mock running Unity to export unity package
        def export_unitypackage_mock(*args, **kwargs):
            assert 'UnityProject' in args[0]  # In temp folder
            assert args[1] == os.path.normpath('Assets/TestProject')
            assert args[2] == os.path.normpath('Output/TestProject_1.0.0_Release.unitypackage')
            create_empty_file(args[2])
            return 0

        unity_runner_instance = MagicMock()
        unity_runner_instance.export_unitypackage = export_unitypackage_mock
        unity_runner_mock.return_value = unity_runner_instance

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.0.0"
        csproj_instance.get_output_path.return_value = "bin/Output/Debug"
        csproj_mock.return_value = csproj_instance

        runner = CliRunner(env={"UNITY_PATH": None, "UNITY_USERNAME": None, "UNITY_PASSWORD": None,
                                "UNITY_SERIAL": None})
        with runner.isolated_filesystem():
            os.makedirs("bin/Output/Debug")
            create_empty_file("bin/Output/Debug/TestProject.dll")
            create_empty_file("bin/Output/Debug/TestProject.pdb")
            result = runner.invoke(
                cli.ugetcli, ['create', '--unity-path', 'unity.exe', '--unity-serial', 'myserial'], obj={})

        assert result.exit_code == 0, result
        unity_runner_mock.assert_called_with('unity.exe', None, None, 'myserial', False)

    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.UnityRunner')
    def test_cli_uget_create_with_unity_serial_env(
        self, unity_runner_mock, csproj_mock):
        """Test cli: uget create with UNITY_SERIAL env variable"""

        # Mock running Unity to export unity package
        def export_unitypackage_mock(*args, **kwargs):
            assert 'UnityProject' in args[0]  # In temp folder
            assert args[1] == os.path.normpath('Assets/TestProject')
            assert args[2] == os.path.normpath('Output/TestProject_1.0.0_Release.unitypackage')
            create_empty_file(args[2])
            return 0

        unity_runner_instance = MagicMock()
        unity_runner_instance.export_unitypackage = export_unitypackage_mock
        unity_runner_mock.return_value = unity_runner_instance

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.0.0"
        csproj_instance.get_output_path.return_value = "bin/Output/Debug"
        csproj_mock.return_value = csproj_instance

        runner = CliRunner(env={"UNITY_PATH": None, "UNITY_USERNAME": None, "UNITY_PASSWORD": None,
                                "UNITY_SERIAL": 'myserial'})
        with runner.isolated_filesystem():
            os.makedirs("bin/Output/Debug")
            create_empty_file("bin/Output/Debug/TestProject.dll")
            create_empty_file("bin/Output/Debug/TestProject.pdb")
            result = runner.invoke(
                cli.ugetcli, ['create', '--unity-path', 'unity.exe'], obj={})

        assert result.exit_code == 0, result
        unity_runner_mock.assert_called_with('unity.exe', None, None, 'myserial', False)

    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.UnityRunner')
    def test_cli_uget_create_with_config_json(
        self, unity_runner_mock, csproj_mock):
        """Test cli: uget create with options loaded via config json"""

        # Mock running Unity to export unity package
        def export_unitypackage_mock(*args, **kwargs):
            assert 'CustomUnityProject' in args[0]  # In temp folder
            assert args[1] == os.path.normpath('Assets/MyUnityPackage')
            assert args[2] == os.path.normpath('CustomOutput/TestProject_1.0.0_Debug.unitypackage')
            create_empty_file(args[2])
            return 0

        unity_runner_instance = MagicMock()
        unity_runner_instance.export_unitypackage = export_unitypackage_mock
        unity_runner_mock.return_value = unity_runner_instance

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.0.0"
        csproj_instance.get_output_path.return_value = "bin/Output/Debug"
        csproj_mock.return_value = csproj_instance

        config_data = {
            "output_dir": "CustomOutput",
            "configuration": "Debug",
            "unity_path": "custom_unity.exe",
            "unity_project_path": "CustomUnityProject",
            "root_dir": "MyUnityPackage",
            "clean": True,
            "unity_username": "my_username",
            "unity_password": "my_password",
            "unity_serial": "my_serial"
        }

        runner = CliRunner(env={"UNITY_PATH": None, "UNITY_USERNAME": None, "UNITY_PASSWORD": None,
                                "UNITY_SERIAL": None})
        with runner.isolated_filesystem():
            os.makedirs("bin/Output/Debug")
            create_empty_file("bin/Output/Debug/TestProject.dll")
            create_empty_file("bin/Output/Debug/TestProject.pdb")
            os.makedirs("CustomOutput/")
            create_empty_file("CustomOutput/TestProject_0.1.0_Release.unitypackage")  # Should be removed

            result = runner.invoke(
                cli.ugetcli, ['create', '--config', json.dumps(config_data)], obj={})

            assert not os.path.isfile("Output/TestProject_0.1.0_Release.unitypackage")

        assert result.exit_code == 0, result
        unity_runner_mock.assert_called_with('custom_unity.exe', "my_username", "my_password", "my_serial", False)


    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.UnityRunner')
    def test_cli_uget_create_with_config_file(
        self, unity_runner_mock, csproj_mock):
        """Test cli: uget create with options loaded via config file"""

        # Mock running Unity to export unity package
        def export_unitypackage_mock(*args, **kwargs):
            assert 'CustomUnityProject' in args[0]  # In temp folder
            assert args[1] == os.path.normpath('Assets/MyUnityPackage')
            assert args[2] == os.path.normpath('CustomOutput/TestProject_1.0.0_Debug.unitypackage')
            create_empty_file(args[2])
            return 0

        unity_runner_instance = MagicMock()
        unity_runner_instance.export_unitypackage = export_unitypackage_mock
        unity_runner_mock.return_value = unity_runner_instance

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.0.0"
        csproj_instance.get_output_path.return_value = "bin/Output/Debug"
        csproj_mock.return_value = csproj_instance

        config_data = {
            "output_dir": "CustomOutput",
            "configuration": "Debug",
            "unity_path": "custom_unity.exe",
            "unity_project_path": "CustomUnityProject",
            "root_dir": "MyUnityPackage",
            "clean": True,
            "unity_username": "my_username",
            "unity_password": "my_password",
            "unity_serial": "my_serial"
        }

        runner = CliRunner(env={"UNITY_PATH": None, "UNITY_USERNAME": None, "UNITY_PASSWORD": None,
                                "UNITY_SERIAL": None})
        with runner.isolated_filesystem():
            os.makedirs("bin/Output/Debug")
            create_empty_file("bin/Output/Debug/TestProject.dll")
            create_empty_file("bin/Output/Debug/TestProject.pdb")
            os.makedirs("CustomOutput/")
            create_empty_file("CustomOutput/TestProject_0.1.0_Release.unitypackage")  # Should be removed

            with open('config_test.json', 'w') as f:
                json.dump(config_data, f)

            result = runner.invoke(
                cli.ugetcli, ['create', '--config-path', 'config_test.json'], obj={})

            assert not os.path.isfile("Output/TestProject_0.1.0_Release.unitypackage")

        assert result.exit_code == 0, result
        unity_runner_mock.assert_called_with('custom_unity.exe', "my_username", "my_password", "my_serial", False)

