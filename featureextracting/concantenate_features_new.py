import os, sys
import acoustic.audioprocessor as audio
import image_feature.imageprocessor as image
import features_util as util

def combine_features(input_path, temp_wav_path, temp_jpg_path):
	# extract features out and save temporarily as npy
    image.deep_learning_vector(temp_jpg_path, "image_temp.npy")
    audio.extract(audio_directory=temp_wav_path, processes=1)

    # move concatenated file

    # concatenate

    # return concatenated features / save them
    