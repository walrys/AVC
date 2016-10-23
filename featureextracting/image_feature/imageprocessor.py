import os, sys
import image_utility.img_util as util
import csv
import tensorflow as tf
import classify_image
import math
import numpy as np

# to be used in UI

def deep_learning_vector(input_path, output_path, filename):
	classify_image.maybe_download_and_extract()
	image_folder = os.listdir(input_path)

	if (len(image_folder) > 0):
		image_index = int(math.floor(len(image_folder)/2.0))

		jpg = image_folder[image_index]
		image_path = input_path + "/" + jpg
		with tf.Graph().as_default():	
			vector = classify_image.run_inference_on_image(image_path)

		np.save(output_path + "/" + filename, [vector])


	return vector