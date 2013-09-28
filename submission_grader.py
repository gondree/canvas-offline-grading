#!/usr/bin/env python3

# A sample "Hello World" submission grader

import subprocess
import sys

CORRECT = "Hello World"

try:
    output = subprocess.check_output(["python3", "submission.py"])
except CalledProcessError as err:
    print("0.00", file=sys.stdout)
    print("Error running submission: {!s}".format(err), file=sys.stderr)
    sys.exit(0)

outputStr = output.decode()
outputStrClean = outputStr.rstrip()

if (outputStrClean == CORRECT):
    print("100.00", file=sys.stdout)
else:
    print("0.00", file=sys.stdout)
    print("Looking for: {!s}".format(CORRECT), file=sys.stderr)
    print("Received:    {!s}".format(outputStrClean), file=sys.stderr)

sys.exit(0)
