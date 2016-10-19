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
def extract(audiodirectory='../../../CS2108-Vine-Dataset/vine/validation/audio',type= 'valid',processes=6):
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
    print 'audio features extracted successfully'

#Concatenates all arrays in the folder
def concatall(directory,output):
    files = []
    temp = output[:-4]+'temp.npy'
    for file in os.listdir(directory):
        files.append(directory+'/'+file)
    print
    print 'concatenating all files...'
    for i in range(len(files)-1):
        print 'merging '+str(i+1)+ ' of ' + str(len(files)-1)
        if i==0:
            concatenate(files[i],files[i+1],temp)
        elif i+1==len(files)-1:
            concatenate(temp,files[i+1], output)
            print 'removing temp files...'
            os.remove(temp)
        else:
            concatenate(temp,files[i+1],temp)
    print 'concatenation complete!'
    print

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
    print 'shortening files...'
    fitLength(38,directory,type+'_'+'spect'+'.npy','short')
    fitLength(38,directory,type+'_'+'mfcc'+'.npy','short')
    fitLength(38,directory,type+'_'+'energy'+'.npy','short')
    fitLength(38,directory,type+'_'+'zero'+'.npy','short')
    print 'done'
    
def lengthenAll(directory,type):
    print 'lengthening files...'
    fitLength(302,directory,type+'_'+'spect'+'.npy','long')
    fitLength(302,directory,type+'_'+'mfcc'+'.npy','long')
    fitLength(302,directory,type+'_'+'energy'+'.npy','long')
    fitLength(302,directory,type+'_'+'zero'+'.npy','long')
    print 'done'

# 1.shortens all features to shortest length and concatenate into 1D and
# outputs np.matrix (shape(3000,shortest length*k) where k is number of lines in feature vector
# eg. shorten(shortest feature length,'./','mfcc.npy','short')
def fitLength(fit,directory,file,mode):
    dict = np.load(directory+'/'+file).item()
    dict = collections.OrderedDict(sorted(dict.items()))
    
    isContiguous = dict.itervalues().next().flags['F_CONTIGUOUS']
    if(isContiguous): #eg. energy, zero
        result = []
        #extract array
        for line in dict: #for every feature vector in dictionary
            a = list(dict[line])
            b = list(dict[line])
            while(len(a)<fit):
                a = a + b #duplicate array to fit fit
            result.append(a[:fit]) #trim to length fit and add to array result
            del a
            del b
    
    else: #eg. mfcc, spectrum
        #initialise result array
        result = []
        
        #extract array
        i = 0
        for arr in dict:
            x = []
            for line in dict[arr]:
                a = list(line)
                b = list(line)
                while(len(a) < fit):
                    a = a + b
                x += (a[:fit]) #trim to fit
                del a
                del b
            #add concatenated array to result    
            result.append(x)
            del x
            printProgress (i, len(dict), 'Fitting to ' + str(fit), '', decimals = 1, barLength = 50)
            i+=1
    print
    directory+='/'+mode
    if not os.path.exists(directory):
        os.makedirs(directory)
    np.save(directory+'/'+file[:-4]+mode+'.npy',result)

    
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
    print
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
    print "done!"
    print
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
