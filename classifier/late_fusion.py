import os, sys
import classify.py as clf

# take multiple feature vectors, put into svm, apply weights and put into svm again
# X_trains_array and Y_trains_array is to be in this order:
# 0: sound
# 1: image
# 2: textual

def late_fusion_batch(X_trains_array, Y_train_array, X_tests_array, Y_gnd_truth_array, output_path):
	weighted_Y_predicted = []
	
	# 0: sound
	# 1: image
	# 2: textual
	Y_predicted_weights = [0.34, 0.33, 0.33]

	for i in xrange(len(X_trains_array)):
		X_train = X_trains_array[i]
		Y_train = Y_train_array
		X_test = X_tests_array[i]
		Y_gnd_truth = Y_gnd_truth_array

		Y_predicted = clf.batch_SVM(X_train, Y_train, X_test, Y_gnd_truth))
		weight = Y_predicted_weights[i]

		for j in xrange(len(Y_predicted)):
			if len(Y_predicted_round_1) > 0:
				weighted_Y_predicted[j] += (weight*Y_predicted[j]) 
			else:
				weighted_Y_predicted.append(weight*Y_predicted[j])

	# save the predicted values
	
	return weighted_Y_predicted

def single_late_fusion(X_train_array, Y_train_array, X_test_array):
	X_train = X_train_array
	Y_train = Y_train_array
	X_test = X_test_array

	Y_predicted = clf.single_SVM(X_train, Y_train, X_test)

	return Y_predicted

