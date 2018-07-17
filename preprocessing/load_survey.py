from static_values import *
import os
import pandas as pd
import numpy as np


def get_survey_duration(df):
    '''
    Finds the survey duration (might be redundant)

    :param df: dataframe containing all data for a participant
    :return: timestamps for the surveys
    '''
    timestamps = {}
    current_stimuli = df['StimulusName'][0]
    # Iterate over all the stimuli and extract the timestamps that define the start and stop time of each stimulus
    start_time = int(df['Timestamp'][0])
    for i in range(len(df['StimulusName'])):
        if df['StimulusName'][i] == current_stimuli:
            continue
        end_time = int(df['Timestamp'][i - 1])
        if current_stimuli in survey_corresponding_to_stimulus.keys():
            timestamps[survey_corresponding_to_stimulus[current_stimuli]] = (start_time, end_time)
        start_time = end_time
        current_stimuli = df['StimulusName'][i]
    return timestamps


def get_survey_answer_for_subject(working_directory, subject_id, survey):
    '''
    Gets the survey answers of one survey for a subject

    :param working_directory: The directory containing all the files
    :param subject_id: The subjects id
    :param survey: The survey to get the answers for
    :return: The answers in a dictionary using questions as keys
    '''
    os.chdir(working_directory)
    answers = {}
    for question in survey_questions.keys():
        answers[survey_questions[question]] = []
        filename = survey_name +survey + question + '.csv'
        df = pd.read_csv(filename, skiprows=survey_question_header_start[question])
        for i in range(len(df['RESPONDENT'])):
            if int(df['RESPONDENT'][i]) == subject_id:
                if not np.isnan(df['Question1.LABELVALUE'][i]):  # check if this column name is same for all questions
                    answers[survey_questions[question]].append(int(df['Question1.LABELVALUE'][i]))
    return answers


def get_survey_answers_for_subject(working_directory, subject_id):
    '''
    Gets the survey answers for all videos for a subject

    :param working_directory: The directory containing all the files
    :param subject_id: The subject id
    :return: The answers in a dictionary using video name as keys
    '''
    survey_answers_for_subject = {}
    for survey in survey_corresponding_to_stimulus.keys():
        survey_answers_for_subject[survey_corresponding_to_stimulus[survey]] = get_survey_answer_for_subject(working_directory, subject_id, survey)
    return survey_answers_for_subject
