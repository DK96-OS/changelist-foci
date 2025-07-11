""" Testing Argument Parser Methods.
"""
import pytest

from changelist_foci.input.argument_parser import parse_arguments


def test_parse_arguments_empty_list_returns_data():
    result = parse_arguments('')
    assert result.changelist_name is None
    assert result.workspace_path is None
    assert not result.full_path
    assert not result.no_file_ext
    assert not result.filename
    assert not result.all_changes


def test_parse_arguments_none_returns_same_as_empty_list():
    empty_list = parse_arguments([])
    assert empty_list == parse_arguments()
    assert empty_list == parse_arguments('')


def test_parse_arguments_change_list_main_returns_data():
    result = parse_arguments(['--changelist', 'Main'])
    assert result.changelist_name == 'Main'
    assert result.workspace_path is None
    assert not result.full_path
    assert not result.no_file_ext
    assert not result.filename
    assert not result.all_changes


def test_parse_arguments_invalid_changelist_name_space_raises_exit():
    with pytest.raises(SystemExit, match='The ChangeList Name was invalid.'):
        parse_arguments(['--changelist', ' '])


def test_parse_arguments_filename_plus_no_file_ext_returns_data():
    result = parse_arguments(['-fx'])
    assert result.changelist_name is None
    assert result.workspace_path is None
    assert not result.full_path
    assert result.no_file_ext
    assert result.filename
    assert not result.all_changes


def test_parse_arguments_filename_returns_data():
    result = parse_arguments(['-f'])
    assert result.changelist_name is None
    assert result.workspace_path is None
    assert not result.full_path
    assert not result.no_file_ext
    assert result.filename
    assert not result.all_changes


def test_parse_arguments_no_file_ext_returns_data():
    result = parse_arguments(['-x'])
    assert result.changelist_name is None
    assert result.workspace_path is None
    assert not result.full_path
    assert result.no_file_ext
    assert not result.filename
    assert not result.all_changes


def test_parse_arguments_full_path_returns_data():
    result = parse_arguments(['--full-path'])
    assert result.changelist_name is None
    assert result.workspace_path is None
    assert result.full_path
    assert not result.no_file_ext
    assert not result.filename
    assert not result.all_changes


def test_parse_arguments_changelist_filename_returns_data():
    result = parse_arguments(['--changelist', "Main", '-f'])
    assert result.changelist_name == 'Main'
    assert result.workspace_path is None
    assert not result.full_path
    assert not result.no_file_ext
    assert result.filename
    assert not result.all_changes


def test_parse_arguments_all_changes_returns_data():
    result = parse_arguments(['--all-changes'])
    assert result.changelist_name is None
    assert result.workspace_path is None
    assert not result.full_path
    assert not result.no_file_ext
    assert not result.filename
    assert result.all_changes


def test_parse_arguments_c_returns_data():
    result = parse_arguments(['-c'])
    assert result.changelist_name is None
    assert result.workspace_path is None
    assert not result.full_path
    assert not result.no_file_ext
    assert not result.filename
    assert not result.all_changes
    assert result.comment


def test_parse_arguments_comment_returns_data():
    result = parse_arguments(['--comment'])
    assert result.changelist_name is None
    assert result.workspace_path is None
    assert not result.full_path
    assert not result.no_file_ext
    assert not result.filename
    assert not result.all_changes
    assert result.comment


def test_parse_arguments_cfx_returns_data():
    result = parse_arguments(['-cfx'])
    assert result.changelist_name is None
    assert result.workspace_path is None
    assert not result.full_path
    assert result.no_file_ext
    assert result.filename
    assert not result.all_changes
    assert result.comment


def test_parse_arguments_acfx_returns_data():
    result = parse_arguments(['-acfx'])
    assert result.changelist_name is None
    assert result.workspace_path is None
    assert not result.full_path
    assert result.no_file_ext
    assert result.filename
    assert result.all_changes
    assert result.comment


def test_parse_arguments_all_changes_plus_filename_returns_data():
    result = parse_arguments(['-af'])
    assert result.changelist_name is None
    assert result.workspace_path is None
    assert not result.full_path
    assert not result.no_file_ext
    assert result.filename
    assert result.all_changes


def test_parse_arguments_all_changes_plus_filename_and_ext_returns_data():
    result = parse_arguments(['-fax'])
    assert result.changelist_name is None
    assert result.workspace_path is None
    assert not result.full_path
    assert result.no_file_ext
    assert result.filename
    assert result.all_changes


def test_parse_arguments_all_changes_with_changelist_name_returns_data():
    # Let the Argument Validation determine whether all changes plus changelist is a valid input or not.
    result = parse_arguments(['-a', '--changelist', 'Main'])
    assert result.changelist_name == 'Main'
    assert result.workspace_path is None
    assert not result.full_path
    assert not result.no_file_ext
    assert not result.filename
    assert result.all_changes


def test_parse_arguments_changelist_argument_missing_raises_exit():
    with pytest.raises(SystemExit):
        parse_arguments(['--changelist', '-a', 'Main'])


def test_parse_arguments_changelist_file_argument_blank_raises_exit():
    with pytest.raises(SystemExit):
        parse_arguments(['--changelists_file', ''])


def test_parse_arguments_workspace_file_argument_blank_raises_exit():
    with pytest.raises(SystemExit):
        parse_arguments(['--workspace_file', ''])
