""" Package Methods.
"""
from changelist_data import Changelist, storage

from .foci_writer import generate_foci
from .input.input_data import InputData


def get_changelist_foci(
    input_data: InputData,
) -> str:
    """
    Processes InputData, returning the FOCI.

    Parameters:
    - input_data (InputData): The program input data.

    Returns:
    str - The FOCI formatted output.
    """
    cl_list = _get_changelists(input_data)
    return '\n\n'.join(
        generate_foci(cl, input_data.format_options)
        for cl in _filter_list(input_data, cl_list)
    )


def _get_changelists(input_data: InputData) -> list[Changelist]:
    """
    Obtain all Changelists in a list.
    - Uses the XML string provided by InputData.
    - Applies workspace_reader module.
    """
    if input_data.workspace_xml is not None:
        return storage.workspace.read_xml(input_data.workspace_xml)
    # todo: Update InputData for more data storage options
    #


def _filter_list(
    input_data: InputData,
    cl_list: list[Changelist]
) -> list[Changelist]:
    """
    Filter the Changelists based on InputData, to determine which changes to output.
    """
    if input_data.all_changes:
        return list(
            filter(lambda x: len(x.changes) > 0, cl_list)
        )
    if input_data.changelist_name not in ["None", None]:
        return _get_changelist_by_name(
            cl_list,
            input_data.changelist_name,
        )
    return _get_active_changelist(cl_list)


def _get_active_changelist(
    cl_list: list[Changelist],
) -> list[Changelist]:
    """
    Find the Active Changelist, or the only changelist.
    """
    if len(cl_list) == 1:
        return [cl_list[0]]
    return list(filter(lambda x: x.is_default, cl_list))


def _get_changelist_by_name(
    cl_list: list[Changelist],
    changelist_name: str,
) -> list[Changelist]:
    """
    Find a Changelist that starts with the given name.
    """
    cl = list(filter(lambda x: x.name.startswith(changelist_name), cl_list))
    if len(cl) == 0:
        exit(f"Specified Changelist {changelist_name} not present.")
    return cl
