from static_values import *
import pandas as pd
import os
import numpy as np

def trim_pulse_log_for_stimulus(working_directory, subject_id, timestamps):
    '''
    Creates new files that contain the trimmed pulse logs, that is the pulse that is relevant for a certain stimulus

    :param subject_id: the subjects id
    :param timestamps: the start and end timestamps for each stimuli stored in a dictionary
    :return: None
    '''
    os.chdir(working_directory)
    for stimulus in stimuli:
        with open('pulse_' + stimulus + '_' + str(subject_id) + '.txt', 'r') as f:
            lines = [line.replace('(', '').replace(')', '').split(' ') for line in f]
        # It might miss first and last value
        trimmed = [line for line in lines if int(line[0]) > timestamps[stimulus][0] and int(line[0]) < timestamps[stimulus][1]]  # put all lines that are within the span of the stimulus in the list 'trimmed'
        trimmed_dict = {'Timestamp': [], 'Pulse': []}
        for line in trimmed:
            trimmed_dict['Timestamp'].append(line[0])
            trimmed_dict['Pulse'].append(line[1])
        # write the trimmed list to a file
        pd.DataFrame(trimmed_dict).to_csv('pulse_' + stimulus + '_' + str(subject_id) + '_trimmed.csv')


def trim_facial_data(working_directory, subject_id, dataframe, experiment_time):
    '''
    Trims the facial data and saves it to a .csv file

    :param subject_id: The subject for which to trim
    :param dataframe: The dataframe containing all the data
    :param experiment_time: The start time of the experiment
    :return: None
    '''
    os.chdir(working_directory)
    data_dict = {}
    for column in relevant_columns:
        data_dict[column] = []

    current_stimulus = dataframe['StimulusName'][0]
    for i in range(len(dataframe['StimulusName'])):
        if not dataframe['StimulusName'][i] in stimuli:  # we don't care about stimulus that are not videos
            continue
        if not dataframe['StimulusName'][i] == current_stimulus:  # if this row is a new stimulus, save the previous one
            if not current_stimulus == 'demographic':  # we don't want to save demographic
                pd.DataFrame(data_dict).to_csv(current_stimulus + '_' + str(subject_id) + '.csv')
            data_dict = {}  # empty the data_dict and start over
            for column in relevant_columns:
                data_dict[column] = []
            current_stimulus = dataframe['StimulusName'][i]
        for column in relevant_columns:  # save the columns we want from the data file
            if column == 'Timestamp':
                data_dict[column].append(int(dataframe[column][i]) + (int(experiment_time.strftime("%s")) * 1000))  # the timestamp is experiment start time + offset
            else:
                data_dict[column].append(float(dataframe[column][i]))
    pd.DataFrame(data_dict).to_csv(current_stimulus + '_' + str(subject_id) + '.csv')  # get that last one aswell

#TODO Handle all files at once
def combine_pulse_and_facial(subject_id, filename_pulse, filename_facial):
    '''
    Combine the pulse and facial data into a single file

    :param subject_id: The subject id
    :param filename_pulse: The filename for the file containing the trimmed pulse data
    :param filename_facial:  The filename for the file containing the trimmed facial data
    :return:
    '''
    df_pulse = pd.read_csv(filename_pulse)
    df_facial = pd.read_csv(filename_facial)

    # create a combined list of all timestamps
    combined_timestamps = []
    combined_timestamps.extend([float(timestamp) for timestamp in list(df_pulse['Timestamp'])])
    combined_timestamps.extend([float(timestamp) for timestamp in list(df_facial['Timestamp'])])
    combined_timestamps = list(set(combined_timestamps))
    combined_timestamps.sort()

    data_dict = {}
    for column in relevant_columns:
        data_dict[column] = []
    data_dict['Pulse'] = []

    # create lists containing float values for easier comparison in the loop
    df_pulse_timestamps = [float(timestamp) for timestamp in df_pulse['Timestamp']]
    df_facial_timestamps = [float(timestamp) for timestamp in df_facial['Timestamp']]

    m = 0
    n = 0
    for i in range(len(combined_timestamps)):
        # If the timestamp exists in both files, add both data types to the row and increment both counters
        if combined_timestamps[i] in df_pulse_timestamps and combined_timestamps[i] in df_facial_timestamps:
            for column in relevant_columns:
                if column == 'Timestamp':  # We take care of Timestamp later on
                    continue
                data_dict[column].append(df_facial[column][n])
            data_dict['Pulse'].append(float(df_pulse['Pulse'][m]))
            n = n + 1
            m = m + 1
        elif combined_timestamps[i] in df_pulse_timestamps:
            data_dict['Pulse'].append(float(df_pulse['Pulse'][m]))
            for column in relevant_columns:
                if column == 'Timestamp':
                    continue
                data_dict[column].append('')
            m = m + 1
        elif combined_timestamps[i] in df_facial_timestamps:
            for column in relevant_columns:
                if column == 'Timestamp':
                    continue
                data_dict[column].append(df_facial[column][n])
            data_dict['Pulse'].append(float(0))
            n = n + 1

    data_dict['Timestamp'] = combined_timestamps  # set the timestamps to be the combined
    pd.DataFrame(data_dict).to_csv('combined_pulse_facial_' + str(subject_id) + '.csv')


def trim_pulse_and_facial(filename):
    '''
    Trims the combined pulse and facial file

    :param filename: the combined pulse and facial filename
    :return: None
    '''
    df = pd.read_csv(filename)
    data_dict = {}
    for column in relevant_columns:
        data_dict[column] = []
    data_dict['Pulse'] = []

    for i in range(len(df['Timestamp'])):
        if np.isnan(df['Anger'][i]) and df['Pulse'][i] == 0:
            continue
        for column in relevant_columns:
            data_dict[column].append(df[column][i])
        data_dict['Pulse'].append(df['Pulse'][i])
    pd.DataFrame(data_dict).to_csv('test_trimmed.csv')


def fill_in_blanks_pulse_and_facial(filename):
    '''
    Fills in the rows that have missing values by just copying from last populated row

    :param filename: the filename of the combined pulse and facial
    :return:
    '''
    df = pd.read_csv(filename)
    data_dict = {}
    for column in relevant_columns:
        data_dict[column] = []
    data_dict['Pulse'] = []
    for i in range(len(df['Timestamp'])):
        if np.isnan(df['Anger'][i]):
            for column in relevant_columns:
                try:
                    data_dict[column].append(df[column][i - 1])
                except:
                    data_dict[column].append(df[column][i])
        else:
            for column in relevant_columns:
                data_dict[column].append(df[column][i])
        if df['Pulse'][i] == 0:
            try:
                data_dict['Pulse'].append(df['Pulse'][i - 1])
            except:
                data_dict['Pulse'].append(df['Pulse'][i])
        else:
            data_dict['Pulse'].append(df['Pulse'][i])
    data_dict['Timestamp'] = df['Timestamp']
    for column in relevant_columns:
        print column + ': ' + str(len(data_dict[column]))
    print 'Pulse: ' + str(len(data_dict['Pulse']))
    pd.DataFrame(data_dict).to_csv('test_trimmed_filled_in_blanks.csv')
