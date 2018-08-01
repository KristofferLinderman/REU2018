from load_data import *
from Decision_tree import *
from random_forest import *
from SVC import *
from tabulate import tabulate
import datetime
from sklearn.dummy import DummyClassifier
from threading import Thread
import sys

questions = ['One a scale of 1 to 5, how would you rate the video?', 'Would you want to watch similar videos?']
filenames = ['master.csv', 'master_with_instances.csv', 'master_with_end_instances.csv']
header = ['Classifier', 'Score using entire video', 'Score using pulse as instances', 'Score using end as instance']
characteristics = ['_min', '_max', '_average', '_median', '_standard_deviation']
data_dict = {}

def load_config():
    config = {}
    with open('config.txt', 'r') as f:
        for line in f:
            parts = line.replace('\n', '').split('=')
            config[parts[0]] = parts[1] if not parts[1] == '' else None
    print config
    return config


def format_score(score):
    return "%0.2f (+/- %0.2f)" % (score.mean(), score.std() * 2)


def ablation_svc(working_direction, filename, question, config, C=1):
    feature_set = features
    scores = []
    all_features = []
    name = ''
    for f in feature_set:
        name = name + f + ' + '
    name = name[0:len(name) - 3]
    for feature in feature_set:
        for characteristic in characteristics:
            all_features.append(feature + characteristic)
    svc_score = format_score(svc(working_direction, filename, all_features, question, name, classify_maybe_as=config['CLASSIFY_MAYBE_AS']))
    scores.append([name, svc_score])

    while(len(feature_set) > 2):
        worst_feature = '0.00'
        print 'feature length: ' + str(len(feature_set)) + '\n'
        all_features = []

        for feature in feature_set:
            for characteristic in characteristics:
                all_features.append(feature + characteristic)

        for feature in feature_set:
            temp_feature_set = [f for f in feature_set if not feature == f]
            temp_all_features = []
            for f in temp_feature_set:
                for characteristic in characteristics:
                    temp_all_features.append(f + characteristic)
            name = ''
            for f in temp_feature_set:
                name = name + f + ' + '
            name = name[0:len(name) - 3]
            print 'removing feature: ' + feature
            svc_score = format_score(svc(working_direction, filename, temp_all_features, question, name, classify_maybe_as=config['CLASSIFY_MAYBE_AS']))
            if float(svc_score[0:3]) > float(worst_feature[0:3]):
                worst_feature = svc_score
                best_feature_set = temp_feature_set
                best_name = name

        feature_set = best_feature_set
        scores.append([best_name, worst_feature])

    return scores


def ablation_dt(working_direction, filename, question, config):
    feature_set = features
    scores = []
    all_features = []
    name = ''
    for f in feature_set:
        name = name + f + ' + '
    name = name[0:len(name) - 3]
    for feature in feature_set:
        for characteristic in characteristics:
            all_features.append(feature + characteristic)
    dt_score = format_score(dt(working_direction, filename, all_features, question, name, classify_maybe_as=config['CLASSIFY_MAYBE_AS']))
    scores.append([name, dt_score])

    while (len(feature_set) > 2):
        worst_feature = '0.00'
        print 'feature length: ' + str(len(feature_set)) + '\n'
        all_features = []

        for feature in feature_set:
            for characteristic in characteristics:
                all_features.append(feature + characteristic)

        for feature in feature_set:
            temp_feature_set = [f for f in feature_set if not feature == f]
            temp_all_features = []
            for f in temp_feature_set:
                for characteristic in characteristics:
                    temp_all_features.append(f + characteristic)
            name = ''
            for f in temp_feature_set:
                name = name + f + ' + '
            name = name[0:len(name) - 3]
            print 'removing feature: ' + feature
            dt_score = format_score(dt(working_direction, filename, temp_all_features, question, name, classify_maybe_as=config['CLASSIFY_MAYBE_AS']))
            if float(dt_score[0:3]) > float(worst_feature[0:3]):
                worst_feature = dt_score
                best_feature_set = temp_feature_set
                best_name = name

        feature_set = best_feature_set
        scores.append([best_name, worst_feature])

    return scores


