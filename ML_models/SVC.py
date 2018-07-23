from sklearn import svm
from load_data import *
from random_forest import *


def svc(working_directory, filename, columns, question, name, cross_valudation_folds=5, C=1, kernel='rbf'):
    data_X, data_y = load_data(working_directory, filename, columns, question)
    clf = svm.SVC(C=C, kernel=kernel)
    clf = clf.fit(data_X, data_y)
    scores = cross_validation(clf, data_X, data_y, cross_valudation_folds, name)
    return scores