# gtfs-fares-v2-validator

This is a tool to validate fares-v2 GTFS datasets.

This tool is based on the fares-v2 [draft specification](https://docs.google.com/document/d/19j-f-wZ5C_kYXmkLBye1g42U-kvfSVgYLkkG5oyBauY/edit#).

The tool validates ONLY fares-v2 specific files and dependent files, and does NOT validate GTFS schedule data.

The tool does NOT read areas from stop_times.txt for performance reasons, but can using the -s option defined below.

## Requirements

python 3

## Validate a fares dataset

`python3 validate.py PATH-TO-FOLDER-CONTAINING-FARES-V2-DATASET [-s, --read-stop-times] [-o, --output-file FILE-TO-EXPORT-VALIDATION-REPORT-TO]`

For example:

`python3 validate.py ~/data/my-fares-v2-dataset -o report.txt`

## Run tests

```
python3 -m pip install pytest
pytest
```
