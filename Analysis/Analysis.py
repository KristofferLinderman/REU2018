import matplotlib

import load_data
import matplotlib.pyplot as plt
from static_values import *


def bar_diagram_video_rating(data, figure_number):
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

    plt.figure(figure_number)
    subplots = []
    order = [1, 6, 11, 2, 7, 12, 3, 8, 13, 4, 9, 14, 5, 10, 15]
    for i in range(len(names)):
        subplots.append(plt.subplot(3, 5, order[i]))
        plt.title('Rating of \"' + names[i] + '\"')
        plt.bar([1, 2, 3, 4, 5], scores[names[i]])
    for sub in subplots:
        sub.set_ylim(0, 15)
    plt.subplots_adjust(top=0.92, bottom=0.08)


def box_pulse_video(data, figure_number):
    names = stimuli_id.keys()
    names = sorted(names, key=lambda name: stimuli_id[name])
    pulse = []
    for name in names:
        pulse.append(data.get_column_for_video('Pulse_derivative_average', name))

    plt.figure(figure_number)
    plt.boxplot(pulse)
    names = [(name + '\n' + intended_emotions[((stimuli_id[name] - 1) / 3)]) for name in names]
    plt.axes().set_xticklabels(names)
    #plt.axes().set_title('Is there a correlation between the average change in pulse during a video and the video category?')
    plt.axes().set_ylabel('average change in pulse during video [bpm/s]')


def box_pulse_score(data, figure_number):
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

    plt.figure(figure_number)
    plt.boxplot(pulse_new)
    names = [1, 2, 3, 4, 5]
    plt.axes().set_xticklabels(names)
    #plt.axes().set_title('Is there a correlation between the pulse derivative average and the score given')
    plt.axes().set_ylabel('average change in pulse during video [bpm/s]')
    plt.axes().set_xlabel('Rating')


def scatter_pulse_score(data, figure_number):
    names = stimuli_id.keys()
    names = sorted(names, key=lambda name: stimuli_id[name])
    pulse = []
    scores = []
    for name in names:
        pulse.extend(data.get_column_for_video('Pulse_derivative_average', name))
        scores.extend(data.get_column_for_video('One a scale of 1 to 5, how would you rate the video?', name))

    plt.figure(figure_number)
    plt.scatter(scores, pulse)
    plt.title('Pulse derivative average vs the score')
    plt.axes().set_ylabel('Pulse derivative average [bpm / s]')
    plt.axes().set_xlabel('Score')


def scatter_genre_scores(data, figure_number):
    names = stimuli_id.keys()
    names = sorted(names, key=lambda name: stimuli_id[name])
    scores = []
    for name in names:
        scores.append(data.get_column_for_video('One a scale of 1 to 5, how would you rate the video?', name))

    scores_genre = []
    for i in range(5):
        scores_genre.append([])
        scores_genre[i].extend(scores[i * 3])
        scores_genre[i].extend(scores[(i * 3)+ 1])
        scores_genre[i].extend(scores[(i * 3) + 2])

    scores_amount_genre = []
    annotation = []

    for i in range(5):
        scores_amount_genre.append([])
        annotation.append([])
        for j in range(5):
            scores_amount_genre[i].append(scores_genre[i].count((j + 1)) ** 2.5)
            annotation[i].append(scores_genre[i].count((j + 1)))

    print(scores_amount_genre)
    genres = []
    #for i in range(len(intended_emotions)):
    #    genres.append([i + 1 for j in range(len(scores_genre[0]))])

    genres = [[i + 1 for j in range(5)] for i in range(5)]
    scores = [[j + 1 for j in range(5)] for i in range(5)]
    print genres
    matplotlib.rcParams.update({'font.size': 22})
    plt.figure(figure_number)
    plt.scatter(genres, scores, s=scores_amount_genre,color='#6699ff')
    #plt.axes().set_title('Is there a correleation between the average score for a video and the rating given?')
    plt.axes().set_ylabel('Rating')
    plt.axes().set_xticklabels(intended_emotions)
    plt.axes().set_xticks([1, 2, 3, 4, 5])
    for i in range(5):
        for j in range(5):
            if annotation[i][j] == 0:
                continue
            plt.axes().annotate(str(annotation[i][j] * 100 / sum(annotation[i])) + '%', xy=(i + 1, j + 1))


