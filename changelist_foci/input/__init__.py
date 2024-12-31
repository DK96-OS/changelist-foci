"""The Input Package level methods.
"""
from pathlib import Path
from sys import exit

from changelist_data.changelist import Changelist
from changelist_data.storage import read_storage
from changelist_data.storage.storage_type import StorageType

from changelist_foci.format_options import FormatOptions
from changelist_foci.input.argument_data import ArgumentData
from changelist_foci.input.argument_parser import parse_arguments
from changelist_foci.input.input_data import InputData
from changelist_foci.input.string_validation import validate_name


def validate_input(
    arguments: list[str],
) -> InputData:
    """ Given the Command Line Arguments, obtain the InputData.
        1. Parse arguments with argument parser
        2. Check File Arguments, read Storage
        3. Return Structured Input Data

    Parameters:
    - arguments (list[str]): The Command Line Arguments received by the program.
    
    Returns:
    InputData - The formatted InputData.
    """
    arg_data = parse_arguments(arguments)
    return InputData(
        changelists=_read_storage_file(arg_data.changelists_path, arg_data.workspace_path),
        changelist_name=arg_data.changelist_name,
        format_options=_extract_format_options(arg_data),
        all_changes=arg_data.all_changes,
    )


def _read_storage_file(
    changelists_file: str | None,
    workspace_file: str | None,
) -> list[Changelist]:
    """ Process the Given File Arguments, and read from Storage.
    Storage is managed by changelist_data package.

    Parameters:
    - changelists_file (str | None): A string path to the Changelists file, if specified.
    - workspace_file (str | None): A string path to the Workspace file, if specified.

    Returns:
    list[Changelist] - The Changelist data from the storage file.
    """
    if isinstance(changelists_file, str) and isinstance(workspace_file, str):
        exit("Cannot use two Data Files!")
    if validate_name(changelists_file):
        return read_storage(StorageType.CHANGELISTS, Path(changelists_file))
    if validate_name(workspace_file):
        return read_storage(StorageType.WORKSPACE, Path(workspace_file))
    return read_storage()


def _extract_format_options(
    data: ArgumentData,
) -> FormatOptions:
    # Map Property names
    return FormatOptions(
        full_path=data.full_path,
        no_file_ext=data.no_file_ext,
        file_name=data.filename,
    )
