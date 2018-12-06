# -*- coding: utf-8 -*-

"""Console script for ugetcli."""
import sys
from ugetcli import cli


# Program entry point - execute cli.ugetcli Click Command Group
def main():
    sys.exit(cli.ugetcli(obj={}))  # pragma: no cover


if __name__ == "__main__":
    main()
