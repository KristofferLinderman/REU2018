from sklearn import svm
from load_data import *


def svc(working_directory, filename, columns, question, name, cross_valudation_folds=5, C=1, kernel='rbf', classify_maybe_as=None):
    data_X, data_y = load_data(working_directory, filename, columns, question, classify_maybe_as=classify_maybe_as)
    clf = svm.SVC(C=C, kernel=kernel)
    return None
    for val in data_X.values():
        data_X1.append(list(val))
    data_X = list(np.transpose(data_X1))
    for row in data_X:
        print row
        print ''
    return None
    data_y = data_y[question]
    clf = clf.fit(data_X, data_y)
    scores = cross_validation(clf, data_X, data_y, cross_valudation_folds, name)
    return scores