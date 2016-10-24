# The simple implementation of obtaining the audio clip of a original video.

import os, sys
import moviepy.editor as mp

def getAudioClip(video_reading_path, audio_storing_path):
    try:
        clip = mp.VideoFileClip(video_reading_path)
        clip.audio.write_audiofile(audio_storing_path)
    except IOError:
        print "An IOError has occured. Error while extracting audio file from mp4"

# input storage path
def batchAudioExtract(video_reading_directory, audio_storing_directory):
    for filename in os.listdir(video_reading_directory):
        if filename.endswith(".mp4"):
            video_reading_path = video_reading_directory + '/' + filename
            audio_storing_path = audio_storing_directory + '/' + filename[:-4] + ".wav"
            if not os.path.isfile(audio_storing_path):
                getAudioClip(video_reading_path, audio_storing_path)

# arg[1] = storage path
# arg[2] = source path

if __name__ == '__main__':
    if (len(sys.argv) != 3):
        #video_reading_directory = "../queries"
        #audio_storing_directory = "../temp/wav"
        #batchAudioExtract(video_reading_directory, audio_storing_directory)
        #print "audio extracted from videos in \""+video_reading_directory+"\""
        print 'not enough arguments'
        print sys.argv[1]
        print sys.argv[2]
        '''
    elif (not os.path.exists(sys.argv[1]) or not os.path.exists(sys.argv[2])):
        print "Please input valid storage path directory for wav files"
        print "arguments given:"
        print sys.argv[1]
        print sys.argv[2]
        '''
    else:
        video_reading_path = sys.argv[1]
        audio_storing_path = sys.argv[2]
        getAudioClip(video_reading_path, audio_storing_path)
        #batchAudioExtract(video_reading_path, audio_storing_path)