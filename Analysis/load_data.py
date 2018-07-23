import pandas as pd
import numpy as np
import os
from static_values import *


class Data:
    def __init__(self, working_directory):
        os.chdir(working_directory)
        self.df = pd.read_csv('master.csv')
        self.length = len(self.df['User'])

    def get_column_for_video(self, column, video):
        '''
        Gets a single column for one video

        :param column: The column
        :param video: The video
        :return: The column as a pandas Series?
        '''
        return [self.df[column][i] for i in range(self.length) if int(self.df['Video'][i]) == stimuli_id[video]]

    def get_column_for_video_for_subject(self, column, video, subject_id):
        '''
        Gets a column for a video for a subject

        :param column: The column to get
        :param video: The video
        :param subject_id: The subject id
        :return: The column for a certain video for a subject
        '''
        column_for_video = self.get_column_for_video(column, video)
        return [column_for_video[i] for i in range(self.length) if int(self.df['User'][i]) == subject_id]

    def get_surveys_for_video(self, video):
        '''
        Gets the survey answers for one video

        :param video: The video
        :return: The survey answers for a video, indexed by question name
        '''
        survey_data = {}
        for column in survey_questions:
            survey_data[column] = self.get_column_for_video(column, video)
        return survey_data

    def get_survey_question_for_video(self, video, question):
        '''
        Gets a certain survey question for a certain video

        :param video: The video
        :param question: The question
        :return: The answers for a certain question for a certain video
        '''
        return self.get_surveys_for_video(video)[question]