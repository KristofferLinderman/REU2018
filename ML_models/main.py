from load_data import *
from Decision_tree import *
from random_forest import *
from SVC import *

questions = ['One a scale of 1 to 5, how would you rate the video?', 'Would you want to watch similar videos?']
filenames = ['master.csv', '']

def load_config():
    config = {}
    with open('config.txt', 'r') as f:
        for line in f:
            parts = line.replace('\n', '').split('=')
            config[parts[0]] = parts[1] if not parts[1] == '' else None
    print config
    return config


def train_models(working_directory):
    return

def main():
    config = load_config()
    return


if __name__ == "__main__":
    main()