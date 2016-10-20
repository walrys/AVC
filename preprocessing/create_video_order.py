import os, sys

if __name__ == "__main__":
	input_path = sys.argv[1]
	filename = sys.argv[2]

	count = 0
	folderlist = os.listdir(input_path)

	with open(filename, 'w') as writer:
		for image in folderlist:
			if (image.endswith(".wav")):
				writer.write(image[:-4] + "\n")
				count += 1

	print count
	print "done!"
			