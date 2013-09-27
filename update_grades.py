#!/usr/bin/env python3

import csv

with open('test.csv', newline='') as gradeFile:

    dialect = csv.Sniffer().sniff(gradeFile.read(1024))
    gradeFile.seek(0)
    gradeReader = csv.reader(gradeFile, dialect)

    for row in gradeReader:
        print(', '.join(row))