def box_joy_video(data, figure_number):
    names = stimuli_id.keys()
    names = sorted(names, key=lambda name: stimuli_id[name])

    joy = []
    for i in range(len(names)):
        joy.append(data.get_column_for_video('Joy_average', names[i]))

    plt.figure(figure_number)
    plt.boxplot(joy)
    plt.axes().set_xticklabels(names)


def hist_emotion_facial_expressions(data, figure_number):
    names = stimuli_id.keys()
    names = sorted(names, key=lambda name: stimuli_id[name])

    facial_expressions_for_Joy = []
    for i in range(len(intended_emotions)):
        facial_expressions_for_Joy.append([])
        facial_expressions_for_Joy[i].extend(data.get_column_for_video(intended_emotions[i] + '_average', 'Noah'))
        facial_expressions_for_Joy[i].extend(data.get_column_for_video(intended_emotions[i] + '_average', 'Cat'))
        facial_expressions_for_Joy[i].extend(data.get_column_for_video(intended_emotions[i] + '_average', 'Despicable'))
    for i in range(len(intended_emotions)):
        facial_expressions_for_Joy[i] = sum(facial_expressions_for_Joy[i]) / len(facial_expressions_for_Joy[i])

    facial_expressions_for_Sadness = []
    for i in range(len(intended_emotions)):
        facial_expressions_for_Sadness.append([])
        facial_expressions_for_Sadness[i].extend(data.get_column_for_video(intended_emotions[i] + '_average', 'Dog'))
        facial_expressions_for_Sadness[i].extend(data.get_column_for_video(intended_emotions[i] + '_average', 'Forest'))
        facial_expressions_for_Sadness[i].extend(data.get_column_for_video(intended_emotions[i] + '_average', 'Interstellar'))
    for i in range(len(intended_emotions)):
        facial_expressions_for_Sadness[i] = sum(facial_expressions_for_Sadness[i]) / len(facial_expressions_for_Sadness[i])

    facial_expressions_for_Anger = []
    for i in range(len(intended_emotions)):
        facial_expressions_for_Anger.append([])
        facial_expressions_for_Anger[i].extend(data.get_column_for_video(intended_emotions[i] + '_average', 'Wheelchair'))
        facial_expressions_for_Anger[i].extend(data.get_column_for_video(intended_emotions[i] + '_average', 'Help'))
        facial_expressions_for_Anger[i].extend(data.get_column_for_video(intended_emotions[i] + '_average', 'Amish'))
    for i in range(len(intended_emotions)):
        facial_expressions_for_Anger[i] = sum(facial_expressions_for_Anger[i]) / len(facial_expressions_for_Anger[i])

    facial_expressions_for_Fear = []
    for i in range(len(intended_emotions)):
        facial_expressions_for_Fear.append([])
        facial_expressions_for_Fear[i].extend(data.get_column_for_video(intended_emotions[i] + '_average', 'Iguana'))
        facial_expressions_for_Fear[i].extend(data.get_column_for_video(intended_emotions[i] + '_average', 'Shining'))
        facial_expressions_for_Fear[i].extend(data.get_column_for_video(intended_emotions[i] + '_average', 'Dino'))
    for i in range(len(intended_emotions)):
        facial_expressions_for_Fear[i] = sum(facial_expressions_for_Fear[i]) / len(facial_expressions_for_Fear[i])

    facial_expressions_for_Surprise = []
    for i in range(len(intended_emotions)):
        facial_expressions_for_Surprise.append([])
        facial_expressions_for_Surprise[i].extend(data.get_column_for_video(intended_emotions[i] + '_average', 'Magic Bird'))
        facial_expressions_for_Surprise[i].extend(data.get_column_for_video(intended_emotions[i] + '_average', 'Flying'))
        facial_expressions_for_Surprise[i].extend(data.get_column_for_video(intended_emotions[i] + '_average', 'Cocaine'))
    for i in range(len(intended_emotions)):
        facial_expressions_for_Surprise[i] = sum(facial_expressions_for_Surprise[i]) / len(facial_expressions_for_Surprise[i])

    plt.figure(figure_number)

    a = plt.subplot(1, 5, 1)
    plt.bar(intended_emotions, facial_expressions_for_Joy)
    plt.title('Joyful video')

    b = plt.subplot(1, 5, 2)
    plt.bar(intended_emotions, facial_expressions_for_Sadness)
    plt.title('Sad video')

    c = plt.subplot(1, 5, 3)
    plt.bar(intended_emotions, facial_expressions_for_Anger)
    plt.title('Anger video')

    d = plt.subplot(1, 5, 4)
    plt.bar(intended_emotions, facial_expressions_for_Fear)
    plt.title('Fearful video')

    e = plt.subplot(1, 5, 5)
    plt.bar(intended_emotions, facial_expressions_for_Surprise)
    plt.title('Surprising video')

    ylim = max(a.get_ylim(), max(b.get_ylim(), max(c.get_ylim(), max(d.get_ylim(), e.get_ylim()))))
    a.set_ylim(ylim)
    b.set_ylim(ylim)
    c.set_ylim(ylim)
    d.set_ylim(ylim)
    e.set_ylim(ylim)


