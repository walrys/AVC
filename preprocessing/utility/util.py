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
# from the database
# eg. '...something.../CS2108-Vine-Dataset/vine/training/1023439919177490432.mp4'

def get_mp4_paths(input_path):
	mp4_paths = []
	
	mp4_paths = os.listdir(input_path);
	for i in xrange(len(mp4_paths)):
		if (mp4_paths[i].endswith('.mp4')):
			mp4_paths[i] = input_path + "/" + mp4_paths[i]

	return mp4_paths

#print get_venue_list("/Users/Brandon/Dropbox/NUS/Y3S1/CS2108/Lab/Assignment_2/CS2108-Vine-Dataset")
#print get_mp4_paths(database_path)