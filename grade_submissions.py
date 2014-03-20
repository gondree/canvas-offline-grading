#!/usr/bin/env python3

# Basic program to unzip a file of submission and walk each

import argparse
import os
import shutil
import subprocess
import sys
import math

import moodle_grading_worksheet as gw
import moodle_submissions as ms

TEMPDIR = './tmp'
_FRAMEWORK_LOG_PATH = './framework.log'
_GRADER_LOG_PATH = './grader.log'
_ERROR_GRADE = '0.00'

_ZERO_CREDIT = 0
_FULL_CREDIT = 100

_EXIT_ERROR = -1
_EXIT_SUCCESS = 0

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
    parser.add_argument('--target_name', type=str, dest='target_name',
                       help='Target name for single file submission')
    parser.add_argument('--extra_files', type=str, dest='extra_files',
                       help='Extra files to be copied into working directory')

    # Parse Arguments
    args = parser.parse_args(argv)
    output_worksheet = args.output_worksheet
    input_worksheet = args.input_worksheet
    submissions = args.submissions
    grading_script = args.grading_script
    target_name = args.target_name
    extra_files = args.extra_files

    # Read Input
    grades, dialect, fields = gw.read_worksheet(input_worksheet)

    # Setup Logs
    framelog = open(_FRAMEWORK_LOG_PATH, mode='w+t')
    gradelog = open(_GRADER_LOG_PATH, mode='w+t')

    # Setup Stats
    found = 0
    unzipped = 0
    moved = 0
    scored = 0
    recorded = 0
    zeros = 0
    fulls = 0
    nerrors = 0
    ferrors = 0
    gerrors = 0

    try:
        subprocess.check_call(['unzip', '-d', TEMPDIR, submissions], stdout=framelog)
    except subprocess.CalledProcessError as err:
        print("ERROR: Could not extract {}: {}".format(submissions, err), file=sys.stderr)
        return _EXIT_ERROR
    try:
        for root, subdirs, subfiles in os.walk(TEMPDIR):

            origwd = os.getcwd()
            script_path = origwd + "/" + grading_script
            print("Entering {}".format(root))
            os.chdir(root)

            # Walk submitted file tree
            try:
                for subfile in subfiles:

                    found += 1

                    # Parse File Name
                    submission = ms.Submission(subfile)
                    print("Processing submission {}".format(subfile))
                    print("Processing submission {}".format(subfile), file=gradelog)
                    student = submission.submitter_name
                    print("Submission by {}".format(student))
                    print("Submission by {}".format(student), file=gradelog)
                    procdir = submission.submitter_id

                    # Extract or Copy Submission
                    if (submission.file_type == 'zip'):
                        # Zip File Submission
                        try:
                            subprocess.check_call(['unzip', '-d', procdir, subfile], stdout=framelog)
                        except subprocess.CalledProcessError as err:
                            print("ERROR: Could not extract {}: {}. ".format(subfile, err) +
                                  "Check the {} log".format(_FRAMEWORK_LOG_PATH), file=sys.stderr)
                            ferrors += 1
                            continue
                        else:
                            unzipped += 1
                    else:
                        # Single File Submission
                        if target_name:
                            file_out = target_name
                        else:
                            file_out = submission.file_name
                        try:
                            subprocess.check_call(['mkdir', procdir], stdout=framelog)
                            subprocess.check_call(['cp', subfile, '{}/{}'.format(procdir, file_out)],
                                                  stdout=framelog)
                        except subprocess.CalledProcessError as err:
                            print("ERROR: Could not copy {}: {}. ".format(subfile, err) +
                                  "Check the {} log".format(_FRAMEWORK_LOG_PATH), file=sys.stderr)
                            ferrors += 1
                            continue
                        else:
                            moved += 1

                    # Extract or Copy Extra Files
                    if extra_files:
                        extra_files_path = origwd + "/" + extra_files
                        extra_files_base, extra_files_ext = os.path.splitext(extra_files_path)
                        if (extra_files_ext == 'zip'):
                            # Zip File Extras
                            try:
                                subprocess.check_call(['unzip', '-d', procdir, extra_files_path], stdout=framelog)
                            except subprocess.CalledProcessError as err:
                                print("ERROR: Could not extract {}: {}. ".format(extra_files_path, err) +
                                      "Check the {} log".format(_FRAMEWORK_LOG_PATH), file=sys.stderr)
                                ferrors += 1
                                raise
                        else:
                            # Single File Extras
                            try:
                                subprocess.check_call(['cp', extra_files_path, '{}/'.format(procdir)],
                                                      stdout=framelog)
                            except subprocess.CalledProcessError as err:
                                print("ERROR: Could not copy {}: {}. ".format(extra_files_path, err) +
                                      "Check the {} log".format(_FRAMEWORK_LOG_PATH), file=sys.stderr)
                                ferrors += 1
                                raise

                    # Enter Submission Directory
                    cwd = os.getcwd()
                    print("Entering {}".format(procdir))
                    os.chdir(procdir)
                    print("Running {}".format(script_path))

                    # Call Grading Script
                    grade = float('nan')
                    try:
                        output = subprocess.check_output([script_path], stderr=gradelog)
                        output_str = output.decode()
                        output_str_clean = output_str.rstrip().lstrip()
                        try:
                            grade = float(output_str_clean)
                        except ValueError as err:
                            print("ERROR: Could not convert '{}' to float: {}".format(output_str_clean, err), file=sys.stderr)
                            raise
                    except subprocess.CalledProcessError as err:
                        print("ERROR: Grading script returned error: " +
                              "Check the {} log".format(_GRADER_LOG_PATH), file=sys.stderr)
                        gerrors += 1
                    except PermissionError as err:
                        print("ERROR: Framework returned permission error: " +
                              "Does {} have execute permissions?".format(script_path), file=sys.stderr)
                        ferrors += 1

                    # Write Out Grade
                    if math.isfinite(grade):
                        scored += 1
                        if(math.ceil(grade) == _FULL_CREDIT):
                            fulls += 1
                        if(math.floor(grade) == _ZERO_CREDIT):
                            zeros += 1
                        try:
                            grades[student]['Grade'] = "{:.2f}".format(grade)
                        except KeyError as err:
                            print("ERROR: Student {} not found in grading worksheet: {}".format(student, err), file=sys.stderr)
                            ferrors += 1
                        else:
                            print("Grade = {}".format(grades[student]['Grade']))
                            print("Grade = {}".format(grades[student]['Grade']), file=gradelog)
                            print("\n", file=gradelog)
                            recorded += 1
                            nerrors += 1

                    # Leave Submission Directory
                    print("Returning to {}".format(cwd))
                    os.chdir(cwd)
                    print("Removing {}".format(procdir))
                    shutil.rmtree(procdir)

            except:
                raise
            finally:
                print("Returning to {}".format(origwd))
                os.chdir(origwd)
    except:
        raise
    finally:
        print("Removing {}".format(TEMPDIR))
        shutil.rmtree(TEMPDIR)

    # Write Output
    gw.write_worksheet(output_worksheet, grades, dialect, fields)

    # Close Logs
    framelog.close()
    gradelog.close()

    # Print Stats
    print("Submissions Found:    {}".format(found))
    print("Submissions Unzipped: {}".format(unzipped))
    print("Submissions Moved:    {}".format(moved))
    print("Submissions Scored:   {}".format(scored))
    print("Submissions Recorded: {}".format(recorded))
    print("Submissions Receiving Full Credit ({:6.2f}): {}".format(_FULL_CREDIT, fulls))
    print("Submissions Receiving Zero Credit ({:6.2f}): {}".format(_ZERO_CREDIT, zeros))
    print("Submissions Causing No Errors:        {}".format(nerrors))
    print("Submissions Causing Framework Errors: {}".format(ferrors))
    print("Submissions Causing Grader Errors:    {}".format(gerrors))

    return _EXIT_SUCCESS;

if __name__ == "__main__":
    sys.exit(_main())