def box_video_facial_expression(data, figure_number):
    names = stimuli_id.keys()
    names = sorted(names, key=lambda name: stimuli_id[name])

    facial_expressions_for_video = []
    for i in range(1, 16):
        facial_expressions_for_video.append([])
        for j in range(len(intended_emotions)):
            facial_expressions_for_video[i - 1].append(data.get_column_for_video(intended_emotions[j] + '_average', id_stimuli[i]))

    plt.figure(figure_number)

    subplots = []
    order = [1, 6, 11, 2, 7, 12, 3, 8, 13, 4, 9, 14, 5, 10, 15]
    for i in range(len(facial_expressions_for_video)):
        subplots.append(plt.subplot(3, 5, order[i]))
        plt.title(names[i])
        plt.boxplot(facial_expressions_for_video[i])
        subplots[i].set_xticklabels(intended_emotions)
        if i < 3:
            subplots[i].set_ylim(0, 100)
        if i >= 3 and i < 6:
            subplots[i].set_ylim(0, 40)
        if (i + 1) % 3 == 1:
            subplots[i].annotate(intended_emotions[((i + 1) / 3)],
                                 xy=(0.4, 1.2),
                                 xycoords='axes fraction',
                                 size='large',
                                 annotation_clip=False)
    plt.subplots_adjust(top=0.92, bottom=0.08)


def scatter_abs_pulse_score(data, figure_number):
    names = stimuli_id.keys()
    names = sorted(names, key=lambda name: stimuli_id[name])
    pulse = []
    scores = []
    for name in names:
        pulse.extend(data.get_column_for_video('Pulse_derivative_abs_average', name))
        scores.extend(data.get_column_for_video('One a scale of 1 to 5, how would you rate the video?', name))

    plt.figure(figure_number)
    plt.scatter(scores, pulse)
    plt.title('Absolute value of pulse derivative average vs the score')
    plt.axes().set_ylabel('Absolute value of pulse derivative average [bpm / s]')
    plt.axes().set_xlabel('Score')


def Analysis():
    data = load_data.Data('../..')
    # bar_diagram_video_rating(data, 1)
    # box_pulse_video(data, 2)
    # box_pulse_score(data, 3)
    # scatter_pulse_score(data, 4)
    scatter_genre_scores(data, 5)
    # box_joy_video(data, 6)
    # hist_emotion_facial_expressions(data, 7)
    # box_video_facial_expression(data, 8)
    plt.show()


if __name__ == '__main__':
    Analysis()