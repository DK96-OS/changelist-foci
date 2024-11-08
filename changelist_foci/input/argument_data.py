"""The Arguments Received from the Command Line Input.

This DataClass is created after the argument syntax is validated.

Syntax Validation:
- The changelist name, if exists is checked for valid characters.
- The workspace path, if exists is currently unvalidated.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class ArgumentData:
    """
    The syntactically valid arguments received by the Program.

    Fields:
    - changelist_name (str | None): The name of the changelist, or None to use the Active Changelist.
    - changelists_path (str | None): The path to the Changelists data xml file, or none to check default paths.
    - workspace_path (str | None): The path to the Workspace xml file, or none to check default paths.
    - full_path (bool): Display the Full File Path.
    - no_file_ext (bool): Remove the File Extension.
    - filename (bool): Remove the Parent Directories.
    - all_changes (bool): Format and Print all Changes from all Changelists.
    """
    changelist_name: str | None = None
    changelists_path: str | None = None
    workspace_path: str | None = None
    full_path: bool = False
    no_file_ext: bool = False
    filename: bool = False
    all_changes: bool = False
