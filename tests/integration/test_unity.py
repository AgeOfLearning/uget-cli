#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Integration tests for `ugetcli` package - `unity` module.
Tests functionality of the Unity Runner integration
"""
import unittest
import os
from mock import MagicMock, patch

from ugetcli.utils import temp_dir
from ugetcli.unity import UnityRunner


class TestUGetCliUnityRunner(unittest.TestCase):
    """Tests for `ugetcli` package - `unity` module"""

    @patch('ugetcli.unity.Popen')
    @patch('ugetcli.unity.open')
    def test_unity_runner_export_unitypackage(self, mock_open, mock_popen):
        """Test UnityRunner.export_unitypackage"""
        mock_open_handler = MagicMock()
        mock_open.return_value = mock_open_handler

        mock_process = MagicMock()
        mock_process.wait.return_value = 0
        mock_popen.return_value = mock_process

        with temp_dir() as temp_dir_path:
            unity_exe = "Editor.exe"
            project_path = "UnityProjects/MyProject"
            package_root = "MyProject"
            output_path = "Output/MyProject.unitypackage"
            username = "test_username"
            password = "test_password"
            serial = "test_serial"

            expected_unity_log_path = os.path.join(temp_dir_path, UnityRunner.log_filename)
            std_out_err_log_path = os.path.join(temp_dir_path, UnityRunner.stdout_filename)

            with open(std_out_err_log_path, "wb") as expected_std_out_err:
                mock_open_handler.__enter__.return_value = expected_std_out_err

                unity_runner = UnityRunner(unity_exe, username, password, serial)
                assert unity_runner.export_unitypackage(project_path, package_root, output_path, temp_dir_path) == 0

                expected_command = "{unity} -projectPath {project_path} -exportPackage {package_root} {output_path} " \
                                   "-logFile {unity_log} -batchmode -quit -username {username} -password {password} " \
                                   "-serial {serial}"\
                    .format(unity=unity_exe, project_path=project_path, package_root=package_root,
                            output_path=os.path.abspath(output_path), unity_log=expected_unity_log_path,
                            username=username, password=password, serial=serial)
                mock_popen.assert_called_with(expected_command, stderr=expected_std_out_err, stdout=expected_std_out_err)
