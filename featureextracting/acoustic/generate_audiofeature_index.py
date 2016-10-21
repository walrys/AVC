import os, sys
import audioprocessor as ap
import multiprocessing

if (__name__ == "__main__"):
	#multiprocessing.set_start_method('spawn')
	ap.extract(audiodirectory='/Users/Brandon/Documents/CS2108-Vine-Dataset/mp4_training_wav', type='train', processes=1)