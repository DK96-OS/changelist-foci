"""
"""
from changelist_data.xml.workspace import generate_changelists_from_xml

from changelist_foci import _filter_list
from test.changelist_foci.conftest import get_simple_changelist_xml, get_multi_changelist_xml


def test_filter_list_simple_select_active_():
    result = list(_filter_list(
        generate_changelists_from_xml(get_simple_changelist_xml()),
        False,
        None,
    ))[0]
    assert result.name == 'Simple'
    assert result.comment == 'Main Program Files'
    assert result.id == '9f60fda2-421e-4a4b-bd0f-4c8f83a47c88'
    assert len(result.changes) == 1
    change = result.changes[0]
    assert change.before_path == change.after_path
    assert change.before_dir == change.after_dir


def test_filter_list_simple_select_simple_():
    result = list(_filter_list(
        generate_changelists_from_xml(get_simple_changelist_xml()),
        False,
        changelist_name='Simple',
    ))[0]
    assert result.name == 'Simple'
    assert result.comment == 'Main Program Files'
    assert result.id == '9f60fda2-421e-4a4b-bd0f-4c8f83a47c88'
    assert len(result.changes) == 1
    change = result.changes[0]
    assert change.before_path == change.after_path
    assert change.before_dir == change.after_dir


def test_filter_list_simple_select_():
    result = list(_filter_list(
        changelists=generate_changelists_from_xml(get_simple_changelist_xml()),
        all_changes=False,
        changelist_name='Simple',
    ))[0]
    assert result.name == 'Simple'
    assert result.comment == 'Main Program Files'
    assert result.id == '9f60fda2-421e-4a4b-bd0f-4c8f83a47c88'
    assert len(result.changes) == 1
    change = result.changes[0]
    assert change.before_path == change.after_path
    assert change.before_dir == change.after_dir


def test_filter_list_multi_select_active_():
    result = list(_filter_list(
        generate_changelists_from_xml(get_multi_changelist_xml()),
        False,
        None
    ))[0]
    assert result.name == 'Main'
    assert result.comment == 'Main Program Files'
    assert result.id == 'af84ea1b-1b24-407d-970f-9f3a2835e933'
    assert len(result.changes) == 2
    change1 = result.changes[0]
    assert change1.before_path == '/history.py'
    assert not change1.before_dir
    assert change1.after_path is None
    assert change1.after_dir is None
    change2 = result.changes[1]
    assert change2.before_path == '/main.py'
    assert not change2.before_dir
    assert change1.after_path is None
    assert change1.after_dir is None