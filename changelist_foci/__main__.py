#!/usr/bin/python


def main():
    from sys import argv
    import changelist_foci
    input_data = changelist_foci.input.validate_input(argv[1:])
    if not input_data.changelist_data_storage:
        output_data = changelist_foci.get_changelist_foci(input_data)
        print(output_data)
    else:
        changelist_foci.insert_foci_comments(
            input_data.changelist_data_storage,
            input_data.format_options
        )
        input_data.changelist_data_storage.write_to_storage()


if __name__ == "__main__":
    from pathlib import Path
    from sys import path
    # Get the directory of the current file (__file__ is the path to the script being executed)
    current_directory = Path(__file__).resolve().parent.parent
    path.append(str(current_directory)) # Add the directory to sys.path
    main()