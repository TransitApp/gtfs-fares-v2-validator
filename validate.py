import argparse
from run_validator import run_validator
from os import path

def print_results(errors, warnings):
    output = ''
    if len(errors) > 0:
        output += 'ERRORS:\n'

        for error in errors:
            output += '\n' + error + '\n'
    else:
        output += 'No errors detected.\n'

    if len(warnings) > 0:
        output += '\n\nWARNINGS:\n'

        for warning in warnings:
            output += '\n' + warning + '\n'
    else:
        output += 'No warnings to report.'

    return output

parser = argparse.ArgumentParser(description='Validate GTFS fares-v2 data.')
parser.add_argument("-s", "--read-stop-times", help="scans stop_times for area_ids", action='store_true')
parser.add_argument("-o", "--output-file", type=str, help="export the errors and warnings to a file")
parser.add_argument("input_gtfs_folder", type=str, help="path to unzipped folder containing fares-v2 GTFS")

args = parser.parse_args()

gtfs_path = args.input_gtfs_folder
if not path.isdir(gtfs_path):
    raise Exception('Input path is not a valid folder.')

read_stop_times = False
if args.read_stop_times:
    read_stop_times = True

results = run_validator(gtfs_path, read_stop_times)
output = print_results(results['errors'], results['warnings'])

if args.output_file:
    try:
        f = open(args.output_file, 'w')
        f.write(output)
    except Exception:
        raise Exception('Writing to output file failed. Please ensure the output file path is valid.')
else:
    print(output)
