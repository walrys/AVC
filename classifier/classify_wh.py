import classify
import numpy as np


def arrtodict(array):
    dict = {}
    for item in array:
        dict[str(item[0])] = item[1].ravel()
        
    return dict

def dicttoarray(dict):
    array  = []
    for item in dict:
        x = []
        for line in dict[item]:
            print len(line)
            #x.append(line[:37])
        x = x.ravel()
        array.append(x)
        
    return array
    
if __name__ == '__main__':
    type = 'energy'
    train_energy = np.load('train_'+type+'.npy').item()
    valid_energy = np.load('valid_'+type+'.npy').item()
    train_gnd = np.load('train_gnd.npy')
    train_gnd = train_gnd[:,1]
    valid_gnd = np.load('valid_gnd.npy')
    valid_gnd = valid_gnd[:,1]

    venues = np.load('venues.npy')
    venues = venues[:,1]

    #give it an array
    '''
    dataset_train = [[1,2,3,4,5,1],[1,2,3,4,5,1],[1,2,3,4,5,1],[1,2,3,4,5,1],[1,2,3,4,5,1]]
    dataset_validation = [[1,2,3,4,5,1],[1,2,3,4,5,1],[1,2,3,4,5,1],[1,2,3,4,5,1],[1,2,3,4,5,1]]
    dataset_train_label   = [1,2,3,4,5]
    dataset_validation_label   = [1,2,3,4,5]
    dataset_label_names = ['one','two','three','four','five']
    '''
    #STUFF WE NEED:
    dataset_train = dicttoarray(train_energy)
    dataset_train_label = train_gnd
    dataset_validation = dicttoarray(valid_energy)
    dataset_validation_label = valid_gnd
    dataset_label_names = venues


    classify.mySVM(dataset_train, dataset_train_label, dataset_validation, dataset_validation_label, dataset_label_names, './')