def ablation_rf(working_direction, filename, question, config):
    feature_set = features
    scores = []
    all_features = []
    name = ''
    for f in feature_set:
        name = name + f + ' + '
    name = name[0:len(name) - 3]
    for feature in feature_set:
        for characteristic in characteristics:
            all_features.append(feature + characteristic)
    rf_score = format_score(rf(working_direction, filename, all_features, question, name, classify_maybe_as=config['CLASSIFY_MAYBE_AS']))
    scores.append([name, rf_score])

    while (len(feature_set) > 2):
        worst_feature = '0.00'
        print 'feature length: ' + str(len(feature_set)) + '\n'
        all_features = []

        for feature in feature_set:
            for characteristic in characteristics:
                all_features.append(feature + characteristic)

        for feature in feature_set:
            temp_feature_set = [f for f in feature_set if not feature == f]
            temp_all_features = []
            for f in temp_feature_set:
                for characteristic in characteristics:
                    temp_all_features.append(f + characteristic)
            name = ''
            for f in temp_feature_set:
                name = name + f + ' + '
            name = name[0:len(name) - 3]
            print 'removing feature: ' + feature
            rf_score = format_score(rf(working_direction, filename, temp_all_features, question, name, classify_maybe_as=config['CLASSIFY_MAYBE_AS']))
            if float(rf_score[0:3]) > float(worst_feature[0:3]):
                worst_feature = rf_score
                best_feature_set = temp_feature_set
                best_name = name

        feature_set = best_feature_set
        scores.append([best_name, worst_feature])

    return scores


def ablation(config, filename, question, cols, clf):
    feature_set = features
    scores = []
    all_features = []
    name = ''
    for f in feature_set:
        name = name + f + ' + '
    name = name[0:len(name) - 3]
    for feature in feature_set:
        for characteristic in characteristics:
            all_features.append(feature + characteristic)
    score = run_ML_leave_one_subject_out(config, filename, question, clf)
    scores.append([name, score[0], score[1], score[2]])

    while len(feature_set) > 2:
        worst_feature = [0.00, 0.00, 0.00]
        print 'feature length: ' + str(len(feature_set)) + '\n'
        all_features = []

        for feature in feature_set:
            for characteristic in characteristics:
                all_features.append(feature + characteristic)

        for feature in feature_set:
            temp_feature_set = [f for f in feature_set if not feature == f]
            temp_all_features = []
            for f in temp_feature_set:
                for characteristic in characteristics:
                    temp_all_features.append(f + characteristic)
            name = ''
            for f in temp_feature_set:
                name = name + f + ' + '
            name = name[0:len(name) - 3]
            print 'removing feature: ' + feature
            score = run_ML_leave_one_subject_out(config, filename, question, clf, temp_all_features)
            if score[0] > worst_feature[0]:
                worst_feature = score
                best_feature_set = temp_feature_set
                best_name = name

        feature_set = best_feature_set
        scores.append([best_name, worst_feature[0], worst_feature[1], worst_feature[2]])

    return scores


