import os, sys
import image_utility.img_util as util
import csv
import tensorflow as tf
import classify_image
import math
import numpy as np

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

def create_DL_image_npy(input_path, filename):
	classify_image.maybe_download_and_extract()
	folderlist = os.listdir(input_path)
	image_vectors = [] 
	i = 0

	for image in folderlist:
		if (image != ".DS_Store"):
			image_folder = os.listdir(input_path + "/" + image)

			if (len(image_folder) > 0):
				image_index = int(math.floor(len(image_folder)/2.0))

				jpg = image_folder[image_index]
				image_path = input_path + "/" + image + "/" + jpg

				with tf.Graph().as_default():
					vector = classify_image.run_inference_on_image(image_path)	

				image_vectors.append(vector)
				print image, vector
			else:
				vector = [0 for x in xrange(1008)]
				image_vectors.append(vector)

		i+= 1
		print i
		#if (i ==10):
			#break
		#printProgress (i, len(folderlist), prefix = "Time left", suffix = '', decimals = 1, barLength = 50)
	#print image_vectors
	np.save(input_path + "/" + filename, image_vectors)

	print "done!"

def printProgress (iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 50):
    formatStr       = "{0:." + str(decimals) + "f}"
    percents        = formatStr.format(100 * (iteration / float(total)))
    filledLength    = int(round(barLength * iteration / float(total)))
    bar             = '|' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "Please input argument: 1: image folder path, 2: name of output"
	else:
		input_path = sys.argv[1]
		filename = sys.argv[2]

		create_DL_image_npy(input_path, filename)

