from sklearn import svm
import os
import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score

wanted_columns = ['Pulse_derivative_min', 'Pulse_derivative_max', 'Pulse_derivative_average',
                  'Engagement_min', 'Engagement_max', 'Engagement_average',
                  'Attention_min', 'Attention_max', 'Attention_average',
                  'Valence_min', 'Valence_max', 'Valence_average',
                  'Anger_min', 'Anger_max', 'Anger_average',
                  'Sadness_min', 'Sadness_max', 'Sadness_average',
                  'Disgust_min', 'Disgust_max', 'Disgust_average',
                  'Joy_min', 'Joy_max', 'Joy_average',
                  'Surprise_min', 'Surprise_max', 'Surprise_average',
                  'Fear_min', 'Fear_max', 'Fear_average',
                  'Contempt_min', 'Contempt_max', 'Contempt_average']

wanted_columns_1 = ['Engagement_average',
                  'Attention_average',
                  'Valence_average',
                  'Anger_average',
                  'Sadness_average',
                  'Disgust_average',
                  'Joy_average',
                  'Surprise_average',
                  'Fear_average',
                  'Contempt_average']


def load_data(working_directory, filename, columns):
    os.chdir(working_directory)
    df = pd.read_csv(filename)
    data_X = []
    for column in columns:
        data_X.append((df[column]))
    data_X = np.transpose(data_X)
    data_y = list(df['One a scale of 1 to 5, how would you rate the video?'])

    return data_X, data_y


def cross_validation(clf, data_X, data_y, folds, name):
    scores = cross_val_score(clf, data_X, data_y, cv=folds)
    print(name + " Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))


def main_with_instances_removed_0_1():
    data_X, data_y = load_data('/home/gustaf/Downloads/17_july/data/final/', 'master_with_instances_removed_0.csv', wanted_columns_1)
    clf = svm.SVC()
    clf = clf.fit(data_X, data_y)
    cross_validation(clf, data_X, data_y, 5, 'With instances removed 0 only average')


def main_with_instances_1():
    data_X, data_y = load_data('/home/gustaf/Downloads/17_july/data/final/', 'master_with_instances.csv', wanted_columns_1)
    clf = svm.SVC()
    clf = clf.fit(data_X, data_y)
    cross_validation(clf, data_X, data_y, 5, 'With instances only average')


def main_1():
    data_X, data_y = load_data('/home/gustaf/Downloads/17_july/data/final/', 'master.csv', wanted_columns_1)
    clf = svm.SVC()
    clf = clf.fit(data_X, data_y)
    cross_validation(clf, data_X, data_y, 5, 'Ordinary only average')


def main_with_instances_removed_0_linear():
    data_X, data_y = load_data('/home/gustaf/Downloads/17_july/data/final/', 'master_with_instances_removed_0.csv', wanted_columns)
    clf = svm.LinearSVC(C=1)
    clf = clf.fit(data_X, data_y)
    cross_validation(clf, data_X, data_y, 5, 'With instances removed 0 (Linear)')


def main_with_instances_removed_0_C01():
    data_X, data_y = load_data('/home/gustaf/Downloads/17_july/data/final/', 'master_with_instances_removed_0.csv', wanted_columns)
    clf = svm.SVC(C=0.1)
    clf = clf.fit(data_X, data_y)
    cross_validation(clf, data_X, data_y, 5, 'With instances removed 0 (C=0.1)')


def main_with_instances_removed_0():
    data_X, data_y = load_data('/home/gustaf/Downloads/17_july/data/final/', 'master_with_instances_removed_0.csv', wanted_columns)
    clf = svm.SVC(kernel='poly')
    clf = clf.fit(data_X, data_y)
    cross_validation(clf, data_X, data_y, 5, 'With instances removed 0 (C=1)')


def main_with_instances_removed_0_C10():
    data_X, data_y = load_data('/home/gustaf/Downloads/17_july/data/final/', 'master_with_instances_removed_0.csv', wanted_columns)
    clf = svm.SVC(C=10)
    clf = clf.fit(data_X, data_y)
    cross_validation(clf, data_X, data_y, 5, 'With instances removed 0 (C=10)')


def main_with_instances_removed_0_C100():
    data_X, data_y = load_data('/home/gustaf/Downloads/17_july/data/final/', 'master_with_instances_removed_0.csv', wanted_columns)
    clf = svm.SVC(C=100)
    clf = clf.fit(data_X, data_y)
    cross_validation(clf, data_X, data_y, 5, 'With instances removed 0 (C=100)')


def main_with_instances_removed_0_C10000():
    data_X, data_y = load_data('/home/gustaf/Downloads/17_july/data/final/', 'master_with_instances_removed_0.csv', wanted_columns)
    clf = svm.SVC(C=10000)
    clf = clf.fit(data_X, data_y)
    cross_validation(clf, data_X, data_y, 5, 'With instances removed 0 (C=10000)')


def main_with_instances():
    data_X, data_y = load_data('/home/gustaf/Downloads/17_july/data/final/', 'master_with_instances.csv', wanted_columns)
    clf = svm.SVC()
    clf = clf.fit(data_X, data_y)
    cross_validation(clf, data_X, data_y, 5, 'With instances')

def main():
    data_X, data_y = load_data('/home/gustaf/Downloads/17_july/data/final/', 'master.csv', wanted_columns)
    clf = svm.SVC()
    clf = clf.fit(data_X, data_y)
    cross_validation(clf, data_X, data_y, 5, 'Ordinary')


if __name__ == '__main__':
    #main()
    #main_with_instances()
    #main_with_instances_removed_0_C01()
    main_with_instances_removed_0()
    #main_with_instances_removed_0_C10()
    #main_with_instances_removed_0_C100()
    #main_with_instances_removed_0_C10000()
    #main_with_instances_removed_0_linear()
    #main_1()
    #main_with_instances_1()
    #main_with_instances_removed_0_1()