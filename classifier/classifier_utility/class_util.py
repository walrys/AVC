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

# returns a dictionary of index-venue key pair 
# eg. {1: 'City', 2: 'Theme Park' ...}

def get_venue_list(input_path):
	venues_dict = {}
	path = input_path + "/venue-name.txt"
	with open(path, 'r') as reader:
		venues = reader.readlines()

	for string in venues:
		divide = string.split("\t")
		divide[1] = divide[1][:-2]
		venues_dict[int(divide[0])] = divide[1]

	return venues_dict

# returns a dictionary of number-image pair
# eg. {'1000046931730481152': 1, ...], ...}

def get_video_category(input_path, textfile):
	video_category = {}
	path = input_path + "/" + textfile
	with open(path, 'r') as reader:
		line = reader.readlines()
	
	for string in line:
		divide = string.split("\t")
		divide[1] = divide[1][:-2]
		video_category[divide[0]] = int(divide[1])

	return video_category


# returns a list of full individual mp4 path 
# from the database by taking in an input_path
# eg. '...something.../CS2108-Vine-Dataset/vine/training/1023439919177490432.mp4'

def get_mp4_paths(input_path):
	mp4_paths = []
	
	mp4_paths = os.listdir(input_path);
	for i in xrange(len(mp4_paths)):
		if (mp4_paths[i].endswith('.mp4')):
			mp4_paths[i] = input_path + "/" + mp4_paths[i]

	return mp4_paths

# returns a dictionary of full jpg path with name and array of frames as key-value pair
# eg. {'1000046931730481152': [...something.../1000046931730481152-frame0.jpg, ...], ...}

def get_jpg_dictionary_path(input_path):
	frame_folder_paths = os.listdir(input_path)
	jpg_dict = {}
	for path in frame_folder_paths:
		full_path = input_path + "/" + path
		if (os.path.basename(full_path) != ".DS_Store"):
			jpg_paths = os.listdir(full_path)
			#print jpg_paths
			if (len(jpg_paths) > 0):
				for i in xrange(len(jpg_paths)):
					jpg_paths[i] = full_path + "/" + jpg_paths[i]
			jpg_dict[os.path.basename(path)] = jpg_paths

	return jpg_dict

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