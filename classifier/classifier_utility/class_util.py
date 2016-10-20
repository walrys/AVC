import os, sys
import csv

""" A utility module with a bunch of functions that 
	manipulates database
""" 

# modify this to the database path to extract from database videos
vine_path = "/Users/Brandon/Documents/CS2108-Vine-Dataset"
database_path = "/Users/Brandon/Documents/CS2108-Vine-Dataset/vine/training"
query_path = "/Users/Brandon/Documents/CS2108-Vine-Dataset/vine/validation"
test_path = "/Users/Brandon/Documents/CS2108-Vine-Dataset/vine/test"

def get_venue_list(input_path):
    venues_array = []
    path = input_path + "/venue-name.txt"
    with open(path, 'r') as reader:
        venues = reader.readlines()

    for string in venues:
        divide = string.split("\t")
        divide[1] = divide[1][:-2]
        venues_array.append(divide[1])

    return venues_array

def get_array_order(input_path):
	array_order = []
	with open(input_path, 'r') as reader:
		files = reader.read()
		array_order = files.split("\n")

	return array_order

def get_labels_ordered(input_path, array_order):
	unordered_dict = {}
	ordered_array = []
	with open(input_path, 'r') as reader:
		files = reader.read()
		unordered_array = files.split("\n")
		for item in unordered_array:
			name, integer = item.split("\t")
			unordered_dict[name] = int(integer)

	for name in array_order:
		ordered_array.append(unordered_dict[name])
		#print name, unordered_dict[name]

	return ordered_array

def extractFeature(csv_path):
    image_features = {}
    with open(csv_path, 'r') as reader:
        csv_reader = csv.reader(reader)
        
        for feature in csv_reader:
            keyword = feature.pop(0)
            #normalized distance
            image_features[keyword] = feature

    return image_features

# Parameters: features dictionary -> filename - feature vector
# to convert feature dictionary to feature array
# eg. {'image_name_1: [f1.1, f1.2, ...]', 'image_name_2': [f2.1, f2.2, ...], ...}
#       -> [[f1.1, f1.2, ...], [f2.1, f2.2, ...], ...]

def features_toArray(data_dict):
    dataset_feature = []
    for name, vector in data_dict.iteritems():
        dataset_feature.append(vector)

    return dataset_feature

def names_toArray(data_dict):
	dataset_names = []
	for name, vector in data_dict_iteritems():
		dataset_names.appened(name)

	return dataset_names

# Parameters: features_dictionary -> filename - feature vector 
#             labels dictionary -> filename - label integer
# to convert labels dictionary to labels array
# eg. {'image_name_1: 2, 'image_name_2': 15, ...}
#       -> [1, 15, ...]
# note: because ordering of features dictionary != ordering of labels dictionary,
#       we need the features dictionary as reference to find the correct corresponding labels

def gndTruth_toArray(data_dict, data_label_dict):
    dataset_label = []
    for name, vector in data_dict.iteritems():
        #array = []
        #array.append(data_train_label_dict[name[:-4]])
        dataset_label.append(data_label_dict[name[:-4]])

    return dataset_label

# Parameters: label name : Integer - string
# converts all labels (aka categories) into an array of just the label name
# eg. {1: 'label_1', 2: 'label_2', ...} -> [label_1, label_2, ...]

def label_toArray(data_label_dict):
    data_label = []
    for name, label_name in data_label_dict.iteritems():
        #array = []
        #array.append(vector)
        data_label.append(label_name)

    return data_label

#print get_venue_list("/Users/Brandon/Dropbox/NUS/Y3S1/CS2108/Lab/Assignment_2/CS2108-Vine-Dataset")
#print get_mp4_paths(database_path)
#print get_jpg_dictionary_path("/Users/Brandon/Dropbox/NUS/Y3S1/CS2108/Lab/Assignment_2/CS2108-Vine-Dataset/mp4_frames")
#print get_video_category("/Users/Brandon/Documents/CS2108-Vine-Dataset/", "vine-venue-training.txt")
#print get_video_category("/Users/Brandon/Documents/CS2108-Vine-Dataset/", "vine-venue-validation.txt")