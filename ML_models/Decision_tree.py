from sklearn import tree
import graphviz
from load_data import *


def plot_tree(clf, name):
    dot_data = tree.export_graphviz(clf, out_file=None)
    graph = graphviz.Source(dot_data)
    graph.render(name)


def dt(working_directory, filename, columns, question, name, max_depth=None, cross_validation_folds=5, render_tree=False, classify_maybe_as=None):
    data_X, data_y = load_data(working_directory, filename, columns, question, classify_maybe_as=classify_maybe_as)
    if max_depth:
        clf = tree.DecisionTreeClassifier(max_depth=max_depth)
    else:
        clf = tree.DecisionTreeClassifier()
    clf = clf.fit(data_X, data_y)
    scores = cross_validation(clf, data_X, data_y, cross_validation_folds, name)
    if render_tree:
        plot_tree(clf, name)
    return scores