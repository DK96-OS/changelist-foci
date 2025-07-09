""" Test Data Providers and Fixtures
"""
import os
import tempfile
from pathlib import Path

import changelist_data
import pytest
from changelist_data.changelist import Changelist
from changelist_data.file_change import FileChange


CHANGELIST_DATA_FILE_PATH = Path(changelist_data.storage.file_validation.CHANGELISTS_FILE_PATH_STR)
WORKSPACE_DATA_FILE_PATH = Path(changelist_data.storage.file_validation.WORKSPACE_FILE_PATH_STR)


def get_empty_xml() -> str:
    return ""


def get_no_changelist_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="AutoImportSettings">
    <option name="autoReloadType" value="NONE" />
  </component>
</project>"""


def get_simple_changelist_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="AutoImportSettings">
    <option name="autoReloadType" value="NONE" />
  </component>
  <component name="ChangeListManager">
    <list id="9f60fda2-421e-4a4b-bd0f-4c8f83a47c88" name="Simple" comment="Main Program Files">
      <change beforePath="$PROJECT_DIR$/main.py" beforeDir="false"  afterPath="$PROJECT_DIR$/main.py" afterDir="false" />
    </list>
  </component>
</project>"""


def get_simple_changelist_data_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8"?>
<changelists>
  <list id="9f60fda2-421e-4a4b-bd0f-4c8f83a47c88" name="Simple" comment="Main Program Files">
    <change beforePath="/main.py" beforeDir="false"  afterPath="/main.py" afterDir="false" />
  </list>
</changelists>"""


def get_multi_changelist_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="AutoImportSettings">
    <option name="autoReloadType" value="NONE" />
  </component>
  <component name="ChangeListManager">
    <list default="true" id="af84ea1b-1b24-407d-970f-9f3a2835e933" name="Main" comment="Main Program Files">
      <change beforePath="$PROJECT_DIR$/history.py" beforeDir="false" />
      <change beforePath="$PROJECT_DIR$/main.py" beforeDir="false" />
    </list>
    <list id="9f60fda2-421e-4a4b-bd0f-4c8f83a47c88" name="Test" comment="Test Files">
      <change afterPath="$PROJECT_DIR$/test/test_file.py" afterDir="false" />
    </list>
  </component>
</project>"""


@pytest.fixture()
def empty_changelists_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8"?>
<changelists></changelists>"""


@pytest.fixture()
def simple_changelists_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8"?>
<changelists>
<list id="9f60fda2-421e-4a4b-bd0f-4c8f83a47c88" name="Simple" comment="Main Program Files">
  <change beforePath="/main.py" beforeDir="false"  afterPath="/main.py" afterDir="false" />
</list>
</changelists>"""


@pytest.fixture()
def multi_changelists_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8"?>
<changelists>
<list default="true" id="af84ea1b-1b24-407d-970f-9f3a2835e933" name="Main" comment="Main Program Files">
  <change beforePath="/history.py" beforeDir="false" />
  <change beforePath="/main.py" beforeDir="false" />
</list>
<list id="9f60fda2-421e-4a4b-bd0f-4c8f83a47c88" name="Test" comment="Test Files">
  <change afterPath="/test/test_file.py" afterDir="false" />
</list>
</changelists>"""


@pytest.fixture()
def invalid_changelists_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8"?>
<changelists>
<lisat id="9f60fda2-421e-4a4b-bd0f-4c8f83a47c88" name="Main" comment="Main Files">
  <change beforePath="/main.py" beforeDir="false" />
</lisat>
</changelists>"""


def get_simple_changelist_data() -> Changelist:
    return Changelist(
        id='9f60fda2-421e-4a4b-bd0f-4c8f83a47c88',
        name="Simple",
        changes=[FileChange(before_path='/main.py', before_dir=False, after_path='/main.py', after_dir=False)],
        comment="Main Program Files",
        is_default=False,
    )


def get_main_changelist_data() -> Changelist:
    return Changelist(
        id='af84ea1b-1b24-407d-970f-9f3a2835e933',
        name="Main",
        changes=[
            FileChange(before_path='/history.py', before_dir=False),
            FileChange(before_path='/main.py', before_dir=False),
        ],
        comment="Main Program Files",
        is_default=True,
    )


REL_FILE_PATH_1 = 'main_package/__main__.py'
REL_FILE_PATH_2 = 'main_package/__init__.py'

ODD_FILE_EXT = '/resources/img/file.png.5'
ODD_FILE_EXT2 = '/resources/img/file-123-8.png.jpg.svg'


@pytest.fixture
def simple_cl1():
    return Changelist(
        id="1212434",
        name="ChangeList",
        changes=[
            FileChange(
                after_path="/module/file.txt",
                after_dir=False,
            )
        ],
    )


@pytest.fixture
def temp_cwd():
    """ Creates a Temporary Working Directory for Git subprocesses.
    """
    tdir = tempfile.TemporaryDirectory()
    initial_cwd = os.getcwd()
    os.chdir(tdir.name)
    yield tdir
    os.chdir(initial_cwd)
    tdir.cleanup()
    

class FileOutputCollector:
    """ Author: DK96-OS 2025
    """
    def __init__(self):
        self._output_str = ''
    
    def set_output(self, output_str: str, **kwargs):
        self._output_str = output_str
    
    def get_mock_write_text(self):
        return self.set_output
    
    def get_output(self) -> str:
        return self._output_str


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