def threaded_ablation(config, filename, question, clf):
    feature_set = features
    scores = []
    all_features = []
    name = ''
    for f in feature_set:
        name = name + f + ' + '
    name = name[0:len(name) - 3]
    for feature in feature_set:
        for characteristic in characteristics:
            all_features.append(feature + characteristic)
    score = run_ML_leave_one_subject_out(config, filename, question, clf)
    scores.append([name, score[0], score[1], score[2]])

    while len(feature_set) > 2:
        worst_feature = [0.00, 0.00, 0.00]
        print 'feature length: ' + str(len(feature_set)) + '\n'
        all_features = []

        for feature in feature_set:
            for characteristic in characteristics:
                all_features.append(feature + characteristic)

        threads = [None] * len(feature_set)
        results = [None] * len(feature_set)
        names = [None] * len(feature_set)
        temp_feature_sets = [None] * len(feature_set)

        for i in range(len(feature_set)):
            feature = feature_set[i]
            temp_feature_set = [f for f in feature_set if not feature == f]
            temp_all_features = []
            for f in temp_feature_set:
                for characteristic in characteristics:
                    temp_all_features.append(f + characteristic)
            name = ''
            for f in temp_feature_set:
                name = name + f + ' + '
            names[i] = name[0:len(name) - 3]
            temp_feature_sets[i] = temp_feature_set
            print 'removing feature: ' + feature
            threads[i] = Thread(target=run_ML_leave_one_subject_out, args=(config, filename, question, clf, results, i))
            threads[i].start()
            #score = run_ML_leave_one_subject_out(config, filename, question, clf)

        for i in range(len(threads)):
            threads[i].join()

        for i in range(len(results)):
            if results[i][0] > worst_feature[0]:
                worst_feature = results[i]
                best_feature_set = temp_feature_sets[i]
                best_name = names[i]

        feature_set = best_feature_set
        scores.append([best_name, worst_feature[0], worst_feature[1], worst_feature[2]])

    return scores


def train_models(working_directory, config):
    scores = [['Decision tree'], ['Random forest'], ['SVC']]

    for filename in filenames:
        dt_score = dt(working_directory, filename, all_columns_min_max_avg, questions[1], 'Decision tree', 3, classify_maybe_as=config['CLASSIFY_MAYBE_AS'])
        rf_score = rf(working_directory, filename, all_columns_min_max_avg, questions[1], 'Random forest', classify_maybe_as=config['CLASSIFY_MAYBE_AS'])
        svc_score = svc(working_directory, filename, all_columns_min_max_avg, questions[1], 'SVC', classify_maybe_as=config['CLASSIFY_MAYBE_AS'])
        scores[0].append(format_score(dt_score))
        scores[1].append(format_score(rf_score))
        scores[2].append(format_score(svc_score))
    return scores


