#!/usr/bin/env python3

# Basic program to unzip a file of submission and walk each

import os
import subprocess
import shutil

tempDir = './tmp'

subprocess.check_call(['unzip', '-d', tempDir, 'in.zip'])

for rootDir, subdirs, subfiles in os.walk(tempDir):

    origcwd1 = os.getcwd()
    print("Entering {!s}".format(rootDir))
    os.chdir(rootDir)

    for subfile in subfiles:
        if (subfile.split('.')[-1] == 'zip'):
            print("Processing {!s}".format(subfile))
            subprocess.check_call(['unzip', '-d', tempDir, subfile])
            origcwd2 = os.getcwd()
            print("Entering {!s}".format(tempDir))
            os.chdir(tempDir)
            print("Submission contains: {!s}".format(os.listdir()))
            print("Returning to {!s}".format(origcwd2))
            os.chdir(origcwd2)
            print("Removing {!s}".format(tempDir))
            shutil.rmtree(tempDir)

    print("Returning to {!s}".format(origcwd1))
    os.chdir(origcwd1)

print("Removing {!s}".format(tempDir))
shutil.rmtree(tempDir)
