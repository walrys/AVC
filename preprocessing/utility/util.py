import os, sys
import csv

""" A utility module with a bunch of functions that 
	manipulates database
""" 

# modify this to the database path to extract from database videos
database_path = "/Users/Brandon/Dropbox/NUS/Y3S1/CS2108/Lab/Assignment_2/CS2108-Vine-Dataset/vine/training"
query_path = "/Users/Brandon/Dropbox/NUS/Y3S1/CS2108/Lab/Assignment_2/CS2108-Vine-Dataset/vine/validation"

# returns a dictionary of index-venue key pair 
# eg. {1: 'City', 2: 'Theme Park' ...}

def get_venue_list(input_path):
	venues_dict = {}
	path = input_path + "/venue-name.txt"
	with open(path, 'r') as reader:
		venues = reader.readlines()

	for string in venues:
		divide = string.split("\t")
		divide[1] = divide[1][:len(divide[1]) - 2]
		venues_dict[int(divide[0])] = divide[1]

	return venues_dict

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
			for i in len(jpg_paths):
				jpg_paths[i] = full_path + "/" + jpg_paths[i]
			jpg_dict[os.path.basename(path)] = jpg_paths

	return jpg_dict

#print get_venue_list("/Users/Brandon/Dropbox/NUS/Y3S1/CS2108/Lab/Assignment_2/CS2108-Vine-Dataset")
#print get_mp4_paths(database_path)
#print get_jpg_dictionary_path("/Users/Brandon/Dropbox/NUS/Y3S1/CS2108/Lab/Assignment_2/CS2108-Vine-Dataset/vine/training/mp4_frames")