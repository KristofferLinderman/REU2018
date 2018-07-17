stimuli = {'Iguana', 'Dog', 'Magic Bird', 'Wheelchair', 'Shining', 'Flying', 'Dino', 'Cocaine', 'Noah', 'Cat', 'Help', 'Amish', 'Despicable', 'Interstellar', 'Forest'}  # the video stimulus
relevant_columns = {'Timestamp', 'Engagement', 'Valence', 'Attention', 'Anger', 'Sadness', 'Disgust', 'Joy', 'Surprise', 'Fear', 'Contempt', 'Smile'}
relevant_final_columns = {'Engagement', 'Valence', 'Attention', 'Anger', 'Sadness', 'Disgust', 'Joy', 'Surprise', 'Fear', 'Contempt', 'Smile'}

stimuli_id = {'Noah': 1, 'Cat': 2, 'Despicable': 3,
              'Dog': 4, 'Forest': 5, 'Interstellar': 6,
              'Wheelchair': 7, 'Help': 8, 'Amish': 9,
              'Iguana': 10, 'Shining': 11, 'Dino': 12,
              'Magic Bird': 13, 'Flying': 14, 'Cocaine': 15}

id_stimuli = {1: 'Noah', 2: 'Cat', 3: 'Despicable',
              4: 'Dog', 5: 'Forest', 6: 'Interstellar',
              7: 'Wheelchair', 8: 'Help', 9: 'Amish',
              10: 'Iguana', 11: 'Shining', 12: 'Dino',
              13: 'Magic Bird', 14: 'Flying', 15: 'Cocaine'}

intended_emotions = ['Joy', 'Sadness', 'Anger', 'Fear', 'Surprise']

final_columns = ['User', 'Video', 'Intended_emotion',
                 'Pulse_derivative_min', 'Pulse_derivative_max', 'Pulse_derivative_average', 'Pulse_derivative_median', 'Pulse_derivative_standard_deviation',
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
                 'Smile_min', 'Smile_max', 'Smile_average', 'Smile_median', 'Smile_standard_deviation',
                 #'Smirk_min', 'Smirk_max', 'Smirk_average', 'Smirk_median', 'Smirk_standard_deviation',
                 'Have you watched this video before?', 'One a scale of 1 to 5, how would you rate the video?', 'Would you want to watch similar videos?', 'What did you feel when watching the video?']

characteristics = ['_min', '_max', '_average', '_median', '_standard_deviation']

features = ['Pulse_derivative', 'Pulse_derivative_abs', 'Pulse_derivative_direction', 'Engagement', 'Attention','Valence',
            'Anger', 'Sadness', 'Disgust', 'Joy', 'Surprise', 'Fear', 'Contempt', 'Smile']

survey_corresponding_to_stimulus = {'Team6VideoSurvey-13': 'Shining',
                                    'Team6VideoSurvey': 'Cat',
                                    'Team6VideoSurvey-6': 'Interstellar',
                                    'Team6VideoSurvey-10': 'Noah',
                                    'Team6VideoSurvey-11': 'Amish',
                                    'Team6VideoSurvey-8': 'Iguana',
                                    'Team6VideoSurvey-2': 'Dino',
                                    'Team6VideoSurvey-4': 'Flying',
                                    'Team6VideoSurvey-3': 'Dog',
                                    'Team6VideoSurvey-1': 'Despicable',
                                    'Team6VideoSurvey-5': 'Forest',
                                    'Team6VideoSurvey-9': 'Magic Bird',
                                    'Team6VideoSurvey-14': 'Wheelchair',
                                    'Team6VideoSurvey-7': 'Help',
                                    'Team6VideoSurvey-12': 'Cocaine'}

survey_name = 'Team 6_Copy-Analysis-'
#TODO missing Question 6, 'if other, please specify' (How should we handle that data?)
survey_questions = {'-Q1': 'Have you watched this video before?',
                    '-Q3': 'What did you feel when watching the video?',
                    '-Q5': 'Would you want to watch similar videos?',
                    '-Question (5)': 'One a scale of 1 to 5, how would you rate the video?'}

survey_question_header_start = {'-Q1': 14,
                                '-Q3': 17,
                                '-Q5': 14,
                                '-Question (5)': 16}

demographic_survey_name = 'Team 6_Copy-Analysis-demographic-'
