""" CL-FOCI Package Methods.
"""
from typing import Generator, Iterable

from changelist_data.changelist import Changelist, get_default_cl

from changelist_foci.foci_writer import generate_foci
from changelist_foci.format_options import FormatOptions
from changelist_foci.input.input_data import InputData


def get_changelist_foci(
    input_data: InputData,
) -> str:
    """ Processes InputData, returning the FOCI.

**Parameters:**
 - input_data (InputData): The program input data.

**Returns:**
 str - The FOCI formatted output.
    """
    return '\n\n'.join(
        generate_changelist_foci(
            input_data.changelists,
            input_data.format_options,
            input_data.all_changes,
            input_data.changelist_name,
        )
    )


def generate_changelist_foci(
    changelists: Iterable[Changelist],
    foci_format: FormatOptions,
    all_changelists: bool = True,
    changelist_name: str | None = None,
) -> Generator[str, None, None]:
    """ Generate String Blocks of FOCI.
- By default, all_changelists argument is True.
- Changelist_name is matched at the start of the string.
- If no changelist_name, tries the Default, then the first Changelist.

**Parameters:**
 - changelists (Iterable[Changelist]): The source collection of Changelists to filter and generate from.
 - foci_format (FormatOptions): The flags describing the details of the output format.
 - all_changelists (bool): Whether to generate the FOCI for all Changelists. Default: True.
 - changelist_name (str): The name of the Changelist to Generate FOCI for. Default: None.

**Yields:**
 str - Blocks of FOCI formatted text.
    """
    for cl in _filter_list(
        changelists, all_changelists, changelist_name
    ): yield generate_foci(cl, foci_format)


def _filter_list(
    changelists: Iterable[Changelist],
    all_changes: bool,
    changelist_name: str | None,
) -> Generator[Changelist, None, None]:
    """ Filter the Changelists based on InputData, to determine which changes to output.
    """
    if all_changes:
        yield from filter(lambda x: len(x.changes) > 0, changelists)
    elif changelist_name not in ["None", None]:
        yield from filter(lambda x: x.name.startswith(changelist_name), changelists)
    else:
        yield get_default_cl(changelists)
    return None