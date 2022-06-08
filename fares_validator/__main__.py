import argparse
from os import path

from .loader import run_validator


def main():
    parser = argparse.ArgumentParser(description='Validate GTFS fares-v2 data.')
    parser.add_argument("-o",
                        "--output-file",
                        type=str,
                        help="Export the errors and warnings to a file")
    parser.add_argument(
        "input_gtfs_folder",
        type=str,
        help="Path to unzipped folder containing the Fares-v2 GTFS")
    parser.add_argument("-e",
                        "--experimental",
                        action="store_true",
                        help="Validate unofficial experimental files and fields")

    args = parser.parse_args()

    gtfs_path = args.input_gtfs_folder
    if not path.isdir(gtfs_path):
        raise Exception('Input path is not a valid folder.')

    results = run_validator(gtfs_path, args.experimental)
    output = results.to_string()

    if args.output_file:
        try:
            f = open(args.output_file, 'w')
            f.write(output)
        except Exception:
            raise Exception(
                'Writing to output file failed. Please ensure the output file path is valid.'
            )
    else:
        print(output)


if __name__ == '__main__':
    main()
