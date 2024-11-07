""" Data Provider for Test Cases
"""
from changelist_data import Changelist
from changelist_data.file_change import FileChange


REL_FILE_PATH_1 = 'main_package/__main__.py'
REL_FILE_PATH_2 = 'main_package/__init__.py'

ODD_FILE_EXT = '/resources/img/file.png.5'
ODD_FILE_EXT2 = '/resources/img/file-123-8.png.jpg.svg'


def get_before_cd():
    """
    """
    return FileChange(
        before_path=f'/{REL_FILE_PATH_1}',
        before_dir=False,
    )

def get_after_cd():
    """
    """
    return FileChange(
        after_path=f'/{REL_FILE_PATH_1}',
        after_dir=False,
    )

def get_both_cd():
    """
    """
    return FileChange(
        before_path=f'/{REL_FILE_PATH_1}',
        before_dir=False,
        after_path=f'/{REL_FILE_PATH_1}',
        after_dir=False,
    )

def get_move_cd():
    """
    """
    return FileChange(
        before_path=f'/{REL_FILE_PATH_2}',
        before_dir=False,
        after_path=f'/{REL_FILE_PATH_1}',
        after_dir=False,
    )


def new_cd(after_path: str) -> FileChange:
    return FileChange(
        after_path=after_path,
        after_dir=False,
    )


def get_cl0():
    return Changelist(
        id="0",
        name="",
        changes=list(),
    )

def get_cl1():
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

