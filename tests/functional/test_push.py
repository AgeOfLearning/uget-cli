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
