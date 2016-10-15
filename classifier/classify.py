
import numpy as np
import csv
import classifier_utility.class_util as util
from sklearn import svm
from sklearn.metrics import classification_report

def extractFeature(csv_path):
    image_features = {}
    with open(csv_path, 'r') as reader:
        csv_reader = csv.reader(reader)
        
        for feature in csv_reader:
            keyword = feature.pop(0)
            #normalized distance
            image_features[keyword] = feature

    return image_features

def early_fusion(feature_vectors):
    pass

def dataset_toArray(data_train_dict):
    dataset_feature = []
    for name, vector in data_train_dict.iteritems():
        dataset_feature.append(vector)

    return dataset_feature

def label_toArray(data_train_dict, data_train_label_dict):
    dataset_label = []
    for name, vector in data_train_dict.iteritems():
        dataset_label.append(data_train_label_dict[name[:-4]])

    return dataset_label

# Train your own classifier.
# Here is the simple implementation of SVM classification.
def mySVM(dataset_train, dataset_train_label, dataset_validation, dataset_validation_label, output_path):

    # 1. dataset_train with instance_num * feature_num dimensions, and its corresponding venue labels label_train
    #    with instance_num * class_num dimensions.
    #    As well as X_test, and its label matrix Y_gnd.
    data_train = np.asmatrix(dataset_train)
    label_train = np.asmatrix(dataset_train_label)

    data_validate  = np.asmatrix(dataset_validation)
    label_validate = np.asmatrix(dataset_validation_label)
    print('Data Load Done.')

    # 2. Generate the predicted label matrix Y_predicted for X_test via SVM or other classifiers.
    instance_num, class_num = label_validate.shape

    Y_predicted = np.asmatrix(np.zeros([instance_num, class_num]))

    # 3. Train the classifier.
    model = svm.SVR(kernel='rbf', degree=3, gamma=0.1, shrinking=True, verbose=False, max_iter=-1)
    model.fit(data_train, label_train)
    Y_predicted = np.asmatrix(model.predict(data_validate))
    print('SVM Train Done.')

    print Y_predicted
    # 5. Save the predicted results and ground truth.
    #sio.savemat(output_path, {'Y_predicted': Y_predicted, 'Y_gnd': Y_gnd})


if __name__ == '__main__':
    # may put in args to indicate path
    
    # for each feature, extract out vectors into 2D arrays according to data_train_dict order
    data_train_dict = extractFeature("/Users/Brandon/Dropbox/NUS/Y3S1/CS2108/Lab/Assignment_2/Audio_Classifier/feature_csv/DL_image_training_features.csv")
    data_train_label_dict = util.get_video_category("/Users/Brandon/Documents/CS2108-Vine-Dataset", "vine-venue-training.txt")
    
    data_validation_dict = extractFeature("/Users/Brandon/Dropbox/NUS/Y3S1/CS2108/Lab/Assignment_2/Audio_Classifier/feature_csv/DL_image_validation_features.csv")
    data_validation_label_dict = util.get_video_category("/Users/Brandon/Documents/CS2108-Vine-Dataset", "vine-venue-validation.txt")

    #venue_label_dict = get_venue_list("/Users/Brandon/Dropbox/NUS/Y3S1/CS2108/Lab/Assignment_2/CS2108-Vine-Dataset")
    
    # combine features together (in early fusion) and pass to SVM
    dataset_train = dataset_toArray(data_train_dict)
    dataset_train_label = label_toArray(data_train_dict, data_train_label_dict)
    
    dataset_validation = dataset_toArray(data_validation_dict)
    dataset_validation_label = label_toArray(data_validation_dict, data_validation_label_dict)

    print dataset_train
    print dataset_train_label

    #print dataset_validation
    #print dataset_validation_label

    #mySVM(dataset_train, dataset_train_label, dataset_validation, dataset_validation_label, "/Users/Brandon/Dropbox/NUS/Y3S1/CS2108/Lab/Assignment_2/Audio_Classifier/feature_csv")