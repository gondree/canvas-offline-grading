#!/usr/bin/env python3

# Basic program to read csv file and spit it back out

import argparse
import csv
import sys


def read_worksheet(csv_file):
    """
    Read contents of worksheet_csv and return (contents, dialect, fields)

    """

    contents = {}
    dialect = None
    fields = None

    with open(csv_file, 'r', newline='') as worksheet:

        dialect = csv.Sniffer().sniff(worksheet.read())
        worksheet.seek(0)
        header = csv.Sniffer().has_header(worksheet.read())
        worksheet.seek(0)
        reader = csv.DictReader(worksheet, dialect=dialect)
        fields = reader.fieldnames

        for row in reader:
            contents[row['Full name']] = row

    return (contents, dialect, fields)


def write_worksheet(csv_file, contents, dialect, fields):
    """
    Write contents to worksheet_csv using dialect and fields

    """

    with open(csv_file, 'w', newline='') as worksheet:

        writer = csv.DictWriter(worksheet, fields, dialect=dialect)
        writer.writeheader()
        for val in contents.values():
            writer.writerow(val)

    return None


def _main(argv=None):
    """
    Module Grading Worksheet Module Unit Tests

    """

    argv = argv or sys.argv[1:]

    # Setup Argument Parsing
    parser = argparse.ArgumentParser(description='Test Process Moodle Grading Worksheet')
    parser.add_argument('input_csv', type=str,
                       help='Input Grading Worksheet CSV File')
    parser.add_argument('output_csv', type=str,
                       help='Output Grading Worksheet CSV File')

    # Parse Arguments
    args = parser.parse_args(argv)
    input_csv = args.input_csv
    output_csv = args.output_csv

    # Read Input
    contents, dialect, fields = read_worksheet(input_csv)

    # Mutate Contents
    for val in contents.values():
        val['Grade'] = '99.9'

    # Write Output
    write_worksheet(output_csv, contents, dialect, fields)

if __name__ == "__main__":
    sys.exit(_main())
