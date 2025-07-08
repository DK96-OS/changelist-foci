""" Testing the Main Module.
"""
import builtins
import sys

import pytest

from changelist_foci.__main__ import main
from test.changelist_foci.conftest import CHANGELIST_DATA_FILE_PATH, PrintCollector, CHANGELIST_DATA_SAMPLE_1, \
    WORKSPACE_DATA_FILE_PATH, WORKSPACE_DATA_SAMPLE_1


def test_main_invalid_arg_raises_exit(temp_cwd):
    sys.argv = ['cl-foci', '--invalid_arg']
    with pytest.raises(SystemExit):
        main()
    sys.argv = sys.orig_argv


def test_main_default_no_cl_data_file_raises_exit(temp_cwd):
    sys.argv = ['cl-foci']
    with pytest.raises(SystemExit, match='There are no Changelists.'):
        main()


def test_main_default_empty_cl_data_file_raises_exit(temp_cwd):
    sys.argv = ['cl-foci']
    # Create the Empty Changelist Data File.
    CHANGELIST_DATA_FILE_PATH.parent.mkdir(parents=True)
    CHANGELIST_DATA_FILE_PATH.touch()
    CHANGELIST_DATA_FILE_PATH.write_text("")
    #
    with pytest.raises(SystemExit, match='There are no Changelists.'):
        main()


def test_main_fx_empty_cl_data_file_raises_exit(temp_cwd):
    sys.argv = ['cl-foci', '-fx']
    # Create the Empty Changelist Data File.
    CHANGELIST_DATA_FILE_PATH.parent.mkdir(parents=True)
    CHANGELIST_DATA_FILE_PATH.touch()
    CHANGELIST_DATA_FILE_PATH.write_text("")
    #
    with pytest.raises(SystemExit, match='There are no Changelists.'):
        main()


def test_main_fax_empty_cl_data_file_raises_exit(temp_cwd):
    sys.argv = ['cl-foci', '-fax']
    # Create the Empty Changelist Data File.
    CHANGELIST_DATA_FILE_PATH.parent.mkdir(parents=True)
    CHANGELIST_DATA_FILE_PATH.touch()
    CHANGELIST_DATA_FILE_PATH.write_text("")
    #
    with pytest.raises(SystemExit, match='There are no Changelists.'):
        main()


def test_main_default_cl_data_file_no_lists_raises_exit(temp_cwd):
    sys.argv = ['cl-foci']
    # Create the Empty Changelist Data File.
    CHANGELIST_DATA_FILE_PATH.parent.mkdir(parents=True)
    CHANGELIST_DATA_FILE_PATH.touch()
    CHANGELIST_DATA_FILE_PATH.write_text("<changelists></changelists>")
    #
    with pytest.raises(SystemExit, match='There are no Changelists.'):
        main()


def test_main_default_cl_data_sample_1(temp_cwd, monkeypatch):
    sys.argv = ['cl-foci']
    collector = PrintCollector()
    monkeypatch.setattr(builtins, 'print', collector.get_mock_print())
    #
    CHANGELIST_DATA_FILE_PATH.parent.mkdir(parents=True)
    CHANGELIST_DATA_FILE_PATH.touch()
    CHANGELIST_DATA_FILE_PATH.write_text(CHANGELIST_DATA_SAMPLE_1)
    #
    main()
    collector.assert_expected("""CL-FOCI Input Package:
* Update changelist_foci/input/input_data.py
* Update changelist_foci/input/argument_parser.py
* Update changelist_foci/input/argument_data.py
* Update changelist_foci/input/__init__.py""")


def test_main_f_cl_data_sample_1(temp_cwd, monkeypatch):
    sys.argv = ['cl-foci', '-f']
    collector = PrintCollector()
    monkeypatch.setattr(builtins, 'print', collector.get_mock_print())
    #
    CHANGELIST_DATA_FILE_PATH.parent.mkdir(parents=True)
    CHANGELIST_DATA_FILE_PATH.touch()
    CHANGELIST_DATA_FILE_PATH.write_text(CHANGELIST_DATA_SAMPLE_1)
    #
    main()
    collector.assert_expected("""CL-FOCI Input Package:
* Update input_data.py
* Update argument_parser.py
* Update argument_data.py
* Update __init__.py""")


def test_main_x_cl_data_sample_1(temp_cwd, monkeypatch):
    sys.argv = ['cl-foci', '-x']
    collector = PrintCollector()
    monkeypatch.setattr(builtins, 'print', collector.get_mock_print())
    #
    CHANGELIST_DATA_FILE_PATH.parent.mkdir(parents=True)
    CHANGELIST_DATA_FILE_PATH.touch()
    CHANGELIST_DATA_FILE_PATH.write_text(CHANGELIST_DATA_SAMPLE_1)
    #
    main()
    collector.assert_expected("""CL-FOCI Input Package:
* Update changelist_foci/input/input_data
* Update changelist_foci/input/argument_parser
* Update changelist_foci/input/argument_data
* Update changelist_foci/input/__init__""")


def test_main_fx_cl_data_sample_1(temp_cwd, monkeypatch):
    sys.argv = ['cl-foci', '-fx']
    collector = PrintCollector()
    monkeypatch.setattr(builtins, 'print', collector.get_mock_print())
    #
    CHANGELIST_DATA_FILE_PATH.parent.mkdir(parents=True)
    CHANGELIST_DATA_FILE_PATH.touch()
    CHANGELIST_DATA_FILE_PATH.write_text(CHANGELIST_DATA_SAMPLE_1)
    #
    main()
    collector.assert_expected("""CL-FOCI Input Package:
* Update input_data
* Update argument_parser
* Update argument_data
* Update __init__""")


