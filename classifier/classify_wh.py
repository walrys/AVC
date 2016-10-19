import classify
import numpy as np

    
if __name__ == '__main__':
    type = 'emsz_short'
    train_energy = np.load('train_'+type+'.npy')
    valid_energy = np.load('valid_'+type+'.npy')
    train_gnd = np.load('train_gnd.npy')
    train_gnd = train_gnd[:,1]
    valid_gnd = np.load('valid_gnd.npy')
    valid_gnd = valid_gnd[:,1]

    venues = np.load('venues.npy')
    venues = venues[:,1]
    
    #STUFF WE NEED:
    dataset_train = train_energy
    dataset_train_label = train_gnd
    dataset_validation = valid_energy
    dataset_validation_label = valid_gnd
    dataset_label_names = venues


    classify.mySVM(dataset_train, dataset_train_label, dataset_validation, dataset_validation_label, dataset_label_names, './')