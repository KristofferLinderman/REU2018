import sys

import load_data
import matplotlib.pyplot as plt
from static_values import *


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

    xValues = [1, 2, 3]
    xStr = ["Yes", "No", "Maybe"]
    y_limit = 25
    x_limit = 4

    plt.xticks(xValues)
    subplots = []

    order = [1, 6, 11, 2, 7, 12, 3, 8, 13, 4, 9, 14, 5, 10, 15]
    for i in range(len(names)):
        subplots.append(plt.subplot(3, 5, order[i]))
        plt.title('Watch again for \"' + names[i] + '\"')
        plt.xticks(xValues, xStr)
        plt.yticks(range(0, y_limit, 2))
        plt.bar([1, 2, 3, 4, 5], survey_answers[names[i]])
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

    survey_answers = [0 for i in range(0,5,1)]

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
    plt.xlim(0,4)

    plt.ylabel('Number of votes')
    plt.bar([1, 2, 3, 4, 5], survey_answers)



def Analysis():
    data = load_data.Data('../..')
    # hist_emotion_facial_expressions(data, 1)
    # bar_chart_video_watch_similar(data, 1)
    # histogram_score(data,1)
    # bar_diagram_video_rating_total(data, 1)
    # bar_chart_video_watch_similar_total(data,2)
    plt.show()


if __name__ == '__main__':
    Analysis()
