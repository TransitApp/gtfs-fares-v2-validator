# gtfs-fares-v2-validator

This is a tool to validate fares-v2 GTFS datasets.

Validates ONLY fares-v2 specific files and dependent files, and does NOT validate GTFS schedule data.

Provides validation towards two versions of the fares-v2 specifications:
  1. \[Default\] fares-v2 files in the official GTFS [specification](https://github.com/google/transit/blob/master/gtfs/spec/en/reference.md)
  2. \[Through `-e` flag\] the official specification above, as well as additional fields ("experimental" fields) defined in the GTFS fares-v2 draft document, with some [exceptions](#unsupported-experimental-fields-and-files-subject-to-change). Also includes some [fields](#additional-experimental-fields) used internally at Transit, and which are either current or upcoming proposals to the official specification.

Running the tool with the -e flag provides validation for experimental features, and notices pertaining to experimental features are clearly marked as such.

## Requirements

python 3

## Validate a fares dataset

`python3 validate.py PATH-TO-FOLDER-CONTAINING-FARES-V2-DATASET [-o, --output-file FILE-TO-EXPORT-VALIDATION-REPORT-TO] [-e, --experimental]`

For example:

`python3 validate.py ~/data/my-fares-v2-dataset -o report.txt`

## Run tests

```
python3 -m pip install pytest
pytest
```

## Unsupported experimental fields and files (subject to change)

- `fare_capping.txt`: unsupported file. All `fare_capping` references in other files are also unsupported.
- `fare_products.txt`: `service_id`, all `timeframe` fields
- `fare_leg_rules.txt`: `contains_area_id`, all `amount` fields, `currency`
- `fare_transfer_rules.txt`: all `amount` fields, `currency`, `transfer_id`, `transfer_sequence`

## Additional experimental fields

- `fare_leg_rules.txt`
  - `transfer_only`: specifies that a fare leg rule may only be used at the back-end of a transfer
- `fare_transfer_rules.txt`
  - `filter_fare_product_id`: a fare product necessary to have in order for a transfer to be valid. Does not encode the `cost` of a transfer, as `fare_product_id` does.