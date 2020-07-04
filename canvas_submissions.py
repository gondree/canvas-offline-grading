#!/usr/bin/env python3

# Module for parsing and manipulating Moodle submissions

import sys
import os
import json
import pprint
from argparse import ArgumentParser
from canvasapi import Canvas
from canvasapi.file import File

_FIELD_SEPERATOR = '_'
_TYPE_SEPERATOR = '.'
pp = pprint.PrettyPrinter(indent=4, compact=True)

class Submission:

    def __init__(self, path, file_name):

        # Extract Subfields
        path = path.split('/')[-1]
        fields = path.split(_FIELD_SEPERATOR)
        self.submitter_name = fields[0]
        self.submitter_id = fields[1]
        self.path = path
        self.file_name = file_name
        dots = self.file_name.split(_TYPE_SEPERATOR)
        self.file_type = dots[-1]
        self.file_base = _TYPE_SEPERATOR.join(dots[:-1])



if __name__ == '__main__':
    SCRIPTPATH = os.path.dirname(os.path.abspath(__file__))

    parser = ArgumentParser(description='Download submissions from Canvas')
    parser.add_argument("--ASSIGNMENT_ID", type=int, 
        dest='ASSIGNMENT_ID', default=None, required=True,
        help="Canvas Assignment ID")
    parser.add_argument("--COURSE_ID", type=int, 
        dest='COURSE_ID', default=None, required=True,
        help="Canvas Course ID")
    parser.add_argument("--API_URL", type=str, 
        dest='API_URL', default=None, required=True,
        help="Canvas API URL")
    parser.add_argument("--API_KEY", type=str, 
        dest='API_KEY', default=None, required=True,
        help="Canvas API URL")

    parser.add_argument("--mode", type=str, 
        dest='mode', default='get', required=False,
        help="Mode: 'get' or 'put'")
    parser.add_argument("--directory", type=str, 
        dest='path', default=None, required=True,
        help="Path to where to store files, or get feedback")

    args = parser.parse_args()
    OPT = vars(args)


    canvas = Canvas(OPT['API_URL'], OPT['API_KEY'])
    course = canvas.get_course(OPT['COURSE_ID'])
    assignment = course.get_assignment(OPT['ASSIGNMENT_ID'])
    
    students = {}
    if True:
        # look at student info
        for s in assignment.get_gradeable_students():
            #print(type(s), dir(s))
            students[s.id] = s

    for s in assignment.get_submissions():
        print("User ID", s.user_id, '=', students[s.user_id].display_name)
        
        if s.user_id != 7196:
            continue

        print("Submission Object", type(s), dir(s), s)
        pp.pprint(s)
        
        if not 'attachments' in dir(s):
            print("No Attachments:")
        else:
            print("Attachments:", len(s.attachments))
            for a in s.attachments:
                #print("   Attachment Object:", type(a), dir(a), a)
                #pp.pprint(a)

                f = File(s._requester, a)
                path = OPT['path'].rstrip('/') + '/' + str(a['id']) + '/'
                if os.path.isdir(path):
                    print('\tExists already -- maybe part of a group?')
                    continue
                os.makedirs(path)
                filename = path + a['filename']
                f.download(filename)
                print("\t", "Filename:", filename)
                print("\t  ", "Submitted:", s.submitted_at)
                print("\t  ", "created_at:", a['created_at'])
                print("\t  ", "updated_at:", a['updated_at'])
                print("\t  ", "modified_at:", a['modified_at'])
                print("\t  ", "workflow_state:", a['workflow_state'])
        print()



    if OPT['mode'] == 'get':
        pass

    if OPT['mode'] == 'put':
        pass

