"""Testing Changelist Foci Module Initialization Methods.
"""
import pytest
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
    with pytest.raises(SystemExit, match='Specified Changelist test not present.'):
        get_changelist_foci(test_input)


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


def test_get_changelist_foci_multi_changelist_name_not_present_raises_exit():
    test_input = InputData(
        changelists=read_xml(get_multi_changelist_xml()),
        changelist_name='Missing Name',
    )
    with pytest.raises(SystemExit, match='Specified Changelist Missing Name not present.'):
        get_changelist_foci(test_input)