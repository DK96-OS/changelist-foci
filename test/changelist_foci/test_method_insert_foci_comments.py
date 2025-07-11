""" Testing the Insert Foci Comments Method.
"""
import pytest
from changelist_data.storage import load_storage

from changelist_foci.format_options import FormatOptions
from changelist_foci import insert_foci_comments
from test.changelist_foci.conftest import CHANGELIST_DATA_FILE_PATH, CHANGELIST_DATA_SAMPLE_1, WORKSPACE_DATA_FILE_PATH, \
    WORKSPACE_DATA_SAMPLE_1


def test_insert_foci_comments_none_raises_exit():
    with pytest.raises(AttributeError):
        insert_foci_comments(None, FormatOptions()) 


def test_insert_foci_comments_cl_data_sample_1_default_format(temp_cwd):
    CHANGELIST_DATA_FILE_PATH.parent.mkdir(parents=True)
    CHANGELIST_DATA_FILE_PATH.touch()
    CHANGELIST_DATA_FILE_PATH.write_text(CHANGELIST_DATA_SAMPLE_1)
    cl_data_storage = load_storage()
    insert_foci_comments(cl_data_storage, FormatOptions())
    #
    result = cl_data_storage.get_changelists()
    for cl in result:
        assert len(cl.comment) > len(cl.name)


def test_insert_foci_comments_ws_data_sample_1_default_format(temp_cwd):
    WORKSPACE_DATA_FILE_PATH.parent.mkdir(parents=True)
    WORKSPACE_DATA_FILE_PATH.touch()
    WORKSPACE_DATA_FILE_PATH.write_text(WORKSPACE_DATA_SAMPLE_1)
    cl_data_storage = load_storage()
    insert_foci_comments(cl_data_storage, FormatOptions())
    #
    result = cl_data_storage.get_changelists()
    for cl in result:
        assert len(cl.comment) > len(cl.name)


def test_insert_foci_comments_cl_data_sample_1_fax_format(temp_cwd):
    CHANGELIST_DATA_FILE_PATH.parent.mkdir(parents=True)
    CHANGELIST_DATA_FILE_PATH.touch()
    CHANGELIST_DATA_FILE_PATH.write_text(CHANGELIST_DATA_SAMPLE_1)
    cl_data_storage = load_storage()
    insert_foci_comments(cl_data_storage, FormatOptions(no_file_ext=True, file_name=True))
    #
    result = cl_data_storage.get_changelists()
    for cl in result:
        assert len(cl.comment) > len(cl.name)


def test_insert_foci_comments_ws_data_sample_1_fax_format(temp_cwd):
    WORKSPACE_DATA_FILE_PATH.parent.mkdir(parents=True)
    WORKSPACE_DATA_FILE_PATH.touch()
    WORKSPACE_DATA_FILE_PATH.write_text(WORKSPACE_DATA_SAMPLE_1)
    cl_data_storage = load_storage()
    insert_foci_comments(cl_data_storage, FormatOptions(no_file_ext=True, file_name=True))
    #
    result = cl_data_storage.get_changelists()
    for cl in result:
        assert len(cl.comment) > len(cl.name)
