""" Testing Input Init Module ValidateInput Method..
"""
from pathlib import Path
from unittest.mock import Mock

import pytest

from changelist_foci.format_options import FormatOptions, DEFAULT_FORMAT_OPTIONS
from changelist_foci.input import validate_input
from test.changelist_foci.conftest import get_simple_changelist_xml, FileOutputCollector, get_simple_changelist_data_xml


def test_validate_input_empty_args_returns_data():
    test_input = []
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda x: x.name == 'workspace.xml')
        c.setattr(Path, 'is_file', lambda _: True)
        obj = Mock()
        obj.__dict__["st_size"] = 4 * 1024
        c.setattr(Path, 'stat', lambda _: obj)
        c.setattr(Path, 'read_text', lambda _: get_simple_changelist_xml())
        #
        result = validate_input(test_input)
        assert not result.all_changes
        assert result.changelist_name is None
        assert len(list(result.changelists)) == 1
        assert result.format_options == FormatOptions(
            False, False, False
        )


def test_validate_input_all_changes_returns_data():
    test_input = ['-a']
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda x: x.name == 'workspace.xml')
        c.setattr(Path, 'is_file', lambda _: True)
        obj = Mock()
        obj.__dict__["st_size"] = 4 * 1024
        c.setattr(Path, 'stat', lambda _: obj)
        c.setattr(Path, 'read_text', lambda _: get_simple_changelist_xml())
        #
        result = validate_input(test_input)
        assert result.all_changes
        assert result.changelist_name is None
        assert len(list(result.changelists)) == 1
        assert result.format_options == FormatOptions(
            False, False, False
        )


def test_validate_input_full_path_returns_data():
    test_input = ['--full-path']
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda x: x.name == 'workspace.xml')
        c.setattr(Path, 'is_file', lambda _: True)
        obj = Mock()
        obj.__dict__["st_size"] = 4 * 1024
        c.setattr(Path, 'stat', lambda _: obj)
        c.setattr(Path, 'read_text', lambda _: get_simple_changelist_xml())
        #
        result = validate_input(test_input)
        assert not result.all_changes
        assert result.changelist_name is None
        assert len(list(result.changelists)) == 1
        assert result.format_options == FormatOptions(
            True, False, False
        )


def test_validate_input_comment_with_workspace_xml_returns_data():
    test_input = ['-c']
    output_collector = FileOutputCollector()
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda x: x.name == 'workspace.xml')
        c.setattr(Path, 'is_file', lambda _: True)
        obj = Mock()
        obj.__dict__["st_size"] = 4 * 1024
        c.setattr(Path, 'stat', lambda _: obj)
        c.setattr(Path, 'read_text', lambda _: get_simple_changelist_xml())
        c.setattr(Path, 'write_text', output_collector.get_mock_write_text())
        #
        result = validate_input(test_input)
        assert not result.all_changes
        assert result.changelist_name is None
        assert len(list(result.changelists)) == 1
        assert result.format_options == FormatOptions(
            False, False, False
        )
        assert result.changelist_data_storage


def test_validate_input_cfx_with_changelist_xml_returns_data():
    test_input = ['-cfx']
    output_collector = FileOutputCollector()
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda x: x.name == 'data.xml')
        c.setattr(Path, 'is_file', lambda _: True)
        obj = Mock()
        obj.__dict__["st_size"] = 4 * 1024
        c.setattr(Path, 'stat', lambda _: obj)
        c.setattr(Path, 'read_text', lambda _: get_simple_changelist_data_xml())
        c.setattr(Path, 'write_text', output_collector.get_mock_write_text())
        #
        result = validate_input(test_input)
        assert not result.all_changes
        assert result.changelist_name is None
        assert len(list(result.changelists)) == 1
        assert result.format_options == FormatOptions(False, True, True)
        assert result.changelist_data_storage


def test_validate_input_filename_only_returns_data():
    test_input = ['-fx']
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda x: x.name == 'workspace.xml')
        c.setattr(Path, 'is_file', lambda _: True)
        obj = Mock()
        obj.__dict__["st_size"] = 4 * 1024
        c.setattr(Path, 'stat', lambda _: obj)
        c.setattr(Path, 'read_text', lambda _: get_simple_changelist_xml())
        #
        result = validate_input(test_input)
        assert not result.all_changes
        assert result.changelist_name is None
        assert len(list(result.changelists)) == 1
        assert result.format_options == FormatOptions(
            False, True, True
        )
        assert not result.changelist_data_storage


