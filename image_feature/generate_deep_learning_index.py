import os, sys
import image_utility.img_util as util
import csv
import tensorflow as tf
import classify_image

""" takes multiple images and runs deep learning feature
		on all images, outputting as csv file
	"""
def create_DL_image_index(input_path):
	classify_image.maybe_download_and_extract()
	jpg_dict_paths = util.get_jpg_dictionary_path(input_path)
	with open('DL_image_features.csv', 'w') as output:
		writer = csv.writer(output)

		for name, images in jpg_dict_paths.iteritems():
			vid_name = name
			
			# how to deal with multiple images?

			with tf.Graph().as_default():	
				predictions = classify_image.run_inference_on_image(image_path)
			
			vectorArray = predictions.tolist()
			vectorArray.insert(0, vid_name)
			writer.writerows([vectorArray])

create_DL_image_index("/Users/Brandon/Dropbox/NUS/Y3S1/CS2108/Lab/Assignment_2/CS2108-Vine-Dataset/mp4_frames")