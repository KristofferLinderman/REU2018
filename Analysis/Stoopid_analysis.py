import csv
import os

import matplotlib

import load_data
import matplotlib.pyplot as plt
from static_values import *

import pandas as pd


def bar_chart_video_watch_similar(data, figure_number):
    names = stimuli_id.keys()
    names = sorted(names, key=lambda name: stimuli_id[name])

    survey_answers = {}
    for name in names:
        survey_answers[name] = []

    for name in names:
        survey_scores = data.get_survey_question_for_video(name, 'Would you want to watch similar videos?')
        for i in range(1, 6):
            survey_answers[name].append(0)
            for s in survey_scores:
                if s == i:
                    survey_answers[name][i - 1] = survey_answers[name][i - 1] + 1

    plt.figure(figure_number)
    plt.tight_layout()

    xValues = [1, 2, 3]
    xStr = ["Yes", "No", "Maybe"]
    y_limit = 25
    x_limit = 4

    plt.xticks(xValues)
    subplots = []

    order = [1, 6, 11, 2, 7, 12, 3, 8, 13, 4, 9, 14, 5, 10, 15]
    for i in range(len(names)):
        subplots.append(plt.subplot(3, 5, order[i]))
        plt.title('Watch similar for \"' + names[i] + '\"')
        plt.xticks(xValues, xStr)
        plt.yticks(range(0, y_limit, 2))
        plt.bar([1, 2, 3, 4, 5], survey_answers[names[i]])
    for sub in subplots:
        sub.set_ylim(0, y_limit)
        sub.set_xlim(0, x_limit)
    plt.subplots_adjust(top=0.92, bottom=0.08)


def bar_chart_video_watch_similar_selective(data, figure_number, names_of_videos, graph_rows, graph_columns):
    survey_answers = {}
    for name in names_of_videos:
        survey_answers[name] = []

    for name in names_of_videos:
        survey_scores = data.get_survey_question_for_video(name, 'Would you want to watch similar videos?')
        for i in range(1, 6):
            survey_answers[name].append(0)
            for s in survey_scores:
                if s == i:
                    survey_answers[name][i - 1] = survey_answers[name][i - 1] + 1

    plt.figure(figure_number)
    plt.tight_layout()

    xValues = [1, 2, 3]
    xStr = ["Yes", "No", "Maybe"]
    y_limit = 25
    x_limit = 4

    plt.xticks(xValues)
    subplots = []

    # order = [1, 6, 11, 2, 7, 12, 3, 8, 13, 4, 9, 14, 5, 10, 15]
    for i in range(len(names_of_videos)):
        matplotlib.rcParams.update({'font.size': 22})
        subplots.append(plt.subplot(graph_rows, graph_columns, i + 1))
        plt.title('Watch similar for \"' + names_of_videos[i] + '\"')
        plt.xticks(xValues, xStr)
        plt.yticks(range(0, y_limit, 2))
        plt.bar([1, 2, 3, 4, 5], survey_answers[names_of_videos[i]])
    for sub in subplots:
        sub.set_ylim(0, y_limit)
        sub.set_xlim(0, x_limit)
    plt.subplots_adjust(top=0.92, bottom=0.08)


# plt.savefig('graphs/' + sys._getframe().f_code.co_name + '.png', dpi=200)


def histogram_score(data, figure_number):
    names = stimuli_id.keys()
    names = sorted(names, key=lambda name: stimuli_id[name])

    survey_scores = {}
    for name in names:
        survey_scores[name] = []

    for name in names:
        scores = data.get_survey_question_for_video(name, 'One a scale of 1 to 5, how would you rate the video?')
        for i in range(1, 6):
            survey_scores[name].append(0)
            for s in scores:
                if s == i:
                    survey_scores[name][i - 1] = survey_scores[name][i - 1] + 1

    plt.figure(figure_number)

    y_limit = 25
    x_limit = 4

    subplots = []

    order = [1, 6, 11, 2, 7, 12, 3, 8, 13, 4, 9, 14, 5, 10, 15]
    for i in range(len(names)):
        subplots.append(plt.subplot(3, 5, order[i]))
        plt.title('Score for \"' + names[i] + '\"')
        # plt.yticks(range(0, y_limit, 2))
        plt.hist(survey_scores[names[i]], bins=[1, 2, 3, 4, 5, 6])
    # for sub in subplots:
    #     sub.set_ylim(0, y_limit)
    #     sub.set_xlim(0, x_limit)
    plt.subplots_adjust(top=0.92, bottom=0.08)


def bar_diagram_video_rating_total(data, figure_number):
    names = stimuli_id.keys()
    names = sorted(names, key=lambda name: stimuli_id[name])

    scores = [0, 0, 0, 0, 0]

    for name in names:
        survey_scores = data.get_survey_question_for_video(name, 'One a scale of 1 to 5, how would you rate the video?')
        for i in range(1, 6):
            for s in survey_scores:
                if s == i:
                    scores[i - 1] = scores[i - 1] + 1

    plt.figure(figure_number)

    plt.title('One a scale of 1 to 5, how would you rate the video?')
    plt.xlabel('Score')
    plt.ylabel('Number of votes')
    plt.bar([1, 2, 3, 4, 5], scores)

    print scores
    print sum(scores)


