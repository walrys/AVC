# The simple implementation of obtaining the audio clip of a original video.

import os, sys
import moviepy.editor as mp
import preprocess_utility.pp_util as util

def getAudioClip(video_reading_path, audio_storing_path):
	"""if (os.path.basename(video_reading_path) == "1001032302756761600.mp4"
		or os.path.basename(video_reading_path) == "1005958035061297152.mp4"):
		size = 150000
	elif (os.path.basename(video_reading_path) == "1001088152326610944.mp4"):
		size = 5000
	else:
		size = 200000"""
	try:
		clip = mp.VideoFileClip(video_reading_path)
		clip.audio.write_audiofile(audio_storing_path)
	except IOError:
		print "An IOError has occured"

# input storage path
def batchAudioExtract(input_store_path, database_path):
	mp4_paths = util.get_mp4_paths(database_path)
	
	for path in mp4_paths:
		sound_file = os.path.basename(path)
		sound_file = input_store_path + "/" + sound_file[:len(sound_file) - 3] + "wav"
		getAudioClip(path, sound_file)

# arg[1] = storage path
# arg[2] = database path

if __name__ == '__main__':
	if (len(sys.argv) != 3):
		print "Please input storage path directory for wav files or input source path"
	elif (not os.path.exists(sys.argv[1]) or not os.path.exists(sys.argv[2])):
		print "Please input valid storage path directory for wav files"
	else:
		input_store_path = sys.argv[1]
		database_path = sys.argv[2]
		#mp4_path = "/Users/Brandon/Dropbox/NUS/Y3S1/CS2108/Lab/Assignment_2/CS2108-Vine-Dataset/vine/training/1005958035061297152.mp4"
		#sound_file = input_store_path + "/" + os.path.basename(mp4_path)[:-3] + "wav"
		#getAudioClip(mp4_path, sound_file)
		batchAudioExtract(input_store_path, database_path)
	

