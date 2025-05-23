""" Testing GenerateChangelistFOCI Package-Level Method.
 - Receives an Iterable of Changelist dataclass objects, and a FormatOptions dataclass object.
 - Prints Multi-Line Strings, starting with Changelist Name, add one additional line for each FileChange.
 - Each unique FormatOption may produces a unique result, but in cases such as root dir files the result is often the same.
"""
from changelist_data.xml.workspace import generate_changelists_from_xml

from changelist_foci import generate_changelist_foci, FormatOptions
from test.changelist_foci.conftest import get_simple_changelist_xml, get_multi_changelist_xml


def test_generate_changelist_foci_simple_():
    result = list(generate_changelist_foci(
        changelists=generate_changelists_from_xml(get_simple_changelist_xml()),
    ))
    assert len(result) == 1
    assert result[0] == """Simple:
* Update main.py"""


def test_generate_changelist_foci_simple_no_file_ext():
    result = list(generate_changelist_foci(
        generate_changelists_from_xml(get_simple_changelist_xml()),
        FormatOptions(
            no_file_ext=True,
        )
    ))
    assert result[0] == """Simple:
* Update main"""


def test_generate_changelist_foci_simple_filename():
    result = list(generate_changelist_foci(
        generate_changelists_from_xml(get_simple_changelist_xml()),
        FormatOptions(
            file_name=True,
        )
    ))
    assert result[0] == """Simple:
* Update main.py"""


def test_generate_changelist_foci_simple_filename_plus_no_file_ext():
    result = list(generate_changelist_foci(
        generate_changelists_from_xml(get_simple_changelist_xml()),
        FormatOptions(
            file_name=True,
            no_file_ext=True,
        )
    ))
    assert result[0] == """Simple:
* Update main"""


def test_generate_changelist_foci_multi_cl():
    result = list(generate_changelist_foci(
        generate_changelists_from_xml(get_multi_changelist_xml()),
    ))
    assert len(result) == 2
    assert result[0] == """Main:
* Remove history.py
* Remove main.py"""
    assert result[1] == """Test:
* Create test/test_file.py"""


def test_generate_changelist_foci_multi_cl_no_file_ext():
    result = list(generate_changelist_foci(
        generate_changelists_from_xml(get_multi_changelist_xml()),
        FormatOptions(
            no_file_ext=True,
        )
    ))
    assert len(result) == 2
    assert result[0] == """Main:
* Remove history
* Remove main"""
    assert result[1] == """Test:
* Create test/test_file"""


def test_generate_changelist_foci_multi_cl_filename_no_file_ext():
    result = list(generate_changelist_foci(
        generate_changelists_from_xml(get_multi_changelist_xml()),
        FormatOptions(
            file_name=True,
            no_file_ext=True,
        )
    ))
    assert len(result) == 2
    assert result[0] == """Main:
* Remove history
* Remove main"""
    assert result[1] == """Test:
* Create test_file"""


def test_generate_changelist_foci_multi_cl_filename():
    result = list(generate_changelist_foci(
        generate_changelists_from_xml(get_multi_changelist_xml()),
        FormatOptions(
            file_name=True,
        )
    ))
    assert len(result) == 2
    assert result[0] == """Main:
* Remove history.py
* Remove main.py"""
    assert result[1] == """Test:
* Create test_file.py"""