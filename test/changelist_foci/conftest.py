""" Test Data Providers and Fixtures
"""
import os
import tempfile

import pytest
from changelist_data.changelist import Changelist
from changelist_data.file_change import FileChange


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
