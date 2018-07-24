from load_data import *
from Decision_tree import *
from random_forest import *
from SVC import *
from tabulate import tabulate
import datetime

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

if __name__ == "__main__":
    main()