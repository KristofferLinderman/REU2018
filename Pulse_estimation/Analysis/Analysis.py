import load_data
import matplotlib.pyplot as plt
from static_values import *


def bar_diagram_video_rating(data):
    names = stimuli_id.keys()
    names = sorted(names, key=lambda name: stimuli_id[name])

    scores = {}
    for name in names:
        scores[name] = []

    for name in names:
        survey_scores = data.get_survey_question_for_video(name, 'One a scale of 1 to 5, how would you rate the video?')
        for i in range(1, 6):
            scores[name].append(0)
            for s in survey_scores:
                if s == i:
                    scores[name][i - 1] = scores[name][i - 1] + 1

    plt.figure(1)
    for i in range(len(names)):
        plt.subplot(3, 5, i + 1)
        plt.title('Rating of \"' + names[i] + '\"')
        plt.bar([1, 2, 3, 4, 5], scores[names[i]])
    plt.subplots_adjust(top=0.92, bottom=0.08)
    plt.show()


def box_pulse_video(data):
    names = stimuli_id.keys()
    names = sorted(names, key=lambda name: stimuli_id[name])
    pulse = []
    for name in names:
        pulse.append(data.get_column_for_video('Pulse_derivative_average', name))

    plt.figure(1)
    plt.boxplot(pulse)
    names = [(name + '\n' + intended_emotions[((stimuli_id[name] - 1) / 3)]) for name in names]
    plt.axes().set_xticklabels(names)
    plt.axes().set_title('Is there a correlation between the average change in pulse during a video and the video category?')
    plt.axes().set_ylabel('average change in pulse during video [bpm/s]')
    plt.show()


def box_pulse_score(data):
    names = stimuli_id.keys()
    names = sorted(names, key=lambda name: stimuli_id[name])
    pulse = []
    scores = []
    for name in names:
        pulse.extend(data.get_column_for_video('Pulse_derivative_average', name))
        scores.extend(data.get_column_for_video('One a scale of 1 to 5, how would you rate the video?', name))

    pulse_new = []
    for i in range(1, 6):
        pulse_new.append([pulse[j] for j in range(len(pulse)) if scores[j] == i])

    plt.figure(1)
    plt.boxplot(pulse_new)
    names = [1, 2, 3, 4, 5]
    plt.axes().set_xticklabels(names)
    plt.axes().set_title('Is there a correlation between the pulse derivative average and the score given')
    plt.axes().set_ylabel('average change in pulse during video [bpm/s]')
    plt.axes().set_xlabel('Score')
    plt.show()


def scatter_pulse_score(data):
    names = stimuli_id.keys()
    names = sorted(names, key=lambda name: stimuli_id[name])
    pulse = []
    scores = []
    for name in names:
        pulse.extend(data.get_column_for_video('Pulse_derivative_average', name))
        scores.extend(data.get_column_for_video('One a scale of 1 to 5, how would you rate the video?', name))

    plt.figure(1)
    plt.scatter(scores, pulse)
    plt.show()

def Analysis():
    data = load_data.Data('/home/gustaf/Downloads/data/final/')



if __name__ == '__main__':
    Analysis()