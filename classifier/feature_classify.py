import SVM
import numpy as np
import classifier_utility.class_util as util

data_path = "../data"
np_output_path = "../data/results"
report_output_path = "../data/report"


if __name__ == '__main__':

    #ground truth unordered
    train_order = util.get_array_order(data_path + "/training_order.txt")
    validation_order = util.get_array_order(data_path + "/validation_order.txt")

    #ground truths
    train_gnd = util.get_labels_ordered(data_path + "/vine-venue-training.txt", train_order)
    valid_gnd = util.get_labels_ordered(data_path + "/vine-venue-validation.txt", validation_order)

    # venues
    venues = util.get_venue_list(data_path)

    #sound features
    acoustic_names = ['emsz_zeropad', 'energyzeropad', 'mfcczeropad', 'spectzeropad', 'zerozeropad']
    
    #for name in acoustic_names:
    type = acoustic_names[1]
    train_acoustic = np.load(data_path + '/train_individual/train_'+type+'.npy')
    valid_acoustic = np.load(data_path + '/validation_individual/valid_'+type+'.npy')
    #SVM.batch_SVM(train_acoustic, train_gnd, valid_acoustic, valid_gnd, venues, np_output_path + "/" + type + "_Y_predict.npy", report_output_path + "/" + type + "_report.txt")
    SVM.single_classifier_method(train_acoustic, train_gnd, valid_acoustic, valid_gnd, venues, np_output_path + "/" + type, report_output_path + "/" + type)


    #image features
    #train_image = np.load(data_path + '/train_individual/train_image_feature.npy')
    #valid_image = np.load(data_path + '/validation_individual/valid_image_feature.npy')

    #combined features
    #train_combined = np.load(data_path + '/train_combined/train_combined_feature.npy')
    #valid_combined = np.load(data_path + '/validation_combined/valid_combined_feature.npy')

    
    #print venues

    #STUFF WE NEED:

    #SVM.batch_SVM(train_image, train_gnd, valid_image, valid_gnd, venues, np_output_path + "/image_Y_predict.npy", report_output_path + "/image_report.txt")

    #SVM.batch_SVM(train_combined, train_gnd, valid_combined, valid_gnd, venues, np_output_path + "/combined_Y_predict.npy", report_output_path + "/combined_report.txt")
