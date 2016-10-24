import classifier.SVM
#from sklearn import svm
import numpy as np
import classifier.SVM as SVM
import classifier.classifier_utility.class_util as util
import featureextracting.acoustic.audioprocessor as ap
import preprocessing.extract_audio as ppa
from sklearn.externals import joblib
from sklearn.metrics import classification_report
import os
data_path = "./data"
np_output_path = "./data/results"
report_output_path = "./data/report"

# runs only for 1 set at a time
# valid set MUST be named test_ground.txt


def generateVideoOrder():
    input_path = './batch/wav'
    filename = data_path+"/test_order.txt"

    count = 0
    folderlist = os.listdir(input_path)

    with open(filename, 'w') as writer:
        for i in xrange(len(folderlist)):
            if (i!=len(folderlist)-1 and folderlist[i].endswith(".wav")):
                writer.write(folderlist[i][:-4] + "\n")
                count += 1
            elif(folderlist[i].endswith(".wav")):
                writer.write(folderlist[i][:-4])
                count += 1

    print count
    print "done!"

if __name__ == '__main__':
    
    # extract audio files
    ppa.batchAudioExtract('./batch','./batch/wav')
    
    # extract audio features
    ap.extract('./batch','valid',6)
    
    generateVideoOrder()
    print 'video order generated'
    
    test_path = '/batch'

    # test / valid set (variable)
    test_order = util.get_array_order(data_path + "/test_order.txt")
    test_gnd = util.get_labels_ordered(data_path + "/test_ground.txt", test_order)

    # venues (stays the same)
    venues = util.get_venue_list(data_path)

    # data needed for training)
    print 'loading model...'
    model = joblib.load('ms_model.pkl')
    X_test = np.load('./batch/npy/valid_ms_zeropad.npy')
    print 'model loaded'
    print 'predicting values... (this might take a while)'
    Y_predict = SVM.predict(data_path, model, X_test)
    print "generating report..."
    report = classification_report(test_gnd, Y_predict, target_names=venues)
    print report