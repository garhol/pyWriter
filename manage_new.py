#!/usr/bin/env python

# copy this manage.py up a level and use this one to run mangement commands.

import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pyWriter.lib.settings.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
