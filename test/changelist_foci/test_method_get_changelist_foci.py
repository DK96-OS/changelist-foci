"""Testing Changelist Foci Module Initialization Methods.
"""
from changelist_data.xml.workspace import read_xml

from changelist_foci import get_changelist_foci
from changelist_foci.input.input_data import InputData
from test.changelist_foci.conftest import get_simple_changelist_xml, get_multi_changelist_xml


def test_get_changelist_foci_simple_changelist():
    test_input = InputData(
        changelists=read_xml(get_simple_changelist_xml()),
        changelist_name=None,
    )
    result = get_changelist_foci(test_input)
    assert result.count('\n') == 1


def test_get_changelist_foci_multi_changelist():
    test_input = InputData(
        changelists=read_xml(get_multi_changelist_xml()),
        changelist_name=None,
    )
    result = get_changelist_foci(test_input)
    assert result.count('\n') == 2


def test_get_changelist_foci_multi_changelist_test_cl():
    test_input = InputData(
        changelists=read_xml(get_multi_changelist_xml()),
        changelist_name='Test',
    )
    result = get_changelist_foci(test_input)
    assert result.count('\n') == 1


def test_get_changelist_foci_multi_changelist_test_cl_lowercase_returns_empty_str():
    test_input = InputData(
        changelists=read_xml(get_multi_changelist_xml()),
        changelist_name='test',
    )
    result = get_changelist_foci(test_input)
    assert result == ''


def test_get_changelist_foci_multi_changelist_all_changes():
    test_input = InputData(
        changelists=read_xml(get_multi_changelist_xml()),
        all_changes=True,
    )
    result = get_changelist_foci(test_input)
    assert result.count('\n') == 5
    # Check that FOCI Titles are present
    assert "Main:" in result
    assert "Test:" in result
    # Check that FOCI Subjects are present
    assert "* Remove history.py" in result
    assert "* Remove main.py" in result
    assert "* Create test/test_file.py" in result


def test_get_changelist_foci_multi_changelist_name_not_present():
    test_input = InputData(
        changelists=read_xml(get_multi_changelist_xml()),
        changelist_name='Missing Name',
    )
    try:
        get_changelist_foci(test_input)
        raised_exit = False
    except SystemExit:
        raised_exit = True
    assert raised_exit