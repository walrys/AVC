import moviepy.editor as mp
import os
import os.path


def getAudioClip(video_reading_path, audio_storing_path):
    clip = mp.VideoFileClip(video_reading_path)
    clip.audio.write_audiofile(audio_storing_path)


if __name__ == '__main__':
    
    directory  = "./"
    for filename in os.listdir(directory):
        if filename.endswith(".mp4"):
            audio_storing_path = directory + filename[:-4] + ".wav"
            if not os.path.isfile(audio_storing_path):
                getAudioClip(video_reading_path=filename, audio_storing_path=audio_storing_path)