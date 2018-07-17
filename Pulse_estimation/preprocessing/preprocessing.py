from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import re
import datetime
import os
import sys
from static_values import *
from load_survey import *
from trimming import *
import random

def load_sensor_data(working_directory, filename):
    '''
    Loads the sensor data from an iMotions file when it has been converted to a .csv

    :param filename: the path to the file
    :return: experiment_time - the time the experiment started as a datetime object
             df - a pandas dataframe containing the experiment sensor data
    '''
    os.chdir(working_directory)

    df = pd.read_csv(filename, nrows=4, header=None)  # read the four first rows, those contain the time
    res = re.search(r'\d\d\d\d\d\d\d\d \d\d:\d\d:\d\d.\d\d\d', df[0][3])  # separate the time from the rest of the string
    date = res.group()[0:8]
    time = res.group()[9::]
    experiment_time = datetime.datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]), int(time[0:2]), int(time[3:5]), int(time[6:8]), int(time[9:12]) * 1000)  # create a time object that represents when the experiment started
    df = pd.read_csv(filename, skiprows=5)  # read from row 5, then the headers will be automatically fixed
    return experiment_time, df


def find_timestamps(experiment_time, df):
    '''
    Finds the start and end timestamps for the different stimuli from the iMotions .csv file

    :param experiment_time: the time the experiment started as a datetime object
    :param df: a pandas dataframe containing the experiment sensor data
    :return: order - the order the stimuli was shown in the experiment
             timestamps - the start and end timestamps for each stimuli stored in a dictionary
    '''
    timestamps = {}
    current_stimuli = df['StimulusName'][0]
    start_time = int(experiment_time.strftime("%s")) * 1000 + int(df['Timestamp'][0])  # the timestamps are presented as milliseconds since experiment started
    order = []
    # Iterate over all the stimuli and extract the timestamps that define the start and stop time of each stimulus
    for i in range(len(df['StimulusName'])):
        if df['StimulusName'][i] == current_stimuli:
            continue
        end_time = int(experiment_time.strftime("%s")) * 1000 + int(df['Timestamp'][i - 1])
        timestamps[current_stimuli] = (start_time, end_time)
        if i < len(df['StimulusName']):
            start_time = end_time
        order.append(current_stimuli)  # keep track of the order that the stimuli was presented
        current_stimuli = df['StimulusName'][i]
    order.append(current_stimuli)
    end_time = int(experiment_time.strftime("%s")) * 1000 + int(df['Timestamp'][len(df['Timestamp']) - 1])
    timestamps[current_stimuli] = (start_time, end_time)
    return order, timestamps


def get_pulse_logs_for_subject(working_directory, subject_id):
    '''
    Retrieves the filenames for the pulse logs for a certain subject

    :param subject_id: the subject to get the pulse logs for
    :param working_directory: the directory containing the pulse log files
    :return: pulse_logs - a list of filenames for the different pulse estimation logs
    '''
    os.chdir(working_directory)
    pulse_logs = []
    for f in os.listdir(os.curdir):
        res = re.search('pulse_estimation_log_\d\d?_.*', f)  # find all files that are pulse_estimation logs
        if res:
            pulse_logs.append(res.group())  # put the filenames in a list
    pulse_logs = [filename for filename in pulse_logs if int(re.search('\d\d?_\d\d?', filename).group().split('_')[0]) == subject_id]  # if the file is for the current subject, save it otherwise discard it
    pulse_logs = sorted(pulse_logs, key=lambda filename: int(re.search('\d\d?_\d\d?', filename).group().split('_')[1]))  # sort the list numerically
    return pulse_logs


def rename_pulse_logs_for_subject(working_directory, subject_id, pulse_logs, order):
    '''
    Renames the pulse logs for a certain subject to their corresponding stimulus

    :param subject_id: the subjects id
    :param pulse_logs: a list of the filenames of the pulse logs for this subject
    :param order: the order the stimuli was presented to the subject
    :return: None
    '''
    os.chdir(working_directory)
    if len(pulse_logs) == 0:  # if the length is empty, the files either don't exist or they have already been renamed
        return
    n = 0
    for i in range(len(order)):
        if order[i] in stimuli:  # we only care about the videos, not the surveys and such
            os.rename(pulse_logs[n], 'pulse_' + order[i] + '_' + str(subject_id) + '.txt')
            n = n + 1


