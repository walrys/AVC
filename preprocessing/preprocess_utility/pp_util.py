import os, sys, random
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
		divide[1] = divide[1][:len(divide[1]) - 2]
		venues_dict[int(divide[0])] = divide[1]

	return venues_dict

# returns a dictionary of number-image pair
# eg. {'1000046931730481152': 1, ...], ...}

def get_video_category(input_path, textfile):
	video_category = {}
	venues_dict = get_venue_list(input_path)
	path = input_path + "/" + textfile
	with open(path, 'r') as reader:
		line = reader.readlines()
	
	for string in line:
		divide = string.split("\t")
		divide[1] = divide[1][:-2]
		video_category[divide[0]] = int(divide[1])

	return video_category

# returns an integer image_list pair
# eg. {1: ['1000046931730481152', ...], ...}

def get_video_category_by_number(input_path, textfile):
	video_category = {}
	venues_dict = get_venue_list(input_path)
	path = input_path + "/" + textfile
	with open(path, 'r') as reader:
		line = reader.readlines()
	
	for string in line:
		divide = string.split("\t")
		divide[1] = divide[1][:-2]
		if (not int(divide[1]) in video_category):
			video_list = []
			video_list.append(divide[0])
			video_category[int(divide[1])] = video_list
		else:
			video_category[int(divide[1])].append(divide[0])	

	return video_category


"""def create_textfile(input_path, originalTextFile, newTextFile_validation, new_TextFile_test):
	path = input_path + "/" + originalTextFile
	mp4_path_validation = get_mp4_paths(input_path + "/vine/validation")
	mp4_path_test = get_mp4_paths(input_path + "/vine/test")

	with open(path, 'r') as reader:
		line = reader.readlines()
		
		for string in line:
			divide = string.split("\t")"""

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

# randomly selects 30 video files as the test set from each category to test

def split_validation_testing(input_path, input_test_path, vine_path):
	# randomly choose 30 videos for test videos, one from each category
	video_category = get_video_category_by_number(vine_path, "vine-venue-validation.txt")
	for i in xrange(30):
		rand_int = random.randint(0, len(video_category[i+1]) - 1)
		video_name = os.path.basename(video_category[i+1][rand_int] + ".mp4")
		os.rename(input_path + "/" + video_name, input_test_path + "/" + video_name)



#print get_venue_list("/Users/Brandon/Documents/CS2108-Vine-Dataset")
#print get_mp4_paths(database_path)
#print len(get_mp4_paths(query_path))
#print len(get_mp4_paths(test_path))
#print get_jpg_dictionary_path("/Users/Brandon/Documents/CS2108-Vine-Dataset/mp4_frames")
#split_validation_testing(query_path, test_path, vine_path)