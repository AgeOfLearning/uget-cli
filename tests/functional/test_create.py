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
    @patch('ugetcli.uget.UnityPackageRunner')
    def test_cli_uget_create(
        self, unitypackage_runner_mock, csproj_mock):
        """Test cli: uget create with default options"""

        invocation_results = [False]

        # Mock running Unity to export unity package
        def export_unitypackage_mock(*args, **kwargs):
            assert 'UnityProject' in args[0]  # In temp folder
            assert args[0] == os.path.normpath('UnityProject/Assets/TestProject')
            assert args[1] == os.path.normpath('Output/TestProject_1.0.0_Release.unitypackage')
            create_empty_file(args[1])
            invocation_results[0] = True
            return 0

        unitypackage_runner_instance = MagicMock()
        unitypackage_runner_instance.export_unitypackage = export_unitypackage_mock
        unitypackage_runner_mock.return_value = unitypackage_runner_instance

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.0.0"
        csproj_instance.get_output_path.return_value = "bin/Output/Debug"
        csproj_instance.path = "TestProject.csproj"
        csproj_mock.return_value = csproj_instance
        csproj_mock.get_csproj_at_path.return_value = "TestProject.csproj"

        runner = CliRunner(env={})
        with runner.isolated_filesystem():
            os.makedirs("bin/Output/Debug")
            create_empty_file("bin/Output/Debug/TestProject.dll")
            create_empty_file("bin/Output/Debug/TestProject.pdb")
            result = runner.invoke(cli.ugetcli, ['create'], obj={})

        assert result.exit_code == 0, result
        unitypackage_runner_mock.assert_called_with(False)
        assert invocation_results[0], "did not invoke export_unitypackage_mock"

    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.UnityPackageRunner')
    def test_cli_uget_create_with_path_directory(
        self, unitypackage_runner_mock, csproj_mock):
        """Test cli: uget create with --path option when path is a directory"""

        invocation_results = [False]

        # Mock running Unity to export unity package
        def export_unitypackage_mock(*args, **kwargs):
            assert 'UnityProject' in args[0]  # In temp folder
            assert args[0] == os.path.normpath('UnityProject/Assets/TestProject')
            assert args[1] == os.path.normpath('Output/TestProject_1.0.0_Release.unitypackage')
            create_empty_file(args[1])
            invocation_results[0] = True
            return 0

        unitypackage_runner_instance = MagicMock()
        unitypackage_runner_instance.export_unitypackage = export_unitypackage_mock
        unitypackage_runner_mock.return_value = unitypackage_runner_instance

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.0.0"
        csproj_instance.get_output_path.return_value = "bin/Output/Debug"
        csproj_instance.path = "custom/MyProject.csproj"
        csproj_mock.return_value = csproj_instance

        runner = CliRunner(env={})
        with runner.isolated_filesystem():
            os.makedirs("custom/bin/Output/Debug")
            create_empty_file("custom/bin/Output/Debug/TestProject.dll")
            create_empty_file("custom/bin/Output/Debug/TestProject.pdb")
            result = runner.invoke(cli.ugetcli, ['create', '--path', 'custom/'], obj={})

        assert result.exit_code == 0, result
        unitypackage_runner_mock.assert_called_with(False)
        csproj_mock.assert_called_with('custom/')
        assert invocation_results[0], "did not invoke export_unitypackage_mock"

    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.UnityPackageRunner')
    def test_cli_uget_create_with_path_file(
        self, unitypackage_runner_mock, csproj_mock):
        """Test cli: uget create with --path option when path is a .csproj file"""

        invocation_results = [False]

        # Mock running Unity to export unity package
        def export_unitypackage_mock(*args, **kwargs):
            assert 'UnityProject' in args[0]  # In temp folder
            assert args[0] == os.path.normpath('UnityProject/Assets/TestProject')
            assert args[1] == os.path.normpath('Output/TestProject_1.0.0_Release.unitypackage')
            create_empty_file(args[1])
            invocation_results[0] = True
            return 0

        unitypackage_runner_instance = MagicMock()
        unitypackage_runner_instance.export_unitypackage = export_unitypackage_mock
        unitypackage_runner_mock.return_value = unitypackage_runner_instance

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.0.0"
        csproj_instance.get_output_path.return_value = "bin/Output/Debug"
        csproj_instance.path = "custom/MyProject.csproj"
        csproj_mock.return_value = csproj_instance

        runner = CliRunner(env={})
        with runner.isolated_filesystem():
            os.makedirs("custom/bin/Output/Debug")
            create_empty_file("custom/bin/Output/Debug/TestProject.dll")
            create_empty_file("custom/bin/Output/Debug/TestProject.pdb")
            result = runner.invoke(cli.ugetcli, ['create', '--path', 'custom/MyProject.csproj'], obj={})

        assert result.exit_code == 0, result
        unitypackage_runner_mock.assert_called_with(False)
        csproj_mock.assert_called_with('custom/MyProject.csproj')
        assert invocation_results[0], "did not invoke export_unitypackage_mock"

    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.UnityPackageRunner')
    def test_cli_uget_create_with_output_dir(
        self, unitypackage_runner_mock, csproj_mock):
        """Test cli: uget create with --output-dir option"""

        invocation_results = [False]

        # Mock running Unity to export unity package
        def export_unitypackage_mock(*args, **kwargs):
            assert 'UnityProject' in args[0]  # In temp folder
            assert args[0] == os.path.normpath('UnityProject/Assets/TestProject')
            assert args[1] == os.path.normpath('out/TestProject_1.0.0_Release.unitypackage')
            create_empty_file(args[1])
            invocation_results[0] = True
            return 0

        unitypackage_runner_instance = MagicMock()
        unitypackage_runner_instance.export_unitypackage = export_unitypackage_mock
        unitypackage_runner_mock.return_value = unitypackage_runner_instance

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.0.0"
        csproj_instance.get_output_path.return_value = "bin/Output/Debug"
        csproj_instance.path = "TestProject.csproj"
        csproj_mock.return_value = csproj_instance

        runner = CliRunner(env={})
        with runner.isolated_filesystem():
            os.makedirs("bin/Output/Debug")
            create_empty_file("bin/Output/Debug/TestProject.dll")
            create_empty_file("bin/Output/Debug/TestProject.pdb")
            result = runner.invoke(cli.ugetcli, ['create', '--output-dir', 'out'], obj={})

        assert result.exit_code == 0, result
        unitypackage_runner_mock.assert_called_with(False)
        assert invocation_results[0], "did not invoke export_unitypackage_mock"

    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.UnityPackageRunner')
    def test_cli_uget_create_with_configuration(
        self, unitypackage_runner_mock, csproj_mock):
        """Test cli: uget create with --configuration option"""

        invocation_results = [False]

        # Mock running Unity to export unity package
        def export_unitypackage_mock(*args, **kwargs):
            assert 'UnityProject' in args[0]  # In temp folder
            assert args[0] == os.path.normpath('UnityProject/Assets/TestProject')
            assert args[1] == os.path.normpath('Output/TestProject_1.0.0_Debug.unitypackage')
            create_empty_file(args[1])
            invocation_results[0] = True
            return 0

        unitypackage_runner_instance = MagicMock()
        unitypackage_runner_instance.export_unitypackage = export_unitypackage_mock
        unitypackage_runner_mock.return_value = unitypackage_runner_instance

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.0.0"
        csproj_instance.get_output_path.return_value = "bin/Output/Debug"
        csproj_instance.path = "TestProject.csproj"
        csproj_mock.return_value = csproj_instance

        runner = CliRunner(env={})
        with runner.isolated_filesystem():
            os.makedirs("bin/Output/Debug")
            create_empty_file("bin/Output/Debug/TestProject.dll")
            create_empty_file("bin/Output/Debug/TestProject.pdb")
            result = runner.invoke(cli.ugetcli, ['create', '--configuration', 'Debug'],
                                   obj={})

        assert result.exit_code == 0, result
        unitypackage_runner_mock.assert_called_with(False)
        assert invocation_results[0], "did not invoke export_unitypackage_mock"

    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.UnityPackageRunner')
    def test_cli_uget_create_with_unity_project_path(
        self, unitypackage_runner_mock, csproj_mock):
        """Test cli: uget create with --unity-project-path"""

        invocation_results = [False]

        # Mock running Unity to export unity package
        def export_unitypackage_mock(*args, **kwargs):
            assert 'MyUnityProject' in args[0]  # In temp folder
            assert args[0] == os.path.normpath('MyUnityProject/Assets/TestProject')
            assert args[1] == os.path.normpath('Output/TestProject_1.0.0_Release.unitypackage')
            create_empty_file(args[1])
            invocation_results[0] = True
            return 0

        unitypackage_runner_instance = MagicMock()
        unitypackage_runner_instance.export_unitypackage = export_unitypackage_mock
        unitypackage_runner_mock.return_value = unitypackage_runner_instance

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.0.0"
        csproj_instance.get_output_path.return_value = "bin/Output/Debug"
        csproj_instance.path = "TestProject.csproj"
        csproj_mock.return_value = csproj_instance

        runner = CliRunner(env={})
        with runner.isolated_filesystem():
            os.makedirs("bin/Output/Debug")
            create_empty_file("bin/Output/Debug/TestProject.dll")
            create_empty_file("bin/Output/Debug/TestProject.pdb")
            result = runner.invoke(
                cli.ugetcli, ['create', '--unity-project-path', 'MyUnityProject'], obj={})

        assert result.exit_code == 0, result
        unitypackage_runner_mock.assert_called_with(False)
        assert invocation_results[0], "did not invoke export_unitypackage_mock"

    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.UnityPackageRunner')
    def test_cli_uget_create_with_root_directory(
        self, unitypackage_runner_mock, csproj_mock):
        """Test cli: uget create with --root-dir"""

        invocation_results = [False]

        # Mock running Unity to export unity package
        def export_unitypackage_mock(*args, **kwargs):
            assert 'UnityProject' in args[0]  # In temp folder
            assert args[0] == os.path.normpath('UnityProject/Assets/MyUnityPackageRoot')
            assert args[1] == os.path.normpath('Output/TestProject_1.0.0_Release.unitypackage')
            create_empty_file(args[1])
            invocation_results[0] = True
            return 0

        unitypackage_runner_instance = MagicMock()
        unitypackage_runner_instance.export_unitypackage = export_unitypackage_mock
        unitypackage_runner_mock.return_value = unitypackage_runner_instance

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.0.0"
        csproj_instance.get_output_path.return_value = "bin/Output/Debug"
        csproj_instance.path = "TestProject.csproj"
        csproj_mock.return_value = csproj_instance

        runner = CliRunner(env={})
        with runner.isolated_filesystem():
            os.makedirs("bin/Output/Debug")
            create_empty_file("bin/Output/Debug/TestProject.dll")
            create_empty_file("bin/Output/Debug/TestProject.pdb")
            result = runner.invoke(
                cli.ugetcli, ['create', '--root-dir', 'MyUnityPackageRoot'], obj={})

        assert result.exit_code == 0, result
        unitypackage_runner_mock.assert_called_with(False)
        assert invocation_results[0], "did not invoke export_unitypackage_mock"

    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.UnityPackageRunner')
    def test_cli_uget_create_with_clean(
        self, unitypackage_runner_mock, csproj_mock):
        """Test cli: uget create with --clean"""

        invocation_results = [False]

        # Mock running Unity to export unity package
        def export_unitypackage_mock(*args, **kwargs):
            assert 'UnityProject' in args[0]  # In temp folder
            assert args[0] == os.path.normpath('UnityProject/Assets/TestProject')
            assert args[1] == os.path.normpath('Output/TestProject_1.0.0_Release.unitypackage')
            create_empty_file(args[1])
            invocation_results[0] = True
            return 0

        unitypackage_runner_instance = MagicMock()
        unitypackage_runner_instance.export_unitypackage = export_unitypackage_mock
        unitypackage_runner_mock.return_value = unitypackage_runner_instance

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.0.0"
        csproj_instance.get_output_path.return_value = "bin/Output/Debug"
        csproj_instance.path = "TestProject.csproj"
        csproj_mock.return_value = csproj_instance

        runner = CliRunner(env={})
        with runner.isolated_filesystem():
            os.makedirs("bin/Output/Debug")
            create_empty_file("bin/Output/Debug/TestProject.dll")
            create_empty_file("bin/Output/Debug/TestProject.pdb")
            os.makedirs("Output/")
            create_empty_file("Output/TestProject_0.1.0_Release.unitypackage")  # Should be removed
            create_empty_file("Output/TestProject_0.1.1_Release.unitypackage")  # Should be removed
            create_empty_file("Output/TestProject_0.1.0_Debug.unitypackage")  # Should NOT be removed
            result = runner.invoke(
                cli.ugetcli, ['create', '--clean'], obj={})

            assert not os.path.isfile("Output/TestProject_0.1.0_Release.unitypackage")
            assert not os.path.isfile("Output/TestProject_0.1.1_Release.unitypackage")
            assert os.path.isfile("Output/TestProject_0.1.0_Debug.unitypackage")

        assert result.exit_code == 0, result
        unitypackage_runner_mock.assert_called_with(False)
        assert invocation_results[0], "did not invoke export_unitypackage_mock"

    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.UnityPackageRunner')
    def test_cli_uget_create_with_unity_username(
        self, unitypackage_runner_mock, csproj_mock):
        """Test cli: uget create with --unity-username"""

        invocation_results = [False]

        # Mock running Unity to export unity package
        def export_unitypackage_mock(*args, **kwargs):
            assert 'UnityProject' in args[0]  # In temp folder
            assert args[0] == os.path.normpath('UnityProject/Assets/TestProject')
            assert args[1] == os.path.normpath('Output/TestProject_1.0.0_Release.unitypackage')
            create_empty_file(args[1])
            invocation_results[0] = True
            return 0

        unitypackage_runner_instance = MagicMock()
        unitypackage_runner_instance.export_unitypackage = export_unitypackage_mock
        unitypackage_runner_mock.return_value = unitypackage_runner_instance

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.0.0"
        csproj_instance.get_output_path.return_value = "bin/Output/Debug"
        csproj_instance.path = "TestProject.csproj"
        csproj_mock.return_value = csproj_instance

        runner = CliRunner(env={})
        with runner.isolated_filesystem():
            os.makedirs("bin/Output/Debug")
            create_empty_file("bin/Output/Debug/TestProject.dll")
            create_empty_file("bin/Output/Debug/TestProject.pdb")
            result = runner.invoke(
                cli.ugetcli, ['create'], obj={})

        assert result.exit_code == 0, result
        unitypackage_runner_mock.assert_called_with(False)
        assert invocation_results[0], "did not invoke export_unitypackage_mock"

    @patch('ugetcli.uget.CsProj')
    @patch('ugetcli.uget.UnityPackageRunner')
    def test_cli_uget_create_with_config_json(
        self, unitypackage_runner_mock, csproj_mock):
        """Test cli: uget create with options loaded via config json"""

        invocation_results = [False]

        # Mock running Unity to export unity package
        def export_unitypackage_mock(*args, **kwargs):
            assert 'CustomUnityProject' in args[0]  # In temp folder
            assert args[0] == os.path.normpath('CustomUnityProject/Assets/MyUnityPackage')
            assert args[1] == os.path.normpath('CustomOutput/TestProject_1.0.0_Debug.unitypackage')
            create_empty_file(args[1])
            invocation_results[0] = True
            return 0

        unitypackage_runner_instance = MagicMock()
        unitypackage_runner_instance.export_unitypackage = export_unitypackage_mock
        unitypackage_runner_mock.return_value = unitypackage_runner_instance

        csproj_instance = MagicMock()
        csproj_instance.get_assembly_name.return_value = "TestProject"
        csproj_instance.get_assembly_version.return_value = "1.0.0"
        csproj_instance.get_output_path.return_value = "bin/Output/Debug"
        csproj_instance.path = "TestProject.csproj"
        csproj_mock.return_value = csproj_instance

        config_data = {
            "output_dir": "CustomOutput",
            "configuration": "Debug",
            "unity_project_path": "CustomUnityProject",
            "root_dir": "MyUnityPackage",
            "clean": True,
        }

        runner = CliRunner(env={})
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
        unitypackage_runner_mock.assert_called_with(False)
        assert invocation_results[0], "did not invoke export_unitypackage_mock"
