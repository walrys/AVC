# The simple implementation of obtaining the audio clip of a original video.

import os, sys
import moviepy.editor as mp
import utility.util as util

def getAudioClip(video_reading_path, audio_storing_path):
    clip = mp.VideoFileClip(video_reading_path)
    clip.audio.write_audiofile(audio_storing_path)

# input storage path
def batchAudioExtract(input_store_path):
	mp4_paths = util.get_mp4_paths(util.database_path)
	
	for path in mp4_paths:
		sound_file = os.path.basename(path)
		sound_file = input_store_path + "/" + sound_file[:len(sound_file) - 3] + "wav"
		getAudioClip(path, sound_file)

if __name__ == '__main__':
	if (len(sys.argv) != 2):
		print "Please input storage path directory for wav files"
	elif (not os.path.exists(sys.argv[1])):
		print "Please input valid storage path directory for wav files"
	else:
		input_store_path = sys.argv[1]
		batchAudioExtract(input_store_path)
	

