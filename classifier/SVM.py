
import numpy as np
import csv
import classifier_utility.class_util as util
from sklearn import svm
from sklearn.metrics import classification_report

feature_store_path = "../data"
video_store_path = "../data"

# X_train -> array of feature vectors for training machine learning (ML) model
# Y_train -> array of corrosponding correct labels to X_train
# X_test -> array of feature vectors for validating ML model
# Y_gnd_truth -> array of corrosponding correct labels to X_test
# label_names -> array of label names (aka categories) for each integer in X_train and Y_gnd_truth

def batch_SVM(X_train_array, Y_train_array, X_test_array, Y_gnd_truth_array, label_names_array, np_output_path, text_output_path):

    # 1. Convert (some) input array into numpy matrices
    X_train = np.asmatrix(X_train_array)
    Y_train = Y_train_array

    X_test  = np.asmatrix(X_test_array)
    Y_gnd_truth = Y_gnd_truth_array

    label_names = label_names_array
    print('Data Load Done.')

    # 2. Generate the predicted label matrix Y_predicted for X_test via SVM or other classifiers.
    #instance_num, class_num = len(label_validate)

    Y_predicted = []
    for i in xrange(len(Y_gnd_truth)):
        Y_predicted.append(0)

    #print data_train
    #print label_train

    #print data_train
    #print label_train

    #print data_validate
    #print label_validate

    # 3. Train the classifier.
    model = svm.SVC(kernel='linear', degree=3, gamma='auto', shrinking=True, verbose=False, max_iter=-1)
    model.fit(X_train, Y_train)

    # should give labels in theory
    Y_predicted = model.predict(X_test)
    print('SVM Train Done.')

    #print Y_predicted
    # 5. Save the predicted results and ground truth.
    #sio.savemat(output_path, {'Y_predicted': Y_predicted, 'Y_gnd': Y_gnd})
    print Y_predicted
    np.save(np_output_path, Y_predicted)

    report = classification_report(Y_gnd_truth, Y_predicted, target_names=label_names)
    print report

    with open(text_output_path, 'w') as writer:
        writer.write(report)
        
    return Y_predicted

# takes a single feature vector, X_test_array and finds the predicted class
# returns an integer corrosponding to the predicted class

def single_SVM(X_train_array, Y_train_array, X_test_array):
    X_train = np.asmatrix(X_train_array)
    Y_train = Y_train_array

    X_test  = np.asmatrix(X_test_array)

    model = svm.SVC(kernel='rbf', degree=3, gamma='auto', shrinking=True, verbose=False, max_iter=-1)
    model.fit(X_train, Y_train)

    Y_predicted = model.predict(X_test)

    return Y_predicted