def test_main_a_cl_data_sample_1(temp_cwd, monkeypatch):
    sys.argv = ['cl-foci', '-a']
    collector = PrintCollector()
    monkeypatch.setattr(builtins, 'print', collector.get_mock_print())
    #
    CHANGELIST_DATA_FILE_PATH.parent.mkdir(parents=True)
    CHANGELIST_DATA_FILE_PATH.touch()
    CHANGELIST_DATA_FILE_PATH.write_text(CHANGELIST_DATA_SAMPLE_1)
    main()
    collector.assert_expected("""CL-FOCI Input Package:
* Update changelist_foci/input/input_data.py
* Update changelist_foci/input/argument_parser.py
* Update changelist_foci/input/argument_data.py
* Update changelist_foci/input/__init__.py

CL-FOCI Main Package:
* Update changelist_foci/__init__.py

Test Fixtures & Data Providers:
* Update test/changelist_foci/conftest.py

Test Input Package:
* Update test/changelist_foci/input/test_method_validate_input.py
* Update test/changelist_foci/input/test_argument_parser.py

Test Main Package:
* Update test/changelist_foci/test_main.py""")


def test_main_fa(temp_cwd, monkeypatch):
    sys.argv = ['cl-foci', '-fa']
    collector = PrintCollector()
    monkeypatch.setattr(builtins, 'print', collector.get_mock_print())
    #
    CHANGELIST_DATA_FILE_PATH.parent.mkdir(parents=True)
    CHANGELIST_DATA_FILE_PATH.touch()
    CHANGELIST_DATA_FILE_PATH.write_text(CHANGELIST_DATA_SAMPLE_1)
    #
    main()
    collector.assert_expected("""CL-FOCI Input Package:
* Update input_data.py
* Update argument_parser.py
* Update argument_data.py
* Update __init__.py

CL-FOCI Main Package:
* Update __init__.py

Test Fixtures & Data Providers:
* Update conftest.py

Test Input Package:
* Update test_method_validate_input.py
* Update test_argument_parser.py

Test Main Package:
* Update test_main.py""")


def test_main_fax_cl_data_sample_1(temp_cwd, monkeypatch):
    sys.argv = ['cl-foci', '-fax']
    collector = PrintCollector()
    monkeypatch.setattr(builtins, 'print', collector.get_mock_print())
    #
    CHANGELIST_DATA_FILE_PATH.parent.mkdir(parents=True)
    CHANGELIST_DATA_FILE_PATH.touch()
    CHANGELIST_DATA_FILE_PATH.write_text(CHANGELIST_DATA_SAMPLE_1)
    #
    main()
    collector.assert_expected("""CL-FOCI Input Package:
* Update input_data
* Update argument_parser
* Update argument_data
* Update __init__

CL-FOCI Main Package:
* Update __init__

Test Fixtures & Data Providers:
* Update conftest

Test Input Package:
* Update test_method_validate_input
* Update test_argument_parser

Test Main Package:
* Update test_main""")


def test_main_comment_workspace_sample_1(temp_cwd):
    sys.argv = ['cl-foci', '-c']
    #
    WORKSPACE_DATA_FILE_PATH.parent.mkdir(parents=True)
    WORKSPACE_DATA_FILE_PATH.touch()
    WORKSPACE_DATA_FILE_PATH.write_text(WORKSPACE_DATA_SAMPLE_1)
    #
    main()
    # Check the Workspace File for the output
    result = WORKSPACE_DATA_FILE_PATH.read_text()
    assert """CL-FOCI Input Package:&#10;* Update changelist_foci/input/__init__.py&#10;* Update changelist_foci/input/argument_data.py&#10;* Update changelist_foci/input/argument_parser.py&#10;* Update changelist_foci/input/input_data.py""" in result


def test_main_comment_changelist_sample_1(temp_cwd):
    sys.argv = ['cl-foci', '-c']
    #
    CHANGELIST_DATA_FILE_PATH.parent.mkdir(parents=True)
    CHANGELIST_DATA_FILE_PATH.touch()
    CHANGELIST_DATA_FILE_PATH.write_text(CHANGELIST_DATA_SAMPLE_1)
    #
    main()
    # Check the Changelist Data file for the output
    result = CHANGELIST_DATA_FILE_PATH.read_text()
    assert """CL-FOCI Input Package:&#10;* Update changelist_foci/input/input_data.py&#10;* Update changelist_foci/input/argument_parser.py&#10;* Update changelist_foci/input/argument_data.py&#10;* Update changelist_foci/input/__init__.py""" in result


def test_main_comment_fx_changelist_sample_1(temp_cwd):
    sys.argv = ['cl-foci', '-cfx']
    #
    CHANGELIST_DATA_FILE_PATH.parent.mkdir(parents=True)
    CHANGELIST_DATA_FILE_PATH.touch()
    CHANGELIST_DATA_FILE_PATH.write_text(CHANGELIST_DATA_SAMPLE_1)
    #
    main()
    # Check the Changelist Data file for the output
    result = CHANGELIST_DATA_FILE_PATH.read_text()
    assert """CL-FOCI Input Package:&#10;* Update input_data&#10;* Update argument_parser&#10;* Update argument_data&#10;* Update __init__""" in result