def test_validate_input_file_does_not_exist_raises_exit():
    test_input = []
    with (pytest.MonkeyPatch().context() as ctx):
        ctx.setattr(Path, 'exists', lambda _: False)
        result = validate_input(test_input)
        assert result.changelist_name is None
        assert len(list(result.changelists)) == 0
        assert result.format_options == DEFAULT_FORMAT_OPTIONS
        assert not result.changelist_data_storage


def test_validate_input_both_changelist_and_workspace_args_provided_raises_exit():
    with pytest.raises(SystemExit, match="Cannot use two Data Files!"):
        result = validate_input([
            '--changelists_file', 'data.xml', '--workspace_file', 'workspace.xml'
        ])
        list(result.changelists) # Runs Generator


def test_validate_input_workspace_file_provided():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda x: x.name == 'workspace.xml')
        c.setattr(Path, 'is_file', lambda _: True)
        obj = Mock()
        obj.__dict__["st_size"] = 4 * 1024
        c.setattr(Path, 'stat', lambda _: obj)
        c.setattr(Path, 'read_text', lambda _: get_simple_changelist_xml())
        #
        result = validate_input([
            '--workspace_file', 'workspace.xml'
        ])
        assert result.changelist_name is None
        assert 1 == len(list(result.changelists))
        assert result.format_options == DEFAULT_FORMAT_OPTIONS
        assert not result.changelist_data_storage


def test_validate_input_changelist_file_valid_no_changelists(empty_changelists_xml):
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda x: x.name == 'data.xml')
        c.setattr(Path, 'is_file', lambda _: True)
        obj = Mock()
        obj.__dict__["st_size"] = 4 * 1024
        c.setattr(Path, 'stat', lambda _: obj)
        c.setattr(Path, 'read_text', lambda _: empty_changelists_xml)
        #
        result = validate_input(['--changelists_file', 'data.xml'])
        assert result.changelist_name is None
        assert len(list(result.changelists)) == 0
        assert result.format_options == DEFAULT_FORMAT_OPTIONS
        assert not result.changelist_data_storage


def test_validate_input_changelist_file_simple(simple_changelists_xml):
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda x: x.name == 'data.xml')
        c.setattr(Path, 'is_file', lambda _: True)
        obj = Mock()
        obj.__dict__["st_size"] = 4 * 1024
        c.setattr(Path, 'stat', lambda _: obj)
        c.setattr(Path, 'read_text', lambda _: simple_changelists_xml)
        #
        result = validate_input(['--changelists_file', 'data.xml'])
        assert result.changelist_name is None
        assert len(list(result.changelists)) == 1
        assert result.format_options == DEFAULT_FORMAT_OPTIONS
        assert not result.changelist_data_storage


def test_validate_input_changelist_file_multi(multi_changelists_xml):
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda x: x.name == 'data.xml')
        c.setattr(Path, 'is_file', lambda _: True)
        obj = Mock()
        obj.__dict__["st_size"] = 4 * 1024
        c.setattr(Path, 'stat', lambda _: obj)
        c.setattr(Path, 'read_text', lambda _: multi_changelists_xml)
        #
        result = validate_input(['--changelists_file', 'data.xml'])
        assert result.changelist_name is None
        assert len(list(result.changelists)) == 2
        assert result.format_options == DEFAULT_FORMAT_OPTIONS
        assert not result.changelist_data_storage


def test_validate_input_changelist_file_multi_name_argument(multi_changelists_xml):
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda x: x.name == 'data.xml')
        c.setattr(Path, 'is_file', lambda _: True)
        obj = Mock()
        obj.__dict__["st_size"] = 4 * 1024
        c.setattr(Path, 'stat', lambda _: obj)
        c.setattr(Path, 'read_text', lambda _: multi_changelists_xml)
        #
        result = validate_input(['--changelists_file', 'data.xml', '--changelist', 'Main'])
        assert result.changelist_name == 'Main'
        assert len(list(result.changelists)) == 2
        assert result.format_options == DEFAULT_FORMAT_OPTIONS
        assert not result.changelist_data_storage


def test_validate_input_changelist_file_invalid(invalid_changelists_xml):
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda x: x.name == 'data.xml')
        c.setattr(Path, 'is_file', lambda _: True)
        obj = Mock()
        obj.__dict__["st_size"] = 4 * 1024
        c.setattr(Path, 'stat', lambda _: obj)
        c.setattr(Path, 'read_text', lambda _: invalid_changelists_xml)
        #
        result = validate_input(['--changelists_file', 'data.xml'])
        assert result.changelist_name is None
        assert len(list(result.changelists)) == 0
        assert result.format_options == DEFAULT_FORMAT_OPTIONS
        assert not result.changelist_data_storage