from load_data import *
from Decision_tree import *
from random_forest import *
from SVC import *
from tabulate import tabulate

questions = ['One a scale of 1 to 5, how would you rate the video?', 'Would you want to watch similar videos?']
filenames = ['master.csv']
data = []

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

def train_models(working_directory):
    data.append(['Decision tree',
                    format_score(dt(working_directory, filenames[0], all_columns_min_max_avg, questions[0], 'Decision tree', 3))])
    data.append(['Random forest',
                    format_score(rf(working_directory, filenames[0], all_columns_min_max_avg, questions[0], 'Random forest'))])
    data.append(['SVC',
                    format_score(svc(working_directory, filenames[0], all_columns_min_max_avg, questions[0], 'SVC'))])
    return data


def main():
    config = load_config()
    working_directory = config['DATA_DIRECTORY']
    model_results = train_models(working_directory)
    print '\n'
    print tabulate(model_results, headers=['Classifier', 'Score'], tablefmt='orgtbl')


if __name__ == "__main__":
    main()