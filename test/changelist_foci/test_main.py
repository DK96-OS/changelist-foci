""" Testing the Main Module.
"""
import sys
import pytest

from changelist_foci.__main__ import main


def test_main_invalid_arg_raises_exit(temp_cwd):
    sys.argv = ['cl-foci', '--invalid_arg']
    with pytest.raises(SystemExit):
        main()
    sys.argv = sys.orig_argv