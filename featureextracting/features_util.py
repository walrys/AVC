import os, sys
import csv
import numpy as np

""" A utility module with a bunch of functions that 
	manipulates database
""" 

def get_array_order(input_path):
	array_order = []
	with open(input_path, 'r') as reader:
		files = reader.read()
		array_order = files.split("\n")

	return array_order

def get_labels_ordered(input_path, array_order):
	unordered_dict = {}
	ordered_array = []
	with open(input_path, 'r') as reader:
		files = reader.read()
		unordered_array = files.split("\n")
		for item in unordered_array:
			name, integer = item.split("\t")
			unordered_dict[name] = int(integer)

	for name in array_order:
		ordered_array.append(unordered_dict[name])
		#print name, unordered_dict[name]

	return ordered_array

def concatenate(file1,file2,output):
    arr1 = np.load(file1)
    arr2 = np.load(file2)
    result = []

    print arr1
    print arr2

    for i in range(len(arr1)):
        result.append(np.append(arr1[i],arr2[i],axis=0))
   
    np.save(output,result)
    print "first array: " + str(len(arr1[0]))
    print "second array: " + str(len(arr2[0]))
    print "result array: " + str(len(result[0]))

    del arr1
    del arr2
    del result


def concatall(directory,output):
    files = []
    temp = output + '/temp.npy'
    for a_file in os.listdir(directory):
        files.append(directory+'/'+a_file)

    #if (os.listdir(output)[0] == ".DS_Store"):
        #os.remove(output + "/.DS_Store")   
    print
    print 'concatenating all files...'
    for i in xrange(len(files)-1):
        print 'merging '+str(i+1)+ ' of ' + str(len(files)-1)
        if files[i].endswith(".npy"):
            if os.path.isfile(output + "/.DS_Store"):
                if i == 1:
                    concatenate(files[i],files[i+1], temp)
                elif i+1==len(files)-1:
                    concatenate(temp,files[i+1], output)
                    print 'removing temp files...'
                    os.remove(temp)
                else:
                    concatenate(temp,files[i+1],temp)

            else:
                if i == 0:
                    concatenate(files[i],files[i+1], temp)

                elif i+1==len(files)-1:
                    concatenate(temp,files[i+1], output)
                    print 'removing temp files...'
                    os.remove(temp)
                else:
                    concatenate(temp,files[i+1],temp)
    
    print 'concatenation complete!'