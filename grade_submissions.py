#!/usr/bin/env python3

# Basic program to unzip a file of submission and walk each

import argparse
import os
import shutil
import subprocess
import sys

import grading_worksheet as gw

TEMPDIR = './tmp'
ERROR_GRADE = '0.00'

def _main(argv=None):
    """
    Map grading script across submissions, populating grading worksheet

    """

    argv = argv or sys.argv[1:]

    # Setup Argument Parsing
    parser = argparse.ArgumentParser(description='Grade Moodle Submissions')
    parser.add_argument('output_worksheet', type=str,
                       help='Output Grading Worksheet CSV File')
    parser.add_argument('input_worksheet', type=str,
                       help='Input Grading Worksheet CSV File')
    parser.add_argument('submissions', type=str,
                       help='Zip file of all submissions')
    parser.add_argument('grading_script', type=str,
                       help='Submssion grading script')

    # Parse Arguments
    args = parser.parse_args(argv)
    output_worksheet = args.output_worksheet
    input_worksheet = args.input_worksheet
    submissions = args.submissions
    grading_script = args.grading_script

    # Read Input
    grades, dialect, fields = gw.read_worksheet(input_worksheet)

    subprocess.check_call(['unzip', '-d', TEMPDIR, submissions])

    for root, subdirs, subfiles in os.walk(TEMPDIR):

        origwd = os.getcwd()
        script_path = origwd + "/" + grading_script
        print("Entering {!s}".format(root))
        os.chdir(root)

        for subfile in subfiles:

            subfile_split_dot = subfile.split('.')
            subfile_split_under = subfile.split('_')
            if (subfile_split_dot[-1] == 'zip'):
                print("Processing submission {!s}".format(subfile))
                student = subfile_split_under[0]
                print("Submission by {!s}".format(student))
                procdir = ''.join(subfile_split_dot[:-1])
                subprocess.check_call(['unzip', '-d', procdir, subfile])
                cwd = os.getcwd()
                print("Entering {!s}".format(procdir))
                os.chdir(procdir)
                print("Running {!s}".format(script_path))
                try:
                    output = subprocess.check_output([script_path])
                    output_str = output.decode()
                    output_str_clean = output_str.rstrip().lstrip()
                    print("Grade = {!s}".format(output_str_clean))
                    grades[student]['Grade'] = output_str_clean
                except subprocess.CalledProcessError as err:
                    print("Error grading submission: {!s}".format(err), file=sys.stderr)
                    grades[student]['Grade'] = ERROR_GRADE
                print("Returning to {!s}".format(cwd))
                os.chdir(cwd)
                print("Removing {!s}".format(procdir))
                shutil.rmtree(procdir)

        print("Returning to {!s}".format(origwd))
        os.chdir(origwd)

    print("Removing {!s}".format(TEMPDIR))
    shutil.rmtree(TEMPDIR)

    # Write Output
    gw.write_worksheet(output_worksheet, grades, dialect, fields)


if __name__ == "__main__":
    sys.exit(_main())
