#!/usr/bin/env python3

# Basic program to unzip a file of submission and walk each

import os
import subprocess
import shutil

tempDir = './tmp'

subprocess.check_call(['unzip', '-d', tempDir, 'in.zip'])

for rootdir, subdirs, subfiles in os.walk(tempDir):
    for subfile in subfiles:
        if (subfile.split('.')[-1] == 'zip'):
            print(subfile)

shutil.rmtree(tempDir)
