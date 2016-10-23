import os, sys
import audioprocessor as ap
import multiprocessing

if (__name__ == "__main__"):
	if (len(sys.argv) != 3):
		print "Please input: 1. audio directory, 2. train/valid/temp"
	else:
		audiodirectory = sys.argv[1]
		file_type = sys.argv[2]
		ap.extract(audiodirectory=audiodirectory, type=file_type, processes=1)
