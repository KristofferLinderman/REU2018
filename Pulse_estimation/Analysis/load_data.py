import pandas as pd
import numpy as np
import os
from static_values import *

class data():
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
        column_for_video = self.get_column_for_video(column, video)
        return [column_for_video[i] for i in range(self.length) if int(self.df['User'][i]) == subject_id]


    def get_surveys_for_video(self, video):
        survey_data = {}
        for column in survey_questions:
            if column == 'What did you feel when watching the video?': #TODO fix
                continue
            survey_data[column] = self.get_column_for_video(column, video)
        return survey_data


    def get_survey_question_for_video(self, video, question):
        return self.get_surveys_for_video(video)[question]