def main():
    config = load_config()
    working_directory = config['DATA_DIRECTORY']
    #model_results = train_models(working_directory, config)
    #print tabulate(model_results, headers=header, tablefmt='orgtbl')
    #pd.DataFrame(model_results, columns=['Clasifier', 'Score using entire video', 'Score using pulse as instances', 'Score using end as instance']).to_csv('test.csv')
    print 'start: ' + str(datetime.datetime.now())
    config_options = ['Yes', 'No', 'Half', 'Exclude', None]
    svc_C = [0.1, 1, 10, 100]
    for c in svc_C:
        for i in range(len(filenames)):
            for j in range(len(questions)):
                if j == 1:
                    for config_option in config_options:
                        config['CLASSIFY_MAYBE_AS'] = config_option
                        results = ablation_svc(working_directory, filenames[i], questions[j], config, C=c)
                        print '\n\n'
                        print tabulate(results, headers=['SVC (C=' + str(c) + ') Classifier features for ' + filenames[i] + ' ,' + questions[j] + ' CLASSIFY_MAYBE_AS=' + config_option if not config_option is None else 'None', 'Score'], tablefmt='orgtbl')
                        print datetime.datetime.now()
                        pd.DataFrame(results, columns=['SVC (C=' + str(c) + ') Classifier features for ' + filenames[i] + ' ,' + questions[j] + ' CLASSIFY_MAYBE_AS=' + config_option if not config_option is None else 'None','Score']).to_csv('SVC_C' + str(c) + '_' + filenames[i].replace('.csv', '') + '_' + questions[j] + '_' + config_option if not config_option is None else 'None' + '.csv')
                else:
                    results = ablation_svc(working_directory, filenames[i], questions[j], config, C=c)
                    print '\n\n'
                    print tabulate(results, headers=['SVC (C=' + str(c) + ') Classifier features for ' + filenames[i] + ' ,' + questions[j], 'Score'], tablefmt='orgtbl')
                    print datetime.datetime.now()
                    pd.DataFrame(results, columns=['SVC (C=' + str(c) + ') Classifier features for ' + filenames[i] + ' ,' + questions[j], 'Score']).to_csv('SVC_C' + str(c) + '_' + filenames[i].replace('.csv', '') + '_' + questions[j] + '.csv')

    for i in range(len(filenames)):
        for j in range(len(questions)):
            if j == 1:
                for config_option in config_options:
                    config['CLASSIFY_MAYBE_AS'] = config_option
                    results = ablation_dt(working_directory, filenames[i], questions[j], config)
                    print '\n\n'
                    print tabulate(results, headers=['Decision tree Classifier features for ' + filenames[i] + ' ,' + questions[j] + ' CLASSIFY_MAYBE_AS=' + config_option if not config_option is None else 'None' , 'Score'], tablefmt='orgtbl')
                    print datetime.datetime.now()
                    pd.DataFrame(results, columns=['Decision tree Classifier features for ' + filenames[i] + ' ,' + questions[j] + ' CLASSIFY_MAYBE_AS=' + config_option if not config_option is None else 'None', 'Score']).to_csv('Decision_tree_' + filenames[i].replace('.csv', '') + '_' + questions[j] + config_option if not config_option is None else 'None' + '.csv')
            else:
                results = ablation_dt(working_directory, filenames[i], questions[j], config)
                print '\n\n'
                print tabulate(results, headers=['Decision tree Classifier features for ' + filenames[i] + ' ,' + questions[j], 'Score'], tablefmt='orgtbl')
                print datetime.datetime.now()
                pd.DataFrame(results, columns=['Decision tree Classifier features for ' + filenames[i] + ' ,' + questions[j], 'Score']).to_csv('Decision_tree_' + filenames[i].replace('.csv', '') + '_' + questions[j] + '.csv')

    for i in range(len(filenames)):
        for j in range(len(questions)):
            if j == 1:
                for config_option in config_options:
                    config['CLASSIFY_MAYBE_AS'] = config_option
                    results = ablation_rf(working_directory, filenames[i], questions[j], config)
                    print '\n\n'
                    print tabulate(results, headers=['Random forest Classifier features for ' + filenames[i] + ' ,' + questions[j] + ' CLASSIFY_MAYBE_AS=' + config_option if not config_option is None else 'None', 'Score'], tablefmt='orgtbl')
                    print datetime.datetime.now()
                    pd.DataFrame(results, columns=['Random forest Classifier features for ' + filenames[i] + ' ,' + questions[j] + ' CLASSIFY_MAYBE_AS=' + config_option if not config_option is None else 'None', 'Score']).to_csv('Random_forest_' + filenames[i].replace('.csv', '') + '_' + questions[j] + config_option if not config_option is None else 'None' + '.csv')
            else:
                results = ablation_rf(working_directory, filenames[i], questions[j], config)
                print '\n\n'
                print tabulate(results, headers=['Random forest Classifier features for ' + filenames[i] + ' ,' + questions[j], 'Score'], tablefmt='orgtbl')
                print datetime.datetime.now()
                pd.DataFrame(results, columns=['Random forest Classifier features for ' + filenames[i] + ' ,' + questions[j], 'Score']).to_csv('Random_forest_' + filenames[i].replace('.csv', '') + '_' + questions[j] + '.csv')
    print 'end: ' + str(datetime.datetime.now())


