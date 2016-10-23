import SVM
import numpy as np
import classifier_utility.class_util as util

data_path = "../data"
np_output_path = "../data/results"
report_output_path = "../data/report"

# runs only for 1 set at a time
# valid set MUST be named test_ground.txt

if __name__ == '__main__':

    if (len(sys.argv) != 3):
        print "Please input: 1: test vector directory 2: test feature numpy name, "
    else:
        test_path = sys.argv[1]
        test_feature_name = sys.argv[1]

    # training set (stays the same)
    train_order = util.get_array_order(data_path + "/training_order.txt")
    train_gnd = util.get_labels_ordered(data_path + "/vine-venue-training.txt", train_order)


    # test / valid set (variable)
    test_order = util.get_array_order(test_path + "/test_order.txt")
    test_gnd = util.get_labels_ordered(test_path + "/test_ground.txt", validation_order)

    # venues (stays the same)
    venues = util.get_venue_list(data_path)

    # data needed for training
    X_train = np.load('/train_combined/multimodal_train_combined_features.npy')
    Y_train = train_gnd
    X_test = np.load(test_path + "/" + test_feature_name)
    Y_gnd = test_gnd

    SVM.batch_classify(X_train, Y_train, X_test, Y_gnd, venues, np_output_path + "/online_test_Y_predict.npy", report_output_path + "/online_test_report.txt")