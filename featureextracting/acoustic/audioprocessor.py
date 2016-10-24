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

def extractQuery(audiodirectory='./temp/wav/19.mp4', type= 'test',processes=1):
    # 1. extract all feature files into directory
    extractor.extract(audiodirectory)
    # 2. combine all feature files into feature dictionary
    collateall('./temp/npy',type)
    
    audiodirectory += '/'+type
    
    # 5. pad zeros to features to match longest file and concatenate to get final array
    padAll('./temp/npy',type)
    concatall('./temp/npy'+'/zeropad/','./temp/npy/'+type+'_ms_'+'zeropad.npy')    
    removeNPY('./temp/npy')
    print 'audio features extracted successfully'
    
def extract(audiodirectory='./batch', type= 'test',processes=1):
    # 1. extract all feature files into directory
    # WARNING: TAKES AT LEAST 10 MINUTES
    
    extractor.extractAll(audiodirectory+'/wav',processes)
    # 2. combine all feature files into feature dictionary
    collateall(audiodirectory+'/npy',type)
    # 3. remove feature vector files
    
    # 4. shorten features to match shortest file and concatenate to get final array
    #shortenAll(audiodirectory,type)
    #concatall(audiodirectory+'/short/',audiodirectory+'/short/'+type+'_emsz_'+'short.npy')
    
    # 5. lengthen features to match longest file and concatenate to get final array
    #lengthenAll(audiodirectory,type)
    #concatall(audiodirectory+'/long/',audiodirectory+'/long/'+type+'_emsz_'+'long.npy')
    
    # 5. pad zeros to features to match longest file and concatenate to get final array
    padAll(audiodirectory+'/npy',type)
    concatall(audiodirectory+'/npy'+'/zeropad/',audiodirectory+'/npy/'+type+'_ms_'+'zeropad.npy')
    removeNPY(audiodirectory+'/npy')
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
        if len(files) == 2 :
            concatenate(files[i],files[i+1],output)
        elif i==0:
            concatenate(files[i],files[i+1],temp)
        elif i+1==len(files)-1:
            concatenate(temp,files[i+1], output)
            print 'removing temp files...'
            os.remove(temp)
        else:
            concatenate(temp,files[i+1],temp)
    print 'concatenation complete!'
    print output
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
    
def padAll(directory,type):
    print 'padding files...'
    padZeros(302,directory,type+'_'+'spect'+'.npy')
    padZeros(302,directory,type+'_'+'mfcc'+'.npy')
    #padZeros(302,directory,type+'_'+'energy'+'.npy')
   # padZeros(302,directory,type+'_'+'zero'+'.npy')
    print 'done'

    
def padZeros(fit,directory,file):
    dict = np.load(directory+'/'+file).item()
    dict = collections.OrderedDict(sorted(dict.items()))
    mode = 'zeropad'
    
    isContiguous = dict.itervalues().next().flags['F_CONTIGUOUS']
    if(isContiguous): #eg. energy, zero
        result = []
        #extract array
        for line in dict: #for every feature vector in dictionary
            a = list(dict[line])
            while(len(a)<fit):
                a = a + [0] #pad with zeros
            result.append(a[:fit]) #trim to length fit and add to array result
            del a
    
    else: #eg. mfcc, spectrum
        #initialise result array
        result = []
        
        #extract array
        i = 0
        for arr in dict:
            x = []
            for line in dict[arr]:
                a = list(line)
                while(len(a) < fit):
                    a = a + [0]
                x += (a[:fit]) #trim to fit
                del a
            #add concatenated array to result    
            result.append(x)
            del x
            printProgress (i, len(dict), 'Padding with zeros to fit ' + str(fit), '', decimals = 1, barLength = 30)
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
            filename = file.replace("_"+featuretype+".npy","")
            array = np.load(directory+'/'+file)
            dict[filename] = array
        counter+=1
        printProgress(counter, foldersize, prefix = featuretype+':', suffix = '', decimals = 2, barLength = 50)
    print
    dict = collections.OrderedDict(sorted(dict.items()))
    #directory += '/'+type
    if not os.path.exists(directory):
        os.makedirs(directory)
    np.save(directory+'/'+type+'_'+featuretype+'.npy',dict)
    

def collateall(directory = './', type = 'train'):
    #collate("energy",type,directory)
    collate("mfcc",type,directory)
    collate("spect",type,directory)
    #collate("zero",type,directory)
    
def removeNPY(directory):
    print 'removing individual feature files (.npy)...'
    print "done!"
    print
    for file in os.listdir(directory):
        if not file.endswith("zeropad.npy"):
            if os.path.isfile(directory+'/'+file):
                os.remove(directory+'/'+file)
    
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
    
if __name__ == '__main__':
    if (len(sys.argv) != 2):
        print "Missing arguments Please input mp4 path"
    elif (not os.path.exists(sys.argv[1])):
        print "Please input valid mp4 path"
    else:
        audio_path = sys.argv[1]
        extractQuery(audio_path)
