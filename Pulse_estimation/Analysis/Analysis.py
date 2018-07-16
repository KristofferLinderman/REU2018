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


def scatter_genre_scores(data):
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
    for i in range(5):
        scores_amount_genre.append([])
        for j in range(5):
            scores_amount_genre[i].append(scores_genre[i].count((j + 1))**2.5)

    print(scores_amount_genre)
    genres = []
    #for i in range(len(intended_emotions)):
    #    genres.append([i + 1 for j in range(len(scores_genre[0]))])

    genres = [[i + 1 for j in range(5)] for i in range(5)]
    scores = [[j + 1 for j in range(5)] for i in range(5)]
    print genres
    plt.figure(1)
    plt.scatter(genres, scores, s=scores_amount_genre)
    plt.axes().set_title('Is there a correleation between the average score for a video and the rating given?')
    plt.axes().set_ylabel('Score')
    plt.axes().set_xticklabels(intended_emotions)
    plt.axes().set_xticks([1, 2, 3, 4, 5])
    plt.show()


def box_joy_video(data):
    names = stimuli_id.keys()
    names = sorted(names, key=lambda name: stimuli_id[name])

    joy = []
    for i in range(len(names)):
        joy.append(data.get_column_for_video('Joy_average', names[i]))

    plt.figure(1)
    plt.boxplot(joy)
    plt.axes().set_xticklabels(names)
    plt.show()


def hist_emotion_facial_expressions(data):
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

    plt.figure(1)

    plt.subplot(1, 5, 1)
    plt.bar(intended_emotions, facial_expressions_for_Joy)
    plt.title('Joyful video')

    plt.subplot(1, 5, 2)
    plt.bar(intended_emotions, facial_expressions_for_Sadness)
    plt.title('Sad video')

    plt.subplot(1, 5, 3)
    plt.bar(intended_emotions, facial_expressions_for_Anger)
    plt.title('Anger video')

    plt.subplot(1, 5, 4)
    plt.bar(intended_emotions, facial_expressions_for_Fear)
    plt.title('Fearful video')

    plt.subplot(1, 5, 5)
    plt.bar(intended_emotions, facial_expressions_for_Surprise)
    plt.title('Surprising video')

    plt.show()


def Analysis():
    data = load_data.Data('/home/gustaf/Downloads/data/final/')
    bar_diagram_video_rating(data)
    box_pulse_video(data)
    box_pulse_score(data)
    scatter_pulse_score(data)
    scatter_genre_scores(data)
    box_joy_video(data)
    hist_emotion_facial_expressions(data)


if __name__ == '__main__':
    Analysis()