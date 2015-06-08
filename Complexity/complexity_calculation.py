# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 18:48:28 2015

@author: roms

Complexity calculation script for scikit-learn classifiers
data source: http://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary.html
"""

# imports and parameters
import numpy as np
from datetime import datetime
from matplotlib import pyplot as plt
%matplotlib inline
from sklearn import linear_model, tree, ensemble
from sklearn.datasets import load_svmlight_files
dataTrainFile = '/home/roms/GitHub/ml-cheat-sheet/Complexity/data/madelon'
dataTestFile = '/home/roms/GitHub/ml-cheat-sheet/Complexity/data/madelon.t'
clf = linear_model.LogisticRegression()   # classifier to be tested
clf = tree.DecisionTreeClassifier(n_estimators=50)
n_samples_list = [1000, 1400, 1700, 2000]
n_features_list = [100, 200, 300, 400, 500]

# functions
def plotComplexity(x, y, title):
    n = 0
    plt.plot(x, y)
    plt.plot(x, (y[n] / (x[n] * np.log(x[n]))) * np.array(x) * np.log(x))
    plt.plot(x, (y[n] / x[n]) * np.array(x))
    plt.plot(x, (y[n] / np.log(x[n])) * np.log(x))
    plt.xlabel('Complexity')
    plt.ylabel('Time')
    plt.title(title)
    plt.legend(['runtime', 'n log(n)', 'n', 'log(n)'], loc=2)
    plt.show()

def getTime(clf, X_train, y_train, n_samples_list=[-1], n_features_list=[-1]):
    '''
        Returns running time for training and prediction tasks of a classifier.
        n_samples_list: list of the different number of samples to use (-1 = all)
        n_features_list: list of the different number of features to use (-1 = all)
    '''
    training_times_samples = []
    training_times_features = []
    prediction_times_samples = []
    prediction_times_features = []
    # calculating runtimes
    for n_samples in n_samples_list:
        n_samples = np.random.choice(list(range(X_train.shape[0])), n_samples)
        # fitting
        start = datetime.now()
        clf.fit(X_train[n_samples, :], y_train[n_samples])
        end = datetime.now()
        training_times_samples.append((end - start).seconds + \
        (end - start).microseconds / 1000000)
        # prediction
        start = datetime.now()
        clf.predict(X_train[n_samples, :])   # predicting on X_train
        end = datetime.now()
        prediction_times_samples.append((end - start).seconds + \
        (end - start).microseconds / 1000000)
    for n_features in n_features_list:
        n_features = np.random.choice(list(range(X_train.shape[1])), n_features)
        # fitting
        start = datetime.now()
        clf.fit(X_train[:, n_features], y_train)
        end = datetime.now()
        training_times_features.append((end - start).seconds + \
        (end - start).microseconds / 1000000)
        # prediction
        start = datetime.now()
        clf.predict(X_train[:, n_features])   # predicting on X_train
        end = datetime.now()
        prediction_times_features.append((end - start).seconds + \
        (end - start).microseconds / 1000000)
    # plotting results
    plotComplexity(n_samples_list, training_times_samples,
                   'Training complexity = f (sample size)')
    plotComplexity(n_samples_list, prediction_times_samples,
                   'Prediction complexity = f (sample size)')
    plotComplexity(n_features_list, training_times_features,
                   'Training complexity = f (features size)')
    plotComplexity(n_features_list, prediction_times_features,
                   'Prediction complexity = f (features size)')

# loads data and run the tests
X_train, y_train, X_test, y_test = \
    load_svmlight_files((dataTrainFile, dataTestFile))
X_train = X_train.todense()
X_test = X_test.todense()
getTime(clf, X_train, y_train, n_samples_list=n_samples_list,
        n_features_list=n_features_list)
