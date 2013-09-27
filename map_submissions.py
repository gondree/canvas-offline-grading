#!/usr/bin/env python3

# Basic program to unzip a file of submission and walk each

import os
import subprocess

tempDir = './tmp'

subprocess.check_call(['unzip', '-d', tempDir, 'in.zip'])