def run_ML_leave_one_subject_out(config, filename, question, clf, cols, return_arr=None, return_index=-1):
    working_directory = config['DATA_DIRECTORY']
    data_X, data_y = load_data(working_directory, filename, cols, question)
    data = leave_one_subject_out(data_X, data_y, 'User')
    score = 0
    score_dummy_mf = 0
    score_dummy_sf = 0
    dummy_clf_mf = DummyClassifier('most_frequent')
    dummy_clf_sf = DummyClassifier('stratified')
    for (training_X, training_y), (testing_X, testing_y) in data:
        clf.fit(training_X, training_y)
        dummy_clf_mf.fit(training_X, training_y)
        dummy_clf_sf.fit(training_X, training_y)

        single_score = clf.score(testing_X, testing_y)
        single_score_dummy_mf = dummy_clf_mf.score(testing_X, testing_y)
        single_score_dummy_sf = dummy_clf_sf.score(testing_X, testing_y)
        #print 'Single run score: ' + ("%0.2f" % single_score.mean())
        #print 'Single run score (dummy most frequent): ' + ("%0.2f" % single_score_dummy_mf.mean())
        #print 'Single run score (dummy stratified): ' + ("%0.2f" % single_score_dummy_sf.mean())

        score = score + single_score.mean()
        score_dummy_mf = score_dummy_mf + single_score_dummy_mf.mean()
        score_dummy_sf = score_dummy_sf + single_score_dummy_sf.mean()
    score = round(float(score / len(data)), 2)
    score_dummy_mf = round(float(score_dummy_mf / len(data)), 2)
    score_dummy_sf = round(float(score_dummy_sf / len(data)), 2)
    #print 'Total score: ' + str(score)
    #print 'Total score (dummy most frequent): ' + str(score_dummy_mf)
    #print 'Total score (dummy stratified): ' + str(score_dummy_sf)
    if return_index == -1:
        return score, score_dummy_mf, score_dummy_sf
    else:
        return_arr[return_index] = (score, score_dummy_mf, score_dummy_sf)


def main_leave_one_out():
    config = load_config()
    scores = []
    print 'start:' + str(datetime.datetime.now())
    for j in range(len(filenames)):
        for k in range(len(questions)):
            clf = svm.SVC(C=1, kernel='rbf')
            print str(datetime.datetime.now()) + '\tSVM ablation ' + str(k + 1) + '/' + str(len(questions)) + ' for file ' + str(j + 1) + '/' + str(len(filenames)) + '\n'
            ablation_score = ablation(config, filenames[j], questions[k], clf)
            for score in ablation_score:
                scores.append(['SVM', filenames[j], questions[k], score[0], score[1], score[2], score[3]])

    print tabulate(scores, headers=['Classifier', 'Data', 'question', 'Features', 'Score', 'Score dummy most frequent', 'Score dummy stratified'], tablefmt='orgtbl')


    for j in range(len(filenames)):
        for k in range(len(questions)):
            clf = RandomForestClassifier()
            print '\nRandom forest ablation ' + str(k + 1) + '/' + str(len(questions)) + ' for file ' + str(j + 1) + '/' + str(len(filenames)) + '\n'
            ablation_score = ablation(config, filenames[j], questions[k], clf)
            for score in ablation_score:
                scores.append(['Random forest', filenames[j], questions[k], score[0], score[1], score[2], score[3]])

    print tabulate(scores,headers=['Classifier', 'Data', 'question', 'Features', 'Score', 'Score dummy most frequent', 'Score dummy stratified'], tablefmt='orgtbl')

    cols = ['Classifier', 'Data', 'Question', 'Features', 'Score', 'Score_dummy_most_frequent', 'Score_dummy_stratified']
    results = {}
    for col in cols:
        results[col] = []
    for val in scores:
        for i in range(len(cols)):
            results[cols[i]].append(val[i])
    pd.DataFrame(results)[cols].to_csv('ml_models.csv')
    print 'end:' + str(datetime.datetime.now())


def test_leave_one_out():
    test_leave_one_out_method()
    return
    config = load_config()
    clf = svm.SVC(C=1, kernel='rbf')
    run_ML_leave_one_subject_out(config, 'master.csv', questions[1], clf)

    #results = ablation(config, 'master.csv', questions[1], clf)
    #print '\n\n'
    #print tabulate(results, headers=['SVC', 'Score'], tablefmt='orgtbl')


