import os, sys
import features_util as util
import numpy as np

feature_store_path = "../data"

if __name__ == "__main__":
	if (len(sys.argv) != 2):
		print "Please input: 1: path to concat"
	else:
		concat_path = sys.argv[1]

    # concatenate features and save as npy
    util.concatall(concat_path, concat_path)