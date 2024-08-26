"""Testing ChangeData Methods.
"""
from changelist_foci.change_data import ChangeData
from changelist_foci.format_options import FormatOptions


REL_FILE_PATH_1 = 'main_package/__main__.py'
REL_FILE_PATH_2 = 'main_package/__init__.py'

ODD_FILE_EXT = '/resources/img/file.png.5'
ODD_FILE_EXT2 = '/resources/img/file-123-8.png.jpg.svg'


def get_before_cd():
    """
    """
    return ChangeData(
        before_path=f'/{REL_FILE_PATH_1}',
        before_dir=False,
    )

def get_after_cd():
    """
    """
    return ChangeData(
        after_path=f'/{REL_FILE_PATH_1}',
        after_dir=False,
    )

def get_both_cd():
    """
    """
    return ChangeData(
        before_path=f'/{REL_FILE_PATH_1}',
        before_dir=False,
        after_path=f'/{REL_FILE_PATH_1}',
        after_dir=False,
    )

def get_move_cd():
    """
    """
    return ChangeData(
        before_path=f'/{REL_FILE_PATH_2}',
        before_dir=False,
        after_path=f'/{REL_FILE_PATH_1}',
        after_dir=False,
    )


def test_get_subject_before_returns_str():
    result = get_before_cd().get_subject()
    assert result == f'Remove {REL_FILE_PATH_1}'


def test_get_subject_after_returns_str():
    result = get_after_cd().get_subject()
    assert result == f'Create {REL_FILE_PATH_1}'


def test_get_subject_both_returns_str():
    result = get_both_cd().get_subject()
    assert result == f'Update {REL_FILE_PATH_1}'


def test_get_subject_move_returns_str():
    result = get_move_cd().get_subject()
    assert result == f'Move {REL_FILE_PATH_2} to {REL_FILE_PATH_1}'


def test_get_subject_format_no_file_ext_returns_str():
    result = get_before_cd().get_subject(FormatOptions(no_file_ext=True))
    assert result == "Remove main_package/__main__"


def test_get_subject_remove_format_no_file_ext_returns_str():
    result = get_before_cd().get_subject(FormatOptions(no_file_ext=True))
    assert result == "Remove main_package/__main__"


def test_get_subject_create_format_no_file_ext_returns_str():
    result = get_after_cd().get_subject(FormatOptions(no_file_ext=True))
    assert result == "Create main_package/__main__"


def test_get_subject_update_format_no_file_ext_returns_str():
    result = get_both_cd().get_subject(FormatOptions(no_file_ext=True))
    assert result == "Update main_package/__main__"


def test_get_subject_move_format_no_file_ext_returns_str():
    result = get_move_cd().get_subject(FormatOptions(no_file_ext=True))
    assert result == "Move main_package/__init__ to main_package/__main__"


def test_get_subject_create_format_full_path_no_file_ext_returns_str():
    result = get_after_cd().get_subject(FormatOptions(full_path=True, no_file_ext=True))
    assert result == "Create /main_package/__main__"


def test_get_subject_create_odd_file_ext_full_path_no_file_ext_returns_str():
    test_input = ChangeData(
        after_path=ODD_FILE_EXT,
        after_dir=False,
    )
    result = test_input.get_subject(FormatOptions(full_path=True, no_file_ext=True))
    assert result == "Create /resources/img/file.png"


def test_get_subject_create_odd_file_ext2_full_path_no_file_ext_returns_str():
    test_input = ChangeData(
        after_path=ODD_FILE_EXT2,
        after_dir=False,
    )
    result = test_input.get_subject(FormatOptions(full_path=True, no_file_ext=True))
    assert result == "Create /resources/img/file-123-8.png.jpg"


def test_get_subject_create_odd_file_ext_full_path_filename_no_file_ext_returns_str():
    test_input = ChangeData(
        after_path=ODD_FILE_EXT,
        after_dir=False,
    )
    # The Following Format Options are not compatible
    f_options = FormatOptions(full_path=True, no_file_ext=True, file_name=True)
    result = test_input.get_subject(f_options)
    # The filename is overridden by the full_path flag
    assert result == "Create /resources/img/file.png"


def test_get_subject_create_odd_file_ext_filename_no_file_ext_returns_str():
    test_input = ChangeData(
        after_path=ODD_FILE_EXT,
        after_dir=False,
    )
    # These Format Options are a likely combination
    f_options = FormatOptions(no_file_ext=True, file_name=True)
    result = test_input.get_subject(f_options)
    assert result == "Create file.png"