def main_best_classifiers():
    config = load_config()
    scores = []
    clf = RandomForestClassifier()
    #run_ML_leave_one_subject_out(config, 'master.csv', '')


def main_leave_one_out_one():
    config = load_config()
    config['DATA_DIRECTORY'] = config['DATA_DIRECTORY'] + 'iter_one/'
    scores = []
    print 'start:' + str(datetime.datetime.now())
    for j in range(len(filenames)):
        question = questions[0]
        clf = svm.SVC(C=1, kernel='rbf')
        print str(datetime.datetime.now()) + '\tSVM ablation for file ' + str(j + 1) + '/' + str(len(filenames)) + '\n'
        ablation_score = ablation(config, filenames[j], question, all_columns_all_characteristics, clf)
        for score in ablation_score:
            scores.append(['SVM', filenames[j], question, score[0], score[1], score[2], score[3]])

    for j in range(len(filenames)):
        question = questions[0]
        clf = RandomForestClassifier()
        print '\nRandom forest ablation for file ' + str(j + 1) + '/' + str(len(filenames)) + '\n'
        ablation_score = ablation(config, filenames[j], question, all_columns_all_characteristics, clf)
        for score in ablation_score:
            scores.append(['Random forest', filenames[j], question, score[0], score[1], score[2], score[3]])

    cols = ['Classifier', 'Data', 'Question', 'Features', 'Score', 'Score_dummy_most_frequent',
            'Score_dummy_stratified']
    results = {}
    for col in cols:
        results[col] = []
    for val in scores:
        for i in range(len(cols)):
            results[cols[i]].append(val[i])
    pd.DataFrame(results)[cols].to_csv('ml_models_1.csv')
    print 'end:' + str(datetime.datetime.now())


def main_leave_one_out_two():
    config = load_config()
    config['DATA_DIRECTORY'] = config['DATA_DIRECTORY'] + 'iter_two/'
    scores = []
    print 'start:' + str(datetime.datetime.now())
    for j in range(len(filenames)):
        question = questions[1]
        clf = svm.SVC(C=1, kernel='rbf')
        print str(datetime.datetime.now()) + '\tSVM ablation for file ' + str(j + 1) + '/' + str(len(filenames)) + '\n'
        ablation_score = ablation(config, filenames[j], question, all_columns_all_characteristics, clf)
        for score in ablation_score:
            scores.append(['SVM', filenames[j], question, score[0], score[1], score[2], score[3]])

    for j in range(len(filenames)):
        question = questions[1]
        clf = RandomForestClassifier()
        print '\nRandom forest ablation for file ' + str(j + 1) + '/' + str(len(filenames)) + '\n'
        ablation_score = ablation(config, filenames[j], question, all_columns_all_characteristics, clf)
        for score in ablation_score:
            scores.append(['Random forest', filenames[j], question, score[0], score[1], score[2], score[3]])

    cols = ['Classifier', 'Data', 'Question', 'Features', 'Score', 'Score_dummy_most_frequent',
            'Score_dummy_stratified']
    results = {}
    for col in cols:
        results[col] = []
    for val in scores:
        for i in range(len(cols)):
            results[cols[i]].append(val[i])
    pd.DataFrame(results)[cols].to_csv('ml_models_2.csv')
    print 'end:' + str(datetime.datetime.now())


if __name__ == "__main__":
    choice = -1
    try:
        choice = int(sys.argv[1])
    except:
        if len(sys.argv) == 1:
            choice = -1
        else:
            raise ValueError('Invalid choice')
    if choice == 1:
        print 'Running main_leave_one_out_one'
        main_leave_one_out_one()
    elif choice == 2:
        print 'Running main_leave_one_out_two'
        main_leave_one_out_two()
    else:
        print 'Running main_leave_one_out'
        main_leave_one_out()
    #main()
    #main_leave_one_out()