import numpy as np
import collections
import sys
import gc
import os
import csv
import extract_acoustic_batch as extractor

# main function that does everything (does not include extracting wav files)
# comment out to disable any steps if necessary!
# INPUT:    i.  audio directory containing all audio files
#           ii. type of data (training/validation)
#           iii.number of processes to handle extraction (depending on your machine)
# OUTPUT:   final concatenated array to be used for classifier (convert to matrix first!)

def extract(audiodirectory='../../../CS2108-Vine-Dataset/vine/training/audio',type= 'train',processes=6):
    # 1. extract all feature files into directory
    # WARNING: TAKES AT LEAST 10 MINUTES
    extractor.extractAll(audiodirectory,processes)
    # 2. combine all feature files into feature dictionary
    collateall(audiodirectory,type)
    # 3. remove feature vector files
    removeVectors(audiodirectory)
    
    audiodirectory += '/'+type
    
    # 4. shorten features to match shortest file and concatenate to get final array
    shortenAll(audiodirectory,type)
    concatall(audiodirectory+'/short/',audiodirectory+'/short/'+type+'_emsz_'+'short.npy')
    
    # 5. lengthen features to match longest file and concatenate to get final array
    lengthenAll(audiodirectory,type)
    concatall(audiodirectory+'/long/',audiodirectory+'/long/'+type+'_emsz_'+'long.npy')

#Concatenates all arrays in the folder
def concatall(directory,output):
    files = []
    temp = output[:-4]+'temp.npy'
    for file in os.listdir(directory):
        files.append(directory+'/'+file)
    for i in range(len(files)-1):
        print 'merging '+str(i+1)+ ' of ' + str(len(files))
        if i==0:
            concatenate(files[i],files[i+1],temp)
        elif i+1==len(files)-1:
            concatenate(temp,files[i+1], output)
            print 'removing ' + temp +'...'
            os.remove(temp)
        else:
            concatenate(temp,files[i+1],temp)

#Concatenates 2 2D-arrays of equal height
def concatenate(file1,file2,output):
    arr1 = np.load(file1)
    arr2 = np.load(file2)
    result = []
    for i in range(len(arr1)):
        result.append(np.append(arr1[i],arr2[i],axis=0))
    del arr1
    del arr2
    np.save(output,result)
    del result

def shortenAll(directory,type):
    shorten(directory,type+'_'+'spect'+'.npy')
    shorten(directory,type+'_'+'mfcc'+'.npy')
    shorten(directory,type+'_'+'energy'+'.npy')
    shorten(directory,type+'_'+'zero'+'.npy')
    
def lengthenAll(directory,type):
    lengthen(directory,type+'_'+'spect'+'.npy')
    lengthen(directory,type+'_'+'mfcc'+'.npy')
    lengthen(directory,type+'_'+'energy'+'.npy')
    lengthen(directory,type+'_'+'zero'+'.npy')

# 1.shortens all features to shortest length and concatenate into 1D and
# outputs np.matrix (shape(3000,shortest length*k) where k is number of lines in feature vector
# eg. shorten('./','mfcc.npy')
def shorten(directory,file):
    dict = np.load(directory+'/'+file).item()
    dict = collections.OrderedDict(sorted(dict.items()))
    isContiguous = dict.itervalues().next().flags['F_CONTIGUOUS']
    result = []
    if(isContiguous): #eg. energy, zero
        #find shortest length SL
        SL = 9999999
        for line in dict:
            if(len(dict[line]) < SL):
                SL = len(dict[line])
        #extract array
        for line in dict: #for every feature vector in dictionary
            result.append((dict[line])[:SL]) #trim to length SL and add to array result
    
    else: #eg. mfcc, spectrum
        #find shortest length SL
        SL = 9999999
        for arr in dict:
            for line in dict[arr]:
                if(len(line) < SL):
                    SL = len(line)
        #extract array
        for arr in dict:
            x = np.array([])
            for line in dict[arr]:
                x = np.append(x,line[:SL],axis=0) #trim to length SL
            result.append(x) #add concatenated array to result
    
    directory+='/short'
    if not os.path.exists(directory):
        os.makedirs(directory)
    np.save(directory+'/'+file[:-4]+'_short.npy',result)
    
# 2. lengthen all features to max length and concatenate into 1D and outputs array (shape(3000,max*k) where k is number of lines in feature vector
# eg. lengthen('./','mfcc.npy')
def lengthen(directory,file):
    dict = np.load(directory+'/'+file).item()
    dict = collections.OrderedDict(sorted(dict.items()))
    
    isContiguous = dict.itervalues().next().flags['F_CONTIGUOUS']
    if(isContiguous): #eg. energy, zero
        result = []
        #find greatest length GL
        GL = 0
        for line in dict:
            if(len(dict[line]) > GL):
                GL = len(dict[line])
        #extract array
        for line in dict: #for every feature vector in dictionary
            a = list(dict[line])
            b = list(dict[line])
            while(len(a)<GL):
                a = a + b #duplicate array to fit GL
            result.append(a[:GL]) #trim to length GL and add to array result
            del a
            del b
    
    else: #eg. mfcc, spectrum
        #find greatest length GL
        GL = 0
        width = 0
        for arr in dict:
            width = len(dict[arr])
            for line in dict[arr]:
                if(len(line) > GL):
                    GL = len(line)
        print "GL = " + str(GL)
        print 'width = ' + str(width)
        
        #initialise result array
        result = []
        
        #extract array
        i = 0
        for arr in dict:
            x = []
            for line in dict[arr]:
                a = list(line)
                b = list(line)
                while(len(a) < GL):
                    a = a + b
                x += (a[:GL]) #trim to length GL
                del a
                del b
            #add concatenated array to result    
            result.append(x)
            del x
            printProgress (i, len(dict), 'Concatenating', '', decimals = 1, barLength = 50)
            i+=1
    directory+='/long'
    if not os.path.exists(directory):
        os.makedirs(directory)
    np.save(directory+'/'+file[:-4]+'_long.npy',result)

    
# gather all feature vectors and save it into a dictionary. (eg. MFCC.npy, energy.npy)
# usage: collate('mfcc', './audiodirectory')
def collate(featuretype,type,directory = "./"):    
    foldersize = len([name for name in os.listdir(directory)])
    dict = {}
    counter = 0
    print 'collating '+type+'_'+featuretype+'.npy...'
    for file in os.listdir(directory):
        if file.endswith(featuretype + ".npy"):
            filename = file.replace("_"+featuretype+".csv","")
            array = np.load(directory+'/'+file)
            dict[filename] = array
        counter+=1
        printProgress(counter, foldersize, prefix = featuretype+':', suffix = '', decimals = 2, barLength = 50)
    dict = collections.OrderedDict(sorted(dict.items()))
    directory += '/'+type
    if not os.path.exists(directory):
        os.makedirs(directory)
    np.save(directory+'/'+type+'_'+featuretype+'.npy',dict)
    

def collateall(directory = './', type = 'train'):
    collate("energy",type,directory)
    collate("mfcc",type,directory)
    collate("spect",type,directory)
    collate("zero",type,directory)
    
def removeVectors(directory):
    print 'removing individual feature files (.npy)...'
    for file in os.listdir(directory):
        if file.endswith(".npy"):
            os.remove(directory+'/'+file)
            
#progress bar
def printProgress (iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 50):
    formatStr       = "{0:." + str(decimals) + "f}"
    percents        = formatStr.format(100 * (iteration / float(total)))
    filledLength    = int(round(barLength * iteration / float(total)))
    bar             = '|' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()
