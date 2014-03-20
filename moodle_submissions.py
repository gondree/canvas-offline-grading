#!/usr/bin/env python3

# Module for parsing and manipulating Moodle submissions

import sys

_FIELD_SEPERATOR = '_'
_TYPE_SEPERATOR = '.'

class Submission:

    def __init__(self, path):

        self.path = path

        # Extract Subfields
        fields = self.path.split(_FIELD_SEPERATOR)
        self.submitter_name = fields[0]
        self.submitter_id = fields[1]
        self.file_name = _FIELD_SEPERATOR.join(fields[4:])
        dots = self.file_name.split(_TYPE_SEPERATOR)
        self.file_type = dots[-1]
        self.file_base = _TYPE_SEPERATOR.join(dots[:-1])
