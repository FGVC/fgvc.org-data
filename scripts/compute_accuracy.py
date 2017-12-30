#!/usr/bin/python

import json
import argparse
import os.path
import numpy as np


def verify_valid_resultsfile( filename ):
    try:
        valid = True
        if not os.path.exists( filename ):
            print 'ERROR: Cannot find file: \"%s\"!!!'%filename
            valid = False

        obj = json.load( open(filename, 'r') )

        if not obj.has_key('dataset'):
            print 'ERROR: Results file not formatted correctly!!!'
            valid = False

        #print obj['dataset']
        ds_info = json.load( open('%s/dataset_info.json'%obj['dataset'],'r') )
        ncats = ds_info['num_categories']
        ntest = ds_info['num_test_images']
        gt    = ds_info['testing_images']

        predictions = obj['predictions']

        if not len(predictions.keys()) == ntest:
            print 'ERROR: Incorrect number of prediction entries!!!'
            valid = False

        for k in predictions.keys():
            if (type(predictions[k]) == list):
                if not len(predictions[k]) == ncats:
                    print 'ERROR: Incorrect number of predicted categories!!!'
                    valid = False
                    break
            elif (type(predictions[k]) == int):
                # this means they just predicted the class #
                pass
            else:
                print 'ERROR: Invalidly formatted prediction!!!'
                valid = False
                break

        # Check that image names match
        for img in gt.keys():
            #print '%s ===> %s' % (img,gt[img])
            fname = img
            if not fname in predictions.keys():
                fname = img.split('/')[-1]
            if not fname in predictions.keys():
                print 'ERROR: Couldn\'t find prediction for \'%s\'!!!'%img
                valid = False
                break
            

           
        return obj if valid else None

    except Exception as e:
        print e
        return None

def compute_accuracy( results_obj ):

    ds_info = json.load( open('%s/dataset_info.json'%results_obj['dataset'],'r') )
    ncats = ds_info['num_categories']
    ntest = ds_info['num_test_images']
    gt    = ds_info['testing_images']
    predictions = results_obj['predictions']
    cat_map = dict( [ (val,idx) for idx,val in \
                      enumerate(ds_info['ordered_class_list']) ] )

    # Check that image names match
    conf_mat = np.zeros( (ncats,ncats) )
    #print correct_by_class.shape
    #print nimgs_by_class.shape
    if results_obj['method_details'].has_key('prediction_type'):
        t = results_obj['method_details']['prediction_type']
        if t == "0-based integer":
            offset = 0
        elif t == "1-based integer":
            offset = -1
        elif t == "probability vector":
            pass

    for img_name in gt.keys():
        fname = img_name
        if not fname in predictions.keys():
            fname = img_name.split('/')[-1]
        # DON'T NEED TO CHECK IF KEY IS THERE, ALREADY DID THAT IN VERIFY...()
        gt_lbl   = cat_map[gt[img_name]]
        p = predictions[fname]
        if type(p) == int:
            pred_lbl = p + offset
        elif type(p) == list:
            pred_lbl = np.argmax( p )
        #pred_lbl = cat_map[predictions[fname]]
        conf_mat[gt_lbl,pred_lbl] += 1.0
            
    # print accuracy
    #print conf_mat
    #print np.sum(conf_mat[:])
    #np.save('/tmp/confmat.npy',conf_mat)

    overall_avg = (100.0*np.trace(conf_mat) / np.sum(conf_mat[:]))
    print 'Overall Accuracy = %2.2f' % overall_avg

    class_avg = 100.0*np.mean(np.diag(conf_mat) / np.sum(conf_mat,axis=1))
    print 'Average Class Accuracy = %2.2f' % class_avg


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("results_file", type=str, help="json results file to use" )
    args = parser.parse_args()
    #print args.results_file

    valid = verify_valid_resultsfile( args.results_file )
    if valid:
        compute_accuracy( valid )

