#!/usr/bin/env python3

import csv

with open('test.csv', newline='') as gradeFile:

    dialect = csv.Sniffer().sniff(gradesheet.read(1024))
    gradeFile.seek(0)
    gradereader = csv.reader(gradesheet, dialect)

    for row in gradereader:
        print(', '.join(row))
