import argparse
from .loader import run_validator
from os import path


def main():
    parser = argparse.ArgumentParser(description='Validate GTFS fares-v2 data.')
    parser.add_argument("-s", "--read-stop-times", help="Scan stop_times for area_ids", action='store_true')
    parser.add_argument("-o", "--output-file", type=str, help="Export the errors and warnings to a file")
    parser.add_argument("input_gtfs_folder", type=str, help="Path to unzipped folder containing the Fares-v2 GTFS")

    args = parser.parse_args()

    gtfs_path = args.input_gtfs_folder
    if not path.isdir(gtfs_path):
        raise Exception('Input path is not a valid folder.')

    read_stop_times = args.read_stop_times
    results = run_validator(gtfs_path, read_stop_times)
    output = results.to_string()

    if args.output_file:
        try:
            f = open(args.output_file, 'w')
            f.write(output)
        except Exception:
            raise Exception('Writing to output file failed. Please ensure the output file path is valid.')
    else:
        print(output)





if __name__ == '__main__':
    main()