def bar_chart_video_watch_similar_total(data, figure_number):
    names = stimuli_id.keys()
    names = sorted(names, key=lambda name: stimuli_id[name])

    survey_answers = [0 for i in range(0, 5, 1)]

    for name in names:
        survey_scores = data.get_survey_question_for_video(name, 'Would you want to watch similar videos?')
        for i in range(1, 6):
            for s in survey_scores:
                if s == i:
                    survey_answers[i - 1] = survey_answers[i - 1] + 1

    print survey_answers
    plt.figure(figure_number)

    xValues = [1, 2, 3]
    xStr = ["Yes", "No", "Maybe"]

    plt.xticks(xValues)

    plt.title('Would you want to watch similar videos?')
    plt.xticks(xValues, xStr)
    plt.xlim(0, 4)

    plt.ylabel('Number of votes')
    plt.bar([1, 2, 3, 4, 5], survey_answers)


def prepare_face_files():
    # Deletes the first 5 rows of the files
    delete_the_top('/Users/kristoffer/Programming/Python/REU2018/Sensor_data')
    # Converts .txt to .csv
    convert('/Users/kristoffer/Programming/Python/REU2018/Sensor_data')


def convert(directory):
    os.chdir(directory)
    for file in os.listdir('.'):
        if '.txt' in str(file):
            print file + '\t->\t' + file.replace('.txt', '.csv')
            in_txt = csv.reader(open(file, "r"), delimiter='\t')
            out_csv = csv.writer(open(file.replace('.txt', '.csv'), 'w'))
            out_csv.writerows(in_txt)
            # os.system('rm \'' + file + '\'')


def delete_the_top(directory):
    os.chdir(directory)
    for file in os.listdir('.'):
        if '.txt' in str(file):
            f = open(file, 'r')
            lines = f.readlines()
            f.close()
            f = open(file, 'w')

            index = 0
            for line in lines:
                if index > 4:
                    f.write(line)
                index += 1
            print file + ' has been modified'


def face_finder(fileToSearch):
    df = pd.read_csv(fileToSearch)
    # print df.head()

    participant_faces = df['Number of faces']

    total_length = len(participant_faces)
    index = 0
    threshold = 3
    empty_face_count = 0

    while index < total_length:
        if participant_faces[index] == 0:
            consecutive_count = count_consecutive_zeros(index, participant_faces)
            if consecutive_count >= threshold:
                # print 'Bigger than three at ', index, 'with a count of ', consecutive_count
                empty_face_count += consecutive_count
                index += consecutive_count
        index += 1

    # print empty_face_count
    # print total_length
    percentage = float(empty_face_count) / float(total_length)

    # print 'Percentage:', percentage
    return percentage


def count_consecutive_zeros(index, data):
    i = index
    count = 0
    while data[i] == 0:
        count += 1
        i += 1
        if i >= len(data):
            break

    return count


def calculate_percentage_of_face():
    names = stimuli_id.keys()
    names = sorted(names, key=lambda name: stimuli_id[name])

    average_percentages = {}
    # for name in names:
    #     average_percentages[name] = 0
    #
    # nbr_of_perticipants = 27
    # min = 1
    # min_id = 0
    # counter = 0
    #
    # progress = 0
    #
    # print average_percentages
    # os.chdir('/Users/kristoffer/Programming/Python/REU2018/Kdata/Facials/')
    # files = os.listdir('.')
    # files = sorted(files)
    #
    # for f in files:
    #     # print os.path.abspath(file)
    #     # print 'Finding missing faces...'
    #     percentage = face_finder(f)
    #
    #     if percentage < min:
    #         min = percentage
    #         min_id = f
    #     if percentage != 1.0:
    #         counter += 1
    #
    #     # print 'Percetage for ', f, ' is: ', percentage
    #     name = f.split('_')[0]
    #
    #     average_percentages[name] += percentage
    #
    #     progress += 1
    #     print 'Progess: ', progress, '/405'
    #
    # print '\n * * * * * * \n'
    # print average_percentages
    # print '\n * * * * * * \n'
    #
    # for name in names:
    #     average_percentages[name] = (average_percentages[name] / nbr_of_perticipants) * 100
    #
    # print '\n * * * * * * \n'
    # print average_percentages
    # print '\n * * * * * * \n'
    #
    # print 'Min: ', min, ' at: ', min_id
    # print 'Not 100% ', counter, ' times'

    #The results from running above code, saved here to make it run faster
    average_percentages = {'Amish': 0.26169395883046914, 'Help': 0.1647084343029575, 'Noah': 1.4021603996022252,
                           'Cocaine': 2.8603968743183628, 'Dino': 1.6580366306666459, 'Wheelchair': 0.2589345128474099,
                           'Flying': 0.5887483566445857, 'Interstellar': 0.7255009664283529, 'Dog': 1.4269808758258062,
                           'Magic Bird': 0.5097514199247638, 'Despicable': 1.0238091212366427,
                           'Shining': 1.0465837429798766,
                           'Forest': 0.40808758821026014, 'Cat': 0.42802938004100133, 'Iguana': 1.1831055901208942}

    lister = []
    for val in average_percentages.values():
        lister.append(val)

    plt.bar(average_percentages.keys(), lister)
    plt.ylabel('Percentage of total duration with missing face')
    plt.show()


def Analysis():
    data = load_data.Data('../..')
    # hist_emotion_facial_expressions(data, 1)
    # bar_chart_video_watch_similar(data, 1)
    # bar_chart_video_watch_similar_selective(data, 1,['Despicable','Dog'])
    bar_chart_video_watch_similar_selective(data, 1, ['Shining'], 1, 1)
    # histogram_score(data,1)
    # bar_diagram_video_rating_total(data, 1)
    # bar_chart_video_watch_similar_total(data,2)

    # prepare_face_files()
    plt.show()

    # calculate_percentage_of_face()


if __name__ == '__main__':
    Analysis()
