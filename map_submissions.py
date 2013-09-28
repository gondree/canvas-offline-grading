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
        subfileSplit = subfile.split('.')
        if (subfileSplit[-1] == 'zip'):
            print("Processing {!s}".format(subfile))
            outDir = ''.join(subfileSplit[:-1])
            subprocess.check_call(['unzip', '-d', outDir, subfile])
            origcwd2 = os.getcwd()
            print("Entering {!s}".format(outDir))
            os.chdir(outDir)
            print("Submission contains: {!s}".format(os.listdir()))
            print("Returning to {!s}".format(origcwd2))
            os.chdir(origcwd2)
            print("Removing {!s}".format(tempDir))
            shutil.rmtree(outDir)

    print("Returning to {!s}".format(origcwd1))
    os.chdir(origcwd1)

print("Removing {!s}".format(tempDir))
shutil.rmtree(tempDir)
