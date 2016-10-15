import os, sys
import image_utility.img_util as util
import csv
import tensorflow as tf
import classify_image

""" takes multiple images and runs deep learning feature
		on all images, outputting as csv file
	"""
def create_DL_image_index(input_path, filename):
	classify_image.maybe_download_and_extract()
	jpg_dict_paths = util.get_jpg_dictionary_path(input_path)
	with open(filename, 'w') as output:
		writer = csv.writer(output)
		count = 0

		for name, images in jpg_dict_paths.iteritems():
			vid_name = name
			average_vector = []

			# calculate average vector values
			if (len(images) > 0):
				predictions = []
				for an_image in images:
					with tf.Graph().as_default():	
						predictions.append(classify_image.run_inference_on_image(an_image).tolist())

				for point in xrange(1008):
					total = 0.0
					for i in xrange(len(predictions)):
						total += predictions[i][point]
					average_vector.append(total/len(predictions))
			else:
				with tf.Graph().as_default():	
						average_vector = classify_image.run_inference_on_image(an_image).tolist()
			count += 1
			print str(count) + " image done"
			vectorArray = average_vector
			vectorArray.insert(0, str(vid_name) + ".mp4")
			writer.writerows([vectorArray])

#create_DL_image_index("/Users/Brandon/Documents/CS2108-Vine-Dataset/mp4_training_frames", "DL_image_training_features.csv")
create_DL_image_index("/Users/Brandon/Documents/CS2108-Vine-Dataset/mp4_validation_frames", "DL_image_validation_features.csv")

