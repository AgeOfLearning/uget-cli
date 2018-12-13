#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Integration tests for `ugetcli` package - `msbuild` module.
Tests functionality of the MsBuild Runner integration
"""
import unittest
import os
import sys
from mock import MagicMock, patch


from ugetcli.utils import create_empty_file, temp_dir, escape_exe_path
from ugetcli.msbuild import MsBuildRunner


class TestUGetCliMSbuild(unittest.TestCase):
    """Tests for `ugetcli` package - `msbuild` module"""

    @patch('ugetcli.msbuild.sys')
    @patch('ugetcli.msbuild.call')
    def test_msbuild_runner_locate_msbuild_when_msvs_installed_win32(self, mock_call, mock_sys):
        """Test MsBuildRunner.locate_msbuild - returns msbuild path in the local system using Visual Studio path """
        if sys.platform != 'win32': # TODO: Fix unit test compatibility on non-windows platform
            return
        mock_call.return_value = 0
        mock_sys.configure_mock(platform='win32')
        vs_msbuild_dir = os.path.normpath("Microsoft Visual Studio\\1.0\\Community\\MSBuild\\1.0\\Bin\\")
        msbuild_name = "MSBuild.exe"
        with temp_dir() as tmp_root_dir:
            from ugetcli import msbuild
            with patch.dict(msbuild.os.environ, {'ProgramFiles': tmp_root_dir, 'WINDIR': tmp_root_dir}, clear=True):
                msbuild_dir_path = os.path.join(tmp_root_dir, vs_msbuild_dir)
                os.makedirs(msbuild_dir_path)
                msbuild_path = os.path.join(msbuild_dir_path, msbuild_name)
                create_empty_file(msbuild_path)
                assert MsBuildRunner.locate_msbuild() == msbuild_path

    @patch('ugetcli.msbuild.sys')
    @patch('ugetcli.msbuild.call')
    def test_msbuild_runner_locate_msbuild_when_dotnet_framework_installed_win32(self, mock_call, mock_sys):
        """Test MsBuildRunner.locate_msbuild - returns msbuild path in the local system using .NET Framework path """
        if sys.platform != 'win32': # TODO: Fix unit test compatibility on non-windows platform
            return
        mock_call.return_value = 0
        mock_sys.configure_mock(platform='win32')
        vs_msbuild_dir = os.path.normpath("Microsoft.NET\\Framework\\1.0\\")
        msbuild_name = "MSBuild.exe"
        with temp_dir() as tmp_root_dir:
            from ugetcli import msbuild
            with patch.dict(msbuild.os.environ, {'ProgramFiles': tmp_root_dir, 'WINDIR': tmp_root_dir}, clear=True):
                msbuild_dir_path = os.path.join(tmp_root_dir, vs_msbuild_dir)
                os.makedirs(msbuild_dir_path)
                msbuild_path = os.path.join(msbuild_dir_path, msbuild_name)
                create_empty_file(msbuild_path)
                assert MsBuildRunner.locate_msbuild() == msbuild_path

    @patch('ugetcli.msbuild.sys')
    @patch('ugetcli.msbuild.call')
    def test_msbuild_runner_locate_msbuild_when_non_win32(self, mock_call, mock_sys):
        """Test MsBuildRunner.locate_msbuild - returns msbuild on non-windows platform when msbuild is executable """
        mock_call.return_value = 0
        mock_sys.configure_mock(platform='darwin')
        assert MsBuildRunner.locate_msbuild() == "msbuild"

    @patch('ugetcli.msbuild.sys')
    @patch('ugetcli.msbuild.call')
    def test_msbuild_runner_locate_msbuild_returns_none_when_non_win32_when_not_found(self, mock_call, mock_sys):
        """Test MsBuildRunner.locate_msbuild - returns msbuild on non-windows platform when msbuild is executable """
        mock_call.return_value = -1
        mock_sys.configure_mock(platform='darwin')
        assert MsBuildRunner.locate_msbuild() == None

    @patch('ugetcli.msbuild.escape_exe_path')
    @patch('ugetcli.msbuild.Popen')
    def test_msbuild_build(self, mock_popen, mock_escape_exe_path):
        """Test MsBuildRunner.build - builds .csproj """
        mock_process_instance = MagicMock()
        mock_popen.return_value = mock_process_instance
        mock_process_instance.wait.return_value = 0
        mock_escape_exe_path.return_value = "msbuild.exe"
        with temp_dir() as tmp_root_dir:
            msbuild_path = os.path.join(tmp_root_dir, "msbuild.exe")
            project_path = os.path.join(tmp_root_dir, "Project.csproj")
            create_empty_file(msbuild_path)
            create_empty_file(project_path)
            configuration = "Debug"
            msbuild = MsBuildRunner(msbuild_path)
            msbuild.build(project_path, configuration, False)
            expected_command = 'msbuild.exe {project_path} /t:Build /p:"Configuration={configuration}"' \
                               ' /verbosity:{verbosity}'.format(project_path=project_path, configuration=configuration,
                                                                verbosity="minimal")
            mock_popen.assert_called_with(expected_command, shell=True)
            mock_process_instance.wait.assert_called()

    @patch('ugetcli.msbuild.escape_exe_path')
    @patch('ugetcli.msbuild.Popen')
    def test_msbuild_build_with_rebuild(self, mock_popen, mock_escape_exe_path):
        """Test MsBuildRunner.build - rebuilds .csproj """
        mock_process_instance = MagicMock()
        mock_popen.return_value = mock_process_instance
        mock_process_instance.wait.return_value = 0
        mock_escape_exe_path.return_value = "msbuild.exe"
        with temp_dir() as tmp_root_dir:
            msbuild_path = os.path.join(tmp_root_dir, "msbuild.exe")
            project_path = os.path.join(tmp_root_dir, "Project.csproj")
            create_empty_file(msbuild_path)
            create_empty_file(project_path)
            configuration = "Debug"
            msbuild = MsBuildRunner(msbuild_path)
            msbuild.build(project_path, configuration, True)
            expected_command = 'msbuild.exe {project_path} /t:Clean,Build /p:"Configuration={configuration}"' \
                               ' /verbosity:{verbosity}'.format(project_path=project_path, configuration=configuration,
                                                                verbosity="minimal")
            mock_popen.assert_called_with(expected_command, shell=True)
            mock_process_instance.wait.assert_called()

