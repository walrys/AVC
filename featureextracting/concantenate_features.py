import os, sys
import features_util as util
import numpy as np

feature_store_path = "../data"

if __name__ == "__main__":

    # extract order of arrays
    train_order = util.get_array_order(feature_store_path + "/training_order.txt")
    validation_order = util.get_array_order(feature_store_path + "/validation_order.txt")

    #print train_order
    #print validation_order

    # order ground truth in training_order and validation order
    train_gnd_truth = util.get_labels_ordered(feature_store_path + "/vine-venue-training.txt", train_order)
    validation_gnd_truth = util.get_labels_ordered(feature_store_path + "/vine-venue-validation.txt", validation_order)

    #print train_gnd_truth
    #print validation_gnd_truth

    # for each feature, extract out vectors into 2D arrays according to order
    train_image = np.load(feature_store_path + "/train_individual/train_image_feature.npy")
    valid_image = np.load(feature_store_path + "/validation_individual/valid_image_feature.npy")

    #print train_image.shape
    print valid_image.shape

    type = 'emsz_short'
    train_energy = np.load(feature_store_path + '/train_individual/train_'+type+'.npy')
    valid_energy = np.load(feature_store_path + '/validation_individual/valid_'+type+'.npy')

    #print train_energy.shape
    print valid_energy.shape

    # concatenate features and save as npy
    #util.concatall(feature_store_path + "/train_individual", feature_store_path + "/train_combined")
    util.concatall(feature_store_path + "/validation_individual", feature_store_path + "/validation_combined")