""" Testing the Main Module.
"""
import builtins
import sys
from pathlib import Path

import changelist_data
import pytest

from changelist_foci.__main__ import main


class PrintCollector:  # Author: DK96-OS
    def __init__(self):
        self.collection: str = ''

    def get_output(self) -> str:
        return self.collection

    def append_print_output(self, output: str):
        self.collection = self.collection + output

    def assert_expected(self, expected: str):
        assert self.collection == expected

    def get_mock_print(self):
        def _collection(result, **kwargs):
            self.append_print_output(result)
        return _collection


CHANGELIST_DATA_FILE_PATH = Path(changelist_data.storage.file_validation.CHANGELISTS_FILE_PATH_STR)
WORKSPACE_DATA_FILE_PATH = Path(changelist_data.storage.file_validation.WORKSPACE_FILE_PATH_STR)

CHANGELIST_DATA_SAMPLE_1 = """<?xml version='1.0' encoding='utf-8'?>
<changelists>
  <list id="c24cb1b3-d9d4-efe1-6d77-2f270a94f8c0" name="CL-FOCI Input Package" comment="">
    <change beforePath="/changelist_foci/input/input_data.py" beforeDir="false" afterPath="/changelist_foci/input/input_data.py" afterDir="false" />
    <change beforePath="/changelist_foci/input/argument_parser.py" beforeDir="false" afterPath="/changelist_foci/input/argument_parser.py" afterDir="false" />
    <change beforePath="/changelist_foci/input/argument_data.py" beforeDir="false" afterPath="/changelist_foci/input/argument_data.py" afterDir="false" />
    <change beforePath="/changelist_foci/input/__init__.py" beforeDir="false" afterPath="/changelist_foci/input/__init__.py" afterDir="false" />
  </list>
  <list id="b17e81ed-e7e9-ae8e-a184-bffc91c68445" name="CL-FOCI Main Package" comment="">
    <change beforePath="/changelist_foci/__init__.py" beforeDir="false" afterPath="/changelist_foci/__init__.py" afterDir="false" />
  </list>
  <list id="79474592-699f-0d51-bba8-4b6dd33537f7" name="Test Fixtures &amp; Data Providers" comment="">
    <change beforePath="/test/changelist_foci/conftest.py" beforeDir="false" afterPath="/test/changelist_foci/conftest.py" afterDir="false" />
  </list>
  <list id="fa3e75da-9391-3e89-3446-a71cdfe6ae37" name="Test Input Package" comment="">
    <change beforePath="/test/changelist_foci/input/test_method_validate_input.py" beforeDir="false" afterPath="/test/changelist_foci/input/test_method_validate_input.py" afterDir="false" />
    <change beforePath="/test/changelist_foci/input/test_argument_parser.py" beforeDir="false" afterPath="/test/changelist_foci/input/test_argument_parser.py" afterDir="false" />
  </list>
  <list id="e0d0366d-a5bd-0beb-3371-83affb120d85" name="Test Main Package" comment="">
    <change beforePath="/test/changelist_foci/test_main.py" beforeDir="false" afterPath="/test/changelist_foci/test_main.py" afterDir="false" />
  </list>
</changelists>"""

WORKSPACE_DATA_SAMPLE_1 = """<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="AutoImportSettings">
    <option name="autoReloadType" value="SELECTIVE" />
  </component>
  <component name="ChangeListManager">
    <list default="true" id="d08b98d0-78b5-88de-fa66-5b7e2c55ff33" name="CL-FOCI Input Package" comment="CL-FOCI Input Package">
      <change beforePath="$PROJECT_DIR$/changelist_foci/__init__.py" beforeDir="false" afterPath="$PROJECT_DIR$/changelist_foci/__init__.py" afterDir="false" />
      <change beforePath="$PROJECT_DIR$/changelist_foci/input/__init__.py" beforeDir="false" afterPath="$PROJECT_DIR$/changelist_foci/input/__init__.py" afterDir="false" />
      <change beforePath="$PROJECT_DIR$/changelist_foci/input/argument_data.py" beforeDir="false" afterPath="$PROJECT_DIR$/changelist_foci/input/argument_data.py" afterDir="false" />
      <change beforePath="$PROJECT_DIR$/changelist_foci/input/argument_parser.py" beforeDir="false" afterPath="$PROJECT_DIR$/changelist_foci/input/argument_parser.py" afterDir="false" />
      <change beforePath="$PROJECT_DIR$/changelist_foci/input/input_data.py" beforeDir="false" afterPath="$PROJECT_DIR$/changelist_foci/input/input_data.py" afterDir="false" />
    </list>
    <list id="0dad9b9d-959c-81d1-9ff9-9fc65ecfa784" name="Changelists Config" comment="">
      <change beforePath="$PROJECT_DIR$/.changelists/sort.xml" beforeDir="false" afterPath="$PROJECT_DIR$/.changelists/sort.xml" afterDir="false" />
    </list>
    <list id="99c5423e-e3b0-f07b-2b92-0e5c86792a2c" name="Test Fixtures &amp; Data Providers" comment="">
      <change beforePath="$PROJECT_DIR$/test/changelist_foci/conftest.py" beforeDir="false" afterPath="$PROJECT_DIR$/test/changelist_foci/conftest.py" afterDir="false" />
    </list>
    <list id="7a5f5562-3c5a-0e6e-d299-ab2c54fa9a3e" name="Test Input Package" comment="">
      <change beforePath="$PROJECT_DIR$/test/changelist_foci/input/test_argument_parser.py" beforeDir="false" afterPath="$PROJECT_DIR$/test/changelist_foci/input/test_argument_parser.py" afterDir="false" />
      <change beforePath="$PROJECT_DIR$/test/changelist_foci/input/test_method_validate_input.py" beforeDir="false" afterPath="$PROJECT_DIR$/test/changelist_foci/input/test_method_validate_input.py" afterDir="false" />
    </list>
    <list id="09965131-41f7-e136-a847-fba638ebeb47" name="Test Main Package" comment="">
      <change beforePath="$PROJECT_DIR$/test/changelist_foci/test_main.py" beforeDir="false" afterPath="$PROJECT_DIR$/test/changelist_foci/test_main.py" afterDir="false" />
    </list>
    <file path="$PROJECT_DIR$/test/changelist_foci/input/test_method_validate_input.py" ignored="true" />
    <option name="SHOW_DIALOG" value="false" />
    <option name="HIGHLIGHT_CONFLICTS" value="true" />
    <option name="HIGHLIGHT_NON_ACTIVE_CHANGELIST" value="false" />
    <option name="LAST_RESOLUTION" value="IGNORE" />
  </component>
</project>"""


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
    assert """CL-FOCI Input Package:
* Update changelist_foci/input/input_data.py
* Update changelist_foci/input/argument_parser.py
* Update changelist_foci/input/argument_data.py
* Update changelist_foci/input/__init__.py""" in result


def test_main_comment_changelist_sample_1(temp_cwd):
    sys.argv = ['cl-foci', '-c']
    #
    CHANGELIST_DATA_FILE_PATH.parent.mkdir(parents=True)
    CHANGELIST_DATA_FILE_PATH.touch()
    CHANGELIST_DATA_FILE_PATH.write_text(CHANGELIST_DATA_SAMPLE_1)
    
    main()
    # Check the Changelist Data file for the output
    result = CHANGELIST_DATA_FILE_PATH.read_text()
    assert """CL-FOCI Input Package:
* Update changelist_foci/input/input_data.py
* Update changelist_foci/input/argument_parser.py
* Update changelist_foci/input/argument_data.py
* Update changelist_foci/input/__init__.py""" in result
