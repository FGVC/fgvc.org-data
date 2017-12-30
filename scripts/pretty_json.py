#!/usr/bin/python

import json
import argparse
import os.path
import shutil


def json_pretty( filename ):
    valid = True
    if not os.path.exists( filename ):
        print 'ERROR: Cannot find file: \"%s\"!!!'%filename
        valid = False

    obj = json.load( open(filename, 'r') )
    #shutil.copyfile(filename,'/tmp/tmp_json_pretty')
    json.dump( obj, open(filename, 'w'), indent=2 )



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("results_file", type=str, help="json results file to use" )
    args = parser.parse_args()

    json_pretty( args.results_file )

