#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `ugetcli` package."""

import unittest
from click.testing import CliRunner

from ugetcli import cli


class TestUGetCliHelp(unittest.TestCase):
    """Tests for `ugetcli` package - help command."""

    def test_cli_uget_help(self):
        """Test cli: uget help"""
        runner = CliRunner()
        result = runner.invoke(cli.ugetcli, ['--help'], obj={})
        assert result.exit_code == 0
        assert '--help' in result.output
        assert 'Show this message and exit.' in result.output