def calculate_characteristic(values):
    '''
    Calculates the characteristics we want

    :param values: The list of values to use in the calculation
    :return: minimum, maximum, average, median, standard deviation
    '''
    values = [float(val) for val in values]

    min_val = min(values)
    max_val = max(values)

    avg_val = float(sum(values)) / max(len(values), 1)

    median_val = np.median(values)
    standard_deviation_val = np.std(values)

    return min_val, max_val, avg_val, median_val, standard_deviation_val


def take_derivative_of_pulse(pulse_collection, pulse_time_collection):
    '''
    Takes the derivative of a matrix of pulse values

    :param pulse_collection: The matrix of pulse values, that is the pulse for a subject for all 15 videos
    :return: A matrix of the same size containing the derivative of the input
    '''
    pulse_derivative = []
    for i in range(len(pulse_collection)):
        pulse_derivative.append([0])
        for j in range(1, len(pulse_collection[i])):
            pulse_derivative[i].append(((pulse_collection[i][j] - pulse_collection[i][j - 1]) / (pulse_time_collection[i][j] - pulse_time_collection[i][j - 1])) * 1000)
    return pulse_derivative


def create_final_sheet_for_subject(working_directory, subject_id):
    '''
    Creates the final sheet for a subject

    :param subject_id: The subjects id
    :param working_directory: The directory containing the files needed
    :return: None
    '''
    os.chdir(working_directory)
    data_dict = {}
    data_dict['User'] = subject_id
    data_dict['Video'] = [i + 1 for i in range(15)]
    data_dict['Intended_emotion'] = [intended_emotions[int(i / 3)] for i in range(15)]

    # add a list for each feature
    for feature in features:
        for characteristic in characteristics:
            data_dict[feature + characteristic] = []

    for question in survey_questions.keys():
        data_dict[survey_questions[question]] = []

    # load the pulse data for a subject for all videos
    pulse_collection = []
    pulse_time_collection = []
    for i in range(15):
        pulse_collection.append(pd.read_csv('pulse_' + id_stimuli[i + 1] + '_' + str(subject_id) + '_trimmed.csv')['Pulse'])
        pulse_time_collection.append(pd.read_csv('pulse_' + id_stimuli[i + 1] + '_' + str(subject_id) + '_trimmed.csv')['Timestamp'])

    pulse_derivative_collection = take_derivative_of_pulse(pulse_collection, pulse_time_collection)

    pulse_derivative_abs_collection = []
    pulse_derivative_direction_collection = []
    for i in range(len(pulse_derivative_collection)):
        # create a list that is the absolute value for the derivative
        pulse_derivative_abs_collection.append([abs(val) for val in pulse_derivative_collection[i]])
        # create a list that is only -1/0/+1 for the derivative
        pulse_derivative_direction_collection.append([(val / (abs(val) if not val == 0 else 1)) for val in pulse_derivative_collection[i]])

    # put the pulse values in the data dictionary
    for i in range(15):
        characteristics_values = calculate_characteristic(pulse_derivative_collection[i])
        for j in range(5):
            data_dict['Pulse_derivative' + characteristics[j]].append(characteristics_values[j])

        characteristics_values = calculate_characteristic(pulse_derivative_abs_collection[i])
        for j in range(5):
            data_dict['Pulse_derivative_abs' + characteristics[j]].append(characteristics_values[j])

        characteristics_values = calculate_characteristic(pulse_derivative_direction_collection[i])
        for j in range(5):
            data_dict['Pulse_derivative_direction' + characteristics[j]].append(characteristics_values[j])

    # put the iMotions features in the data dictionary
    for column in relevant_final_columns:
        collection = []
        for i in range(15):
            instance = pd.read_csv(id_stimuli[i + 1] + '_' + str(subject_id) + '.csv')[column]
            instance = ([float(val) for val in instance if not np.isnan(val)])
            collection.append(instance)

        for i in range(15):
            characteristics_values = calculate_characteristic(collection[i])
            for j in range(5):
                data_dict[column + characteristics[j]].append(characteristics_values[j])

    answers = get_survey_answers_for_subject(working_directory, subject_id)
    for i in range(1, 16):
        answers_for_video = answers[id_stimuli[i]]
        for question in survey_questions.values():
            if question == 'What did you feel when watching the video?':
                Q3_answer = str(answers_for_video[question][0])
                if len(answers_for_video[question]) > 1:
                    for j in range(1, len(answers_for_video[question])):
                        Q3_answer = Q3_answer + ' ' + str(answers_for_video[question][j])
                data_dict[question].append(Q3_answer)
                continue
            data_dict[question].append(answers_for_video[question][0])

    # save the data as subject id.csv e.g '7.csv'
    pd.DataFrame(data_dict)[final_columns].to_csv(str(subject_id) + '.csv')


def organize(subject_id, main_filename):
    '''
    Organizes the files into a folder for the subject

    :param subject_id: the subjects id
    :return: None
    '''
    try:
        os.mkdir(str(subject_id))
        os.mkdir(str('final'))
    except:
        pass
    for stimulus in stimuli:
        os.system('mv pulse_' + stimulus.replace(' ', '\ ') + '_' + str(subject_id) + '.txt ' + str(subject_id))
        os.system('mv pulse_' + stimulus.replace(' ', '\ ') + '_' + str(subject_id) + '_trimmed.csv ' + str(subject_id))
        os.system('mv ' + stimulus.replace(' ', '\ ') + '_' + str(subject_id) + '.csv ' + str(subject_id))
        os.system('mv ' + main_filename + ' ' + str(subject_id))
        os.system('mv ' + str(subject_id) + '.csv final')
    try:
        os.chdir(str(subject_id))
        os.mkdir('pulse_files')
        os.mkdir('pulse_files_trimmed')
        os.mkdir('facial_files_trimmed')
    except:
        pass
    for stimulus in stimuli:
        os.system('mv pulse_' + stimulus.replace(' ', '\ ') + '_' + str(subject_id) + '.txt pulse_files')
        os.system('mv pulse_' + stimulus.replace(' ', '\ ') + '_' + str(subject_id) + '_trimmed.csv pulse_files_trimmed')
        os.system('mv ' + stimulus.replace(' ', '\ ') + '_' + str(subject_id) + '.csv facial_files_trimmed')


def create_master_sheet(working_directory):
    '''
    Creates a sheet which contains all data from all participants

    :param working_directory: The directory containing the final sheet for each participant
    :return: None
    '''
    os.chdir(working_directory)
    master_sheet = {}
    for column in final_columns:
        master_sheet[column] = []
    files = os.listdir('.')
    files = sorted(files, key=lambda file : int(file.replace('.csv', '')))
    for file in files:
        df = pd.read_csv(file)
        for column in final_columns:
            master_sheet[column].extend(df[column])
    pd.DataFrame(master_sheet)[final_columns].to_csv('master.csv')


def plot_data(datapoints):
    '''
    Plot a set of datapoints

    :param datapoints: the datapoints to plot in a list
    :return: None
    '''
    plt.plot(np.arange(0, len(datapoints)), datapoints)
    plt.show()


def load_config():
    config = {}
    with open('./preprocessing/config.txt', 'r') as f:
        for line in f:
            parts = line.replace('\n', '').split('=')
            config[parts[0]] = parts[1] if not parts[1] == '' else None
    print config
    return config

def preprocess():
    '''
    Preprocesses the data from the pulse estimation and iMotions
    - trims the pulse logs to match each stimulus
    - renames the pulse logs to it's corresponding stimulus

    :param working_directory: the directory containing the pulse logs and the iMotions sensor data
    :return: None
    '''

    config = load_config()

    excluded_subject = -1
    working_directory = config['DATA_DIRECTORY']

    os.chdir(working_directory)
    res = [re.search('\d\d\d_\d*', f) for f in os.listdir('.')]
    res = [r.group() for r in res if r]
    participants = max([int(r[0:3]) for r in res])

    if config['LEAVE_ONE_SUBJECT_OUT']:
        excluded_subject = random.randint(1, participants)

    for i in range(1, participants + 1):
        if i == 4 or i == 20 or i == 23 or i == 28 or excluded_subject:  # these have faulty pulse files
            continue
        print str(i) + '/' + str(participants)
        filename = ('0' + str(participants + 1 - i) + '_' + str(i) + '.csv')
        if (participants + 1 - i) < 10:
            filename = ('00' + str(participants + 1 - i) + '_' + str(i) + '.csv')
        print filename
        if filename in os.listdir('.'):
            experiment_time, df = load_sensor_data(working_directory, filename)
            order, timestamps = find_timestamps(experiment_time, df)
            pulse_logs = get_pulse_logs_for_subject(working_directory, i)
            rename_pulse_logs_for_subject(working_directory, i, pulse_logs, order)
            trim_pulse_log_for_stimulus(working_directory, i, timestamps)
            trim_facial_data(working_directory, i, df, experiment_time)
            # survey_duration = get_survey_duration(df)  # data already exist in timestamps
            create_final_sheet_for_subject(working_directory, i)
            organize(i, filename)
            os.chdir(working_directory)
        else:
            print 'data for participant ' + str(i) + ' is missing, skipping that participant'
            continue

    create_master_sheet(working_directory + 'final/')


if __name__ == "__main__":
    preprocess()