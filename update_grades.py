#!/usr/bin/env python3

# Basic program to read csv file and spit it back out

import csv

rows = []
students = {}
gradeDialect = None
fieldNames = None

csv.register_dialect('moodle',
                     delimiter=',',
                     quotechar='"',
                     quoting=csv.QUOTE_MINIMAL,
                     lineterminator='\n')

with open('in.csv', 'r', newline='') as gradeFileIn:

    gradeDialect = csv.Sniffer().sniff(gradeFileIn.read())
    gradeFileIn.seek(0)
    gradeHeader = csv.Sniffer().has_header(gradeFileIn.read())
    gradeFileIn.seek(0)
    gradeReader = csv.DictReader(gradeFileIn, dialect=gradeDialect)
    fieldNames = gradeReader.fieldnames

    for row in gradeReader:
        rows += [row]

for row in rows:
    students[row['Full name']] = row

with open('out.csv', 'w', newline='') as gradeFileOut:

    gradeWriter = csv.DictWriter(gradeFileOut, fieldNames, dialect=gradeDialect)
    gradeWriter.writeheader()

    for v in students.values():
        gradeWriter.writerow(v)
