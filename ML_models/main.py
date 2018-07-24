from load_data import *
from Decision_tree import *
from random_forest import *
from SVC import *
from tabulate import tabulate

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


def ablation(working_direction, filename, question):
    feature_set = features
    scores = []

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
            svc_score = format_score(svc(working_direction, filename, temp_all_features, question, name))
            if float(svc_score[0:3]) > float(worst_feature[0:3]):
                worst_feature = svc_score
                best_feature_set = temp_feature_set
                best_name = name

        feature_set = best_feature_set
        scores.append([best_name, worst_feature])

    return scores


def train_models(working_directory):
    scores = [['Decision tree'], ['Random forest'], ['SVC']]

    for filename in filenames:
        dt_score = dt(working_directory, filename, all_columns_min_max_avg, questions[0], 'Decision tree', 3)
        rf_score = rf(working_directory, filename, all_columns_min_max_avg, questions[0], 'Random forest')
        svc_score = svc(working_directory, filename, all_columns_min_max_avg, questions[0], 'SVC')
        scores[0].append(format_score(dt_score))
        scores[1].append(format_score(rf_score))
        scores[2].append(format_score(svc_score))
    return scores


def main():
    config = load_config()
    working_directory = config['DATA_DIRECTORY']
    #model_results = train_models(working_directory)
    #print tabulate(model_results, headers=header, tablefmt='orgtbl')
    for i in range(len(filenames)):
        results = ablation(working_directory, filenames[i], questions[0])
        print '\n\n'
        print tabulate(results, headers=['Classifier features for ' + filenames[i] + ' ,' + questions[0], 'Score'], tablefmt='orgtbl')


if __name__ == "__main__":
    main()