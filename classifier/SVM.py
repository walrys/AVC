
import numpy as np
import csv
import classifier_utility.class_util as util
from sklearn import svm
from sklearn.metrics import classification_report

feature_store_path = "../data"
video_store_path = "../data"

def create_model(search_path):
    X_train_array= np.load(search_path + '/train_combined/multimodal_train_combined_features.npy')
    train_order = util.get_array_order(search_path + "/training_order.txt")
    train_gnd = util.get_labels_ordered(search_path + "/vine-venue-training.txt", train_order)


    X_train = np.asmatrix(X_train_array)
    Y_train = train_gnd

    model = svm.SVC(kernel='linear', degree=3, gamma='auto', shrinking=True, verbose=False, max_iter=-1)
    model.fit(X_train, Y_train)

    print "model created!"
    return model

def predict(search_path, model, X_test_array):
    X_test  = np.asmatrix(X_test_array)
    validation_order = util.get_array_order(search_path + "/validation_order.txt")
    valid_gnd = util.get_labels_ordered(search_path + "/vine-venue-validation.txt", validation_order)

    Y_predicted = []
    for i in xrange(len(valid_gnd)):
        Y_predicted.append(0)

    Y_predicted = model.predict(X_test)

    return Y_predicted

def find_f1_score(final_predicted, Y_gnd_truth):
    # load features, find f1 score
    score = 0.0
    total = 0.0
    for i in xrange(len(Y_gnd_truth)):
        if (final_predicted[i] == -1):
            continue
        
        if final_predicted[i] == Y_gnd_truth[i]:
            score += 1.0

    recall = (score / total)
    precision = (score / len(Y_gnd_truth))

    if (recall+precision > 0):
        f1 = 2.0*(precision*recall)/(precision+recall)
    else:
        f1 = 0.0

    return recall, precision, f1

    # if equal, find a way to resolve

# assume number of features == 900 (for validation) and categories == 30
def find_common_categories(input_path):
    # this a array of all VIDEOS keep a list of common categories (those which have value 1)
    videos_list_of_common_categories = {}
    for i in xrange(900):
        videos_list_of_common_categories[i] = []

    for i in xrange(30):
        path = input_path + '/energyzeropad' + str(i) + "_Y_predict.npy"
        prediction = np.load(path) 
        for j in xrange(len(prediction)):
            if prediction[j] == 1:
                # saved is the category number each video has been predicted to be in
                videos_list_of_common_categories[j].append(i)

    print videos_list_of_common_categories

    return videos_list_of_common_categories

def single_classifier_method(X_train_array, Y_train_array, X_test_array, Y_gnd_truth_array, label_names_array, np_output_path, text_output_path):

    Y_train_class_dict = util.get_binary_classes(label_names_array, Y_train_array)
    Y_valid_class_dict = util.get_binary_classes(label_names_array, Y_gnd_truth_array)

    labels = [0, 1]
    #print Y_train_class
    #print Y_valid_class
    for i in xrange(len(label_names_array)):
        filename = "score_" + str(i+1) + ".txt"
        Y_predicted, decision_functions = batch_SVM(X_train_array, Y_train_class_dict[i+1], X_test_array, Y_valid_class_dict[i+1], labels, np_output_path + str(i), text_output_path + label_names_array[i] + "_report.txt")
        
        #recall, precision, f1 = find_f1_score(np_output_path + str(i) + "_Y_predict.npy", Y_valid_class_dict[i+1])
        #result = label_names_array[i] + ":\n" + "recall: " + str(recall) + "\n" + "precision: " + str(precision) + "\n" + "f1: " + str(f1) + "\n"
        
        #path_name = text_output_path + "_report.txt"
        #with open(path_name, 'a') as writer:
            #writer.write(result + "\n")

    final_predicted = []
    videos_list_of_common_categories = find_common_categories("../data/results")
    for vector_number, categories in videos_list_of_common_categories.iteritems():
        smallest_distance = -999999
        best_category = -1
        if len(categories) > 1:
            for i in categories:
                path = np_output_path + str(i) + "_decision_functions.npy"
                decision_functions = np.load(path)
                if abs(decision_functions[vector_number]) > smallest_distance:
                    best_category = i
                    smallest_distance = decision_functions[vector_number]    

        elif len(categories) == 1:
            best_category = categories[0]
        
        final_predicted.append(best_category)

    path_name = text_output_path + "_category.txt"
    with open(path_name, 'w') as writer:
        writer.write(final_predicted + "\n")
    
    recall, precision, f1 = find_f1_score(final_predicted, Y_gnd_truth_array)
    result = "recall: " + str(recall) + "\n" + "precision: " + str(precision) + "\n" + "f1: " + str(f1) + "\n"

    path_name = text_output_path + "_report.txt"

    with open(path_name, 'w') as writer:
        writer.write(result + "\n")

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
    #decision_functions = model.decision_function(X_test)
    print('SVM Train Done.')
    #for i in xrange(len(Y_predicted)):
        #Y_predicted[i] = int(round(Y_predicted[i]))

    # 5. Save the predicted results and ground truth.
    #sio.savemat(output_path, {'Y_predicted': Y_predicted, 'Y_gnd': Y_gnd})
    #print Y_predicted

    np.save(np_output_path + "_Y_predict.npy", Y_predicted)
    #np.save(np_output_path + "_decision_functions.npy", decision_functions)

    report = classification_report(Y_gnd_truth, Y_predicted, target_names=label_names)
    
    with open(text_output_path + "_report.txt", 'a') as writer:
        writer.write(report)
    
    #print report
    #decision_functions

# takes a single feature vector, X_test_array and finds the predicted class
# returns an integer corrosponding to the predicted class

def create_SVM(X_train_array, Y_train_array, X_test_array):
    X_train = np.asmatrix(X_train_array)
    Y_train = Y_train_array

    X_test  = np.asmatrix(X_test_array)

    model = svm.SVC(kernel='rbf', degree=3, gamma='auto', shrinking=True, verbose=False, max_iter=-1)
    model.fit(X_train, Y_train)

    return model