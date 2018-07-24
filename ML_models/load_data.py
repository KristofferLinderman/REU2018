import os
import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score
import random

all_columns_min_max_avg = ['Pulse_derivative_min', 'Pulse_derivative_max', 'Pulse_derivative_average',
                           'Engagement_min', 'Engagement_max', 'Engagement_average',
                           'Attention_min', 'Attention_max', 'Attention_average',
                           'Valence_min', 'Valence_max', 'Valence_average',
                           'Anger_min', 'Anger_max', 'Anger_average',
                           'Sadness_min', 'Sadness_max', 'Sadness_average',
                           'Disgust_min', 'Disgust_max', 'Disgust_average',
                           'Joy_min', 'Joy_max', 'Joy_average',
                           'Surprise_min', 'Surprise_max', 'Surprise_average',
                           'Fear_min', 'Fear_max', 'Fear_average',
                           'Contempt_min', 'Contempt_max', 'Contempt_average']


all_columns_min_max_avg_no_pulse = ['Pulse_derivative_min', 'Pulse_derivative_max', 'Pulse_derivative_average',
                                    'Engagement_min', 'Engagement_max', 'Engagement_average',
                                    'Attention_min', 'Attention_max', 'Attention_average',
                                    'Valence_min', 'Valence_max', 'Valence_average',
                                    'Anger_min', 'Anger_max', 'Anger_average',
                                    'Sadness_min', 'Sadness_max', 'Sadness_average',
                                    'Disgust_min', 'Disgust_max', 'Disgust_average',
                                    'Joy_min', 'Joy_max', 'Joy_average',
                                    'Surprise_min', 'Surprise_max', 'Surprise_average',
                                    'Fear_min', 'Fear_max', 'Fear_average',
                                    'Contempt_min', 'Contempt_max', 'Contempt_average']

all_columns_avg = ['Engagement_average',
                   'Attention_average',
                   'Valence_average',
                   'Anger_average',
                   'Sadness_average',
                   'Disgust_average',
                   'Joy_average',
                   'Surprise_average',
                   'Fear_average',
                   'Contempt_average']

all_columns_all_characteristics = ['Pulse_derivative_min', 'Pulse_derivative_max', 'Pulse_derivative_average', 'Pulse_derivative_median', 'Pulse_derivative_standard_deviation',
                                   'Pulse_derivative_abs_min', 'Pulse_derivative_abs_max', 'Pulse_derivative_abs_average', 'Pulse_derivative_abs_median', 'Pulse_derivative_abs_standard_deviation',
                                   'Pulse_derivative_direction_min', 'Pulse_derivative_direction_max', 'Pulse_derivative_direction_average', 'Pulse_derivative_direction_median', 'Pulse_derivative_direction_standard_deviation',
                                   'Engagement_min', 'Engagement_max', 'Engagement_average', 'Engagement_median', 'Engagement_standard_deviation',
                                   'Attention_min', 'Attention_max', 'Attention_average', 'Attention_median', 'Attention_standard_deviation',
                                   'Valence_min', 'Valence_max', 'Valence_average', 'Valence_median', 'Valence_standard_deviation',
                                   'Anger_min', 'Anger_max', 'Anger_average', 'Anger_median', 'Anger_standard_deviation',
                                   'Sadness_min', 'Sadness_max', 'Sadness_average', 'Sadness_median', 'Sadness_standard_deviation',
                                   'Disgust_min', 'Disgust_max', 'Disgust_average', 'Disgust_median', 'Disgust_standard_deviation',
                                   'Joy_min', 'Joy_max', 'Joy_average', 'Joy_median', 'Joy_standard_deviation',
                                   'Surprise_min', 'Surprise_max', 'Surprise_average', 'Surprise_median', 'Surprise_standard_deviation',
                                   'Fear_min', 'Fear_max', 'Fear_average', 'Fear_median', 'Fear_standard_deviation',
                                   'Contempt_min', 'Contempt_max', 'Contempt_average', 'Contempt_median', 'Contempt_standard_deviation',
                                   'Smile_min', 'Smile_max', 'Smile_average', 'Smile_median', 'Smile_standard_deviation']


features = ['Pulse_derivative', 'Pulse_derivative_abs', 'Pulse_derivative_direction', 'Engagement', 'Attention','Valence',
            'Anger', 'Sadness', 'Disgust', 'Joy', 'Surprise', 'Fear', 'Contempt', 'Smile']


def cross_validation(clf, data_X, data_y, folds, name):
    scores = cross_val_score(clf, data_X, data_y, cv=folds)
    return scores


def load_data(working_directory, filename, columns, question, classify_maybe_as=None):
    os.chdir(working_directory)
    df = pd.read_csv(filename)
    data_X = []
    for j in range(len(columns)):
        if classify_maybe_as == 'Exclude' and question == 'Would you want to watch similar videos?':
            data_X.append([])
            for i in range(len(df[columns[j]])):
                if not df['Would you want to watch similar videos?'][i] == 3:
                    data_X[j].append((df[columns[j]][i]))
        else:
            data_X.append(df[columns[j]])
    data_X = np.transpose(data_X)
    if question == 'Would you want to watch similar videos?':
        if classify_maybe_as == 'No':
            data_y = [s if s == 1 or s == 2 else 2 for s in list(df[question])]
        elif classify_maybe_as == 'Yes':
            data_y = [s if s == 1 or s == 2 else 1 for s in list(df[question])]
        elif classify_maybe_as == 'Half':
            data_y = [s if s == 1 or s == 2 else random.randint(1, 2) for s in list(df[question])]
        elif classify_maybe_as == 'Exclude':
            data_y = [s for s in list(df[question]) if s == 1 or s == 2]
        else:
            data_y = list(df[question])
    else:
        data_y = list(df[question])

    return data_X, data_y
