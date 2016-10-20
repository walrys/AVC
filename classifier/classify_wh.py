import classify
import numpy as np
import classifier_utility.class_util as util

data_path = "../data"

if __name__ == '__main__':

    train_order = util.get_array_order(data_path + "/training_order.txt")
    validation_order = util.get_array_order(data_path + "/validation_order.txt")

    train_gnd = util.get_labels_ordered(data_path + "/vine-venue-training.txt", train_order)
    valid_gnd = util.get_labels_ordered(data_path + "/vine-venue-validation.txt", validation_order)

    type = 'emsz_short'
    train_energy = np.load(data_path + '/train_individual/train_'+type+'.npy')
    valid_energy = np.load(data_path + '/validation_individual/valid_'+type+'.npy')

    train_image = np.load(data_path + '/train_individual/train_image_feature.npy')

    venues = util.get_venue_list(data_path)
    
    #print venues

    #STUFF WE NEED:
    dataset_train = train_energy
    dataset_train_label = train_gnd
    dataset_validation = valid_energy
    dataset_validation_label = valid_gnd
    dataset_label_names = venues


    classify.batch_SVM(dataset_train, dataset_train_label, dataset_validation, dataset_validation_label, dataset_label_names)