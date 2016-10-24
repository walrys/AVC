import os, sys
#import image_feature.imageprocessor as image
import features_util as util

def combine_features(temp_wav_path, temp_jpg_path, output_path):
	# extract features out and save temporarily as npy
    #image.deep_learning_vector(temp_jpg_path, output_path, "image_temp.npy")
    
    # concatenate
    util.concatall(output_path, output_path)