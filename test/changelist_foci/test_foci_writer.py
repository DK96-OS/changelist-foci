""" Testing FOCI Writer Module Methods.
"""
from changelist_data import Changelist
from changelist_data.file_change import FileChange, create_fc, update_fc, delete_fc

from changelist_foci.foci_writer import get_file_subject, generate_foci
from changelist_foci.format_options import FormatOptions
from test.changelist_foci.conftest import REL_FILE_PATH_1, REL_FILE_PATH_2, ODD_FILE_EXT, ODD_FILE_EXT2


def get_before_cd(): return delete_fc(f"/{REL_FILE_PATH_1}")
def get_after_cd(): return create_fc(f"/{REL_FILE_PATH_1}")
def get_both_cd(): return update_fc(f"/{REL_FILE_PATH_1}")

def get_move_cd():
    return FileChange(
        before_path=f'/{REL_FILE_PATH_2}',
        before_dir=False,
        after_path=f'/{REL_FILE_PATH_1}',
        after_dir=False,
    )


def test_generate_foci_0_returns_error():
    result = generate_foci(Changelist(
        id="0",
        name="",
    ))
    assert result == ":\n"


def test_generate_foci_1_returns_str(simple_cl1):
    assert generate_foci(simple_cl1) == "ChangeList:\n* Create module/file.txt"


def test_generate_foci_1_full_path_returns_str(simple_cl1):
    result = generate_foci(simple_cl1, FormatOptions(full_path=True))
    assert result == "ChangeList:\n* Create /module/file.txt"


def test_generate_foci_1_no_file_ext_returns_str(simple_cl1):
    result = generate_foci(simple_cl1, FormatOptions(no_file_ext=True))
    assert result == "ChangeList:\n* Create module/file"


def test_generate_foci_1_filename_returns_str(simple_cl1):
    result = generate_foci(simple_cl1, FormatOptions(file_name=True))
    assert result == "ChangeList:\n* Create file.txt"


def test_generate_foci_1_filename_plus_no_file_ext_returns_str(simple_cl1):
    result = generate_foci(simple_cl1, FormatOptions(file_name=True, no_file_ext=True))
    assert result == "ChangeList:\n* Create file"


def test_get_file_subject_before_returns_str():
    result = get_file_subject(get_before_cd())
    assert result == f'Remove {REL_FILE_PATH_1}'


def test_get_file_subject_after_returns_str():
    result = get_file_subject(get_after_cd())
    assert result == f'Create {REL_FILE_PATH_1}'


def test_get_file_subject_both_returns_str():
    result = get_file_subject(get_both_cd())
    assert result == f'Update {REL_FILE_PATH_1}'


def test_get_file_subject_move_returns_str():
    result = get_file_subject(get_move_cd())
    assert result == f'Move {REL_FILE_PATH_2} to {REL_FILE_PATH_1}'


def test_get_file_subject_format_no_file_ext_returns_str():
    result = get_file_subject(get_before_cd(), FormatOptions(no_file_ext=True))
    assert result == "Remove main_package/__main__"


def test_get_file_subject_remove_format_no_file_ext_returns_str():
    result = get_file_subject(get_before_cd(), FormatOptions(no_file_ext=True))
    assert result == "Remove main_package/__main__"


def test_get_file_subject_create_format_no_file_ext_returns_str():
    result = get_file_subject(get_after_cd(), FormatOptions(no_file_ext=True))
    assert result == "Create main_package/__main__"


def test_get_file_subject_update_format_no_file_ext_returns_str():
    result = get_file_subject(get_both_cd(), FormatOptions(no_file_ext=True))
    assert result == "Update main_package/__main__"


def test_get_file_subject_move_format_no_file_ext_returns_str():
    result = get_file_subject(get_move_cd(), FormatOptions(no_file_ext=True))
    assert result == "Move main_package/__init__ to main_package/__main__"


def test_get_file_subject_create_format_full_path_no_file_ext_returns_str():
    result = get_file_subject(get_after_cd(), FormatOptions(full_path=True, no_file_ext=True))
    assert result == "Create /main_package/__main__"


def test_get_file_subject_create_odd_file_ext_full_path_no_file_ext_returns_str():
    test_input = create_fc(ODD_FILE_EXT)
    result = get_file_subject(test_input, FormatOptions(full_path=True, no_file_ext=True))
    assert result == "Create /resources/img/file.png"


def test_get_file_subject_create_odd_file_ext2_full_path_no_file_ext_returns_str():
    test_input = create_fc(ODD_FILE_EXT2)
    result = get_file_subject(test_input, FormatOptions(full_path=True, no_file_ext=True))
    assert result == "Create /resources/img/file-123-8.png.jpg"


def test_get_file_subject_create_odd_file_ext_full_path_filename_no_file_ext_returns_str():
    test_input = create_fc(ODD_FILE_EXT)
    # The Following Format Options are not compatible
    f_options = FormatOptions(full_path=True, no_file_ext=True, file_name=True)
    result = get_file_subject(test_input, f_options)
    # The filename is overridden by the full_path flag
    assert result == "Create /resources/img/file.png"


def test_get_file_subject_create_odd_file_ext_filename_no_file_ext_returns_str():
    test_input = create_fc(ODD_FILE_EXT)
    # These Format Options are a likely combination
    f_options = FormatOptions(no_file_ext=True, file_name=True)
    result = get_file_subject(test_input, f_options)
    assert result == "Create file.png"


def test_get_file_subject_create_odd_file_ext2_filename_no_file_ext_returns_str():
    test_input = create_fc(ODD_FILE_EXT2)
    # These Format Options are a likely combination
    f_options = FormatOptions(no_file_ext=True, file_name=True)
    result = get_file_subject(test_input, f_options)
    assert result == "Create file-123-8.png"