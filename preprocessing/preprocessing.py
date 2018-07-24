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

    if len(values) == 0:
        return 0, 0, 0, 0, 0

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


def take_derivative_of_pulse_for_video(pulse_collection, pulse_time_collection):
    pulse_derivative = [0]
    for i in range(1, len(pulse_collection)):
        pulse_derivative.append(((pulse_collection[i] - pulse_collection[i - 1]) / (pulse_time_collection[i] - pulse_time_collection[i - 1])) * 1000)

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


def find_instances_for_subject_for_video(subject_id, video, threshold):
    pulse_collection = pd.read_csv('pulse_' + video + '_' + str(subject_id) + '_trimmed.csv')['Pulse']
    pulse_time_collection = pd.read_csv('pulse_' + video + '_' + str(subject_id) + '_trimmed.csv')['Timestamp']

    pulse_derivative_collection = take_derivative_of_pulse_for_video(pulse_collection, pulse_time_collection)

    pulse_derivative_abs_collection = [abs(val) for val in pulse_derivative_collection]

    interesting_timestamps = [pulse_time_collection[i] for i in range(len(pulse_derivative_abs_collection)) if pulse_derivative_abs_collection[i] >= threshold]

    return interesting_timestamps


def trim_for_timestamp(timestamp, collection, time_collection=None):
    if not time_collection is None:
        return [collection[i] for i in range(len(collection)) if timestamp[0] <= time_collection[i] <= timestamp[1]]
    return [collection[i][0] for i in range(len(collection)) if timestamp[0] <= collection[i][1] <= timestamp[1]]


def trim_for_end(duration, collection, time_collection=None):
    if not time_collection is None:
        return [collection[i] for i in range(len(collection)) if time_collection[i] >= (time_collection[len(time_collection) - 1] - duration)]
    new_collection = []
    for i in range(len(collection)):
        t = collection[i][1]
        start_end = collection[len(collection) - 1][1] - duration
        if t >= start_end:
            new_collection.append(collection[i][0])
    #new_collection = [collection[i][0] for i in range(len(collection)) if collection[i][1] >= (collection[len(collection) - 1][1] - duration)]
    return new_collection


def create_instances_for_video(working_directory, subject_id, video_id, threshold):
    os.chdir(working_directory)
    interesting_timestamps = find_instances_for_subject_for_video(subject_id, id_stimuli[video_id + 1], threshold)
    pulse_collection = pd.read_csv('pulse_' + id_stimuli[video_id + 1] + '_' + str(subject_id) + '_trimmed.csv')['Pulse']
    pulse_time_collection = pd.read_csv('pulse_' + id_stimuli[video_id + 1] + '_' + str(subject_id) + '_trimmed.csv')['Timestamp']
    answers = get_survey_answers_for_subject(working_directory, subject_id)[id_stimuli[video_id + 1]]
    data_dict = {}

    data_dict['User'] = []
    data_dict['Video'] = []
    data_dict['Intended_emotion'] = []

    for question in survey_questions.values():
        data_dict[question] = []

    for feature in features:
        for characteristic in characteristics:
            data_dict[feature + characteristic] = []

    pulse_derivative_collection = take_derivative_of_pulse_for_video(pulse_collection, pulse_time_collection)

    pulse_derivative_abs_collection = [abs(val) for val in pulse_derivative_collection]

    pulse_derivative_direction_collection = [(val / (abs(val) if not val == 0 else 1)) for val in pulse_derivative_collection]

    df = pd.read_csv(id_stimuli[video_id + 1] + '_' + str(subject_id) + '.csv')

    facial_features = {}
    for column in relevant_final_columns:
        facial_features[column] = ([(float(df[column][i]), df['Timestamp'][i]) for i in range(len(df[column])) if not np.isnan(df[column][i])])

    for timestamp in interesting_timestamps:
        timestamp = timestamp - 5000 if (timestamp - 5000) >= pulse_time_collection[0] else pulse_time_collection[0]
        timestamp = (timestamp, timestamp + 10000 if (timestamp + 10000) <= pulse_time_collection[len(pulse_time_collection) - 1] else pulse_time_collection[len(pulse_time_collection) - 1])

        #pulse_collection_for_timestamp = trim_for_timestamp(timestamp, pulse_collection, pulse_time_collection)
        pulse_derivative_collection_for_timestamp = trim_for_timestamp(timestamp, pulse_derivative_collection, pulse_time_collection)
        pulse_derivative_abs_collection_for_timestamp = trim_for_timestamp(timestamp, pulse_derivative_abs_collection, pulse_time_collection)
        pulse_derivative_direction_collection_for_timestamp = trim_for_timestamp(timestamp, pulse_derivative_direction_collection, pulse_time_collection)

        facial_features_for_timestamp = facial_features.copy()
        for column in facial_features_for_timestamp.keys():
            facial_features_for_timestamp[column] = trim_for_timestamp(timestamp, facial_features[column])

        data_dict['User'].append(subject_id)
        data_dict['Video'].append(video_id + 1)
        data_dict['Intended_emotion'].append(intended_emotions[(video_id / 3)])

        characteristics_values = calculate_characteristic(pulse_derivative_collection_for_timestamp)
        for i in range(5):
            data_dict['Pulse_derivative' + characteristics[i]].append(characteristics_values[i])

        characteristics_values = calculate_characteristic(pulse_derivative_abs_collection_for_timestamp)
        for i in range(5):
            data_dict['Pulse_derivative_abs' + characteristics[i]].append(characteristics_values[i])

        characteristics_values = calculate_characteristic(pulse_derivative_direction_collection_for_timestamp)
        for i in range(5):
            data_dict['Pulse_derivative_direction' + characteristics[i]].append(characteristics_values[i])

        for facial_feature in facial_features_for_timestamp.keys():
            characteristics_values = calculate_characteristic(facial_features_for_timestamp[facial_feature])
            for i in range(5):
                data_dict[facial_feature + characteristics[i]].append(characteristics_values[i])

        for question in survey_questions.values():
            if question == 'What did you feel when watching the video?':
                Q3_answer = str(answers[question][0])
                if len(answers[question]) > 1:
                    for j in range(1, len(answers[question])):
                        Q3_answer = Q3_answer + ' ' + str(answers[question][j])
                data_dict[question].append(Q3_answer)
                continue
            data_dict[question].append(answers[question][0])

    return data_dict


def create_end_instance_for_video(working_directory, subject_id, video_id, duration):
    os.chdir(working_directory)
    pulse_collection = pd.read_csv('pulse_' + id_stimuli[video_id + 1] + '_' + str(subject_id) + '_trimmed.csv')['Pulse']
    pulse_time_collection = pd.read_csv('pulse_' + id_stimuli[video_id + 1] + '_' + str(subject_id) + '_trimmed.csv')['Timestamp']
    answers = get_survey_answers_for_subject(working_directory, subject_id)[id_stimuli[video_id + 1]]
    data_dict = {}

    data_dict['User'] = []
    data_dict['Video'] = []
    data_dict['Intended_emotion'] = []

    for question in survey_questions.values():
        data_dict[question] = []

    for feature in features:
        for characteristic in characteristics:
            data_dict[feature + characteristic] = []

    pulse_derivative_collection = take_derivative_of_pulse_for_video(pulse_collection, pulse_time_collection)

    pulse_derivative_abs_collection = [abs(val) for val in pulse_derivative_collection]

    pulse_derivative_direction_collection = [(val / (abs(val) if not val == 0 else 1)) for val in
                                             pulse_derivative_collection]

    df = pd.read_csv(id_stimuli[video_id + 1] + '_' + str(subject_id) + '.csv')

    facial_features = {}
    for column in relevant_final_columns:
        facial_features[column] = ([(float(df[column][i]), df['Timestamp'][i]) for i in range(len(df[column])) if not np.isnan(df[column][i])])

    pulse_derivative_collection_for_end = trim_for_end(duration, pulse_derivative_collection, pulse_time_collection)
    pulse_derivative_abs_collection_for_end = trim_for_end(duration, pulse_derivative_abs_collection, pulse_time_collection)
    pulse_derivative_direction_collection_for_end = trim_for_end(duration, pulse_derivative_direction_collection, pulse_time_collection)

    facial_features_for_timestamp = facial_features.copy()
    for column in facial_features_for_timestamp.keys():
        facial_features_for_timestamp[column] = trim_for_end(duration, facial_features[column])

    data_dict['User'].append(subject_id)
    data_dict['Video'].append(video_id + 1)
    data_dict['Intended_emotion'].append(intended_emotions[(video_id / 3)])

    characteristics_values = calculate_characteristic(pulse_derivative_collection_for_end)
    for i in range(5):
        data_dict['Pulse_derivative' + characteristics[i]].append(characteristics_values[i])

    characteristics_values = calculate_characteristic(pulse_derivative_abs_collection_for_end)
    for i in range(5):
        data_dict['Pulse_derivative_abs' + characteristics[i]].append(characteristics_values[i])

    characteristics_values = calculate_characteristic(pulse_derivative_direction_collection_for_end)
    for i in range(5):
        data_dict['Pulse_derivative_direction' + characteristics[i]].append(characteristics_values[i])

    for facial_feature in facial_features_for_timestamp.keys():
        characteristics_values = calculate_characteristic(facial_features_for_timestamp[facial_feature])
        for i in range(5):
            data_dict[facial_feature + characteristics[i]].append(characteristics_values[i])

    for question in survey_questions.values():
        if question == 'What did you feel when watching the video?':
            Q3_answer = str(answers[question][0])
            if len(answers[question]) > 1:
                for j in range(1, len(answers[question])):
                    Q3_answer = Q3_answer + ' ' + str(answers[question][j])
            data_dict[question].append(Q3_answer)
            continue
        data_dict[question].append(answers[question][0])

    return data_dict


def create_final_sheet_for_subject_using_pulse_as_instances(working_directory, subject_id, threshold, allow_overlapping=True):
    os.chdir(working_directory)
    data_dict = {}

    data_dict['User'] = []
    data_dict['Video'] = []
    data_dict['Intended_emotion'] = []
    # add a list for each feature
    for feature in features:
        for characteristic in characteristics:
            data_dict[feature + characteristic] = []

    for question in survey_questions.keys():
        data_dict[survey_questions[question]] = []

    for i in range(15):
        video_instances = create_instances_for_video(working_directory, subject_id, i, threshold)
        instances = len(video_instances['User'])
        for j in range(instances):
            for column in final_columns:
                data_dict[column].append(video_instances[column][j])
    pd.DataFrame(data_dict)[final_columns].to_csv(str(subject_id) + '_with_instances.csv')


def create_final_sheet_for_subject_using_end_as_instances(working_directory, subject_id, duration):
    os.chdir(working_directory)
    data_dict = {}

    data_dict['User'] = []
    data_dict['Video'] = []
    data_dict['Intended_emotion'] = []
    # add a list for each feature
    for feature in features:
        for characteristic in characteristics:
            data_dict[feature + characteristic] = []

    for question in survey_questions.keys():
        data_dict[survey_questions[question]] = []

    for i in range(15):
        video_instances = create_end_instance_for_video(working_directory, subject_id, i, duration)
        instances = len(video_instances['User'])
        for j in range(instances):
            for column in final_columns:
                data_dict[column].append(video_instances[column][j])
    pd.DataFrame(data_dict)[final_columns].to_csv(str(subject_id) + '_with_end_instances.csv')


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
        print 'Can\'t make folder for ' + str(subject_id)
    for stimulus in stimuli:
        os.system('mv pulse_' + stimulus.replace(' ', '\ ') + '_' + str(subject_id) + '.txt ' + str(subject_id))
        os.system('mv pulse_' + stimulus.replace(' ', '\ ') + '_' + str(subject_id) + '_trimmed.csv ' + str(subject_id))
        os.system('mv ' + stimulus.replace(' ', '\ ') + '_' + str(subject_id) + '.csv ' + str(subject_id))
        os.system('mv ' + main_filename + ' ' + str(subject_id))
        os.system('mv ' + str(subject_id) + '.csv final')
        os.system('mv ' + str(subject_id) + '_with_instances.csv final')
        os.system('mv ' + str(subject_id) + '_with_end_instances.csv final')
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


def create_master_sheet(working_directory, excluded_subject):
    '''
    Creates a sheet which contains all data from all participants

    :param working_directory: The directory containing the final sheet for each participant
    :param excluded_subject: The subject that should be excluded during the training
    :return: None
    '''
    os.chdir(working_directory)
    master_sheet = {}
    for column in final_columns:
        master_sheet[column] = []
    files = os.listdir('.')
    files_with_instances = []
    files_with_end_instances = []
    original_files = []
    for filename in files:
        if 'master' in filename:
            continue
        elif 'with_end_instances' in filename:
            files_with_end_instances.append(filename)
        elif 'with_instances' in filename:
            files_with_instances.append(filename)
        else:
            original_files.append(filename)
    files_with_instances = sorted(files_with_instances, key=lambda filename: int(filename.replace('_with_instances.csv', '')))
    files_with_end_instances = sorted(files_with_end_instances, key=lambda filename: int(filename.replace('_with_end_instances.csv', '')))
    original_files = sorted(original_files, key=lambda filename: int(filename.replace('.csv', '')))
    for filename in original_files:
        if filename == (str(excluded_subject) + '.csv'):  # exclude one subject in final document
            continue
        df = pd.read_csv(filename)
        for column in final_columns:
            master_sheet[column].extend(df[column])

    pd.DataFrame(master_sheet)[final_columns].to_csv('master.csv')

    master_sheet = {}
    for column in final_columns:
        master_sheet[column] = []

    for filename in files_with_instances:
        if filename == (str(excluded_subject) + '_with_instances.csv'):  # exclude one subject in final document
            continue
        df = pd.read_csv(filename)
        for column in final_columns:
            master_sheet[column].extend(df[column])

    pd.DataFrame(master_sheet)[final_columns].to_csv('master_with_instances.csv')

    new_master_sheet = {}
    for column in final_columns:
        new_master_sheet[column] = []

    for i in range(len(master_sheet['User'])):
        has_data = False
        for column in relevant_final_columns:
            for characteristic in characteristics:
                if not master_sheet[column + characteristic][i] == 0:
                    has_data = True
        if has_data:
            for column in final_columns:
                new_master_sheet[column].append(master_sheet[column][i])

    pd.DataFrame(new_master_sheet)[final_columns].to_csv('master_with_instances_removed_0.csv')

    master_sheet = {}
    for column in final_columns:
        master_sheet[column] = []

    for filename in files_with_end_instances:
        if filename == (str(excluded_subject) + '_with_end_instances.csv'):  # exclude one subject in final document
            continue
        df = pd.read_csv(filename)
        for column in final_columns:
            master_sheet[column].extend(df[column])

    pd.DataFrame(master_sheet)[final_columns].to_csv('master_with_end_instances.csv')


def plot_pulse(pulse, time, markers=[], figurenum=1, do_plot=True):
    '''
    Plot a set of datapoints

    :param datapoints: the datapoints to plot in a list
    :return: None
    '''
    plt.figure(figurenum)
    plt.plot(time, pulse)
    max_pulse = max(pulse) + 10
    for marker in markers:
        x = np.arange(marker, marker + 10000)
        plt.axes().fill_between(x, ([0 for i in range(len(x))]), ([max_pulse for i in range(len(x))]), color='r', alpha=0.5)
        plt.plot([marker, marker], [max_pulse, 0], color='k', linestyle='-', lw=1, alpha=1)
    if do_plot:
        plt.show()


def load_config():
    config = {}
    with open('config.txt', 'r') as f:
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

    for i in range(1, participants + 1):
        if i == 4 or i == 20 or i == 23 or i == 28 or i == 32:  # these have faulty pulse files
            continue
        filename = ('0' + str(participants + 1 - i) + '_' + str(i) + '.csv')
        if (participants + 1 - i) < 10:
            filename = ('00' + str(participants + 1 - i) + '_' + str(i) + '.csv')
        organize(i, filename)
        os.chdir(working_directory)
    create_master_sheet(working_directory + 'final/', excluded_subject)
    return
    #if config['LEAVE_ONE_SUBJECT_OUT'] == 'Y:
    #    excluded_subject = random.randint(1, participants)

    for i in range(1, participants + 1):
        if i == 4 or i == 20 or i == 23 or i == 28 or i == 32:  # these have faulty pulse files
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
            create_final_sheet_for_subject_using_pulse_as_instances(working_directory, i, int(config['THRESHOLD']) if config['THRESHOLD'] else 20)
            create_final_sheet_for_subject_using_end_as_instances(working_directory, i, int(config['DURATION']))
            #organize(i, filename)
            os.chdir(working_directory)
        else:
            print 'data for participant ' + str(i) + ' is missing, skipping that participant'
            continue

    create_master_sheet(working_directory + 'final/', excluded_subject)


if __name__ == "__main__":
    preprocess()