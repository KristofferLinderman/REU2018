from sklearn.ensemble import RandomForestClassifier
from load_data import *


def rf(working_directory, filename, columns, question, name, cross_validation_folds=5, n_estimators=10, max_depth=5, min_samples_split=2, random_state=0, classify_maybe_as=None):
    data_X, data_y = load_data(working_directory, filename, columns, question, classify_maybe_as=classify_maybe_as)
    clf = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, min_samples_split=min_samples_split, random_state=random_state)
    clf.fit(data_X, data_y)
    scores = cross_validation(clf, data_X, data_y, cross_validation_folds, name)
    return scores