import csv
import os
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


def bar_diagram_video_rating_selective(data, figure_number, video_names):
    scores = {}
    for name in video_names:
        scores[name] = []

    for name in video_names:
        survey_scores = data.get_survey_question_for_video(name, 'One a scale of 1 to 5, how would you rate the video?')
        for i in range(1, 6):
            scores[name].append(0)
            for s in survey_scores:
                if s == i:
                    scores[name][i - 1] = scores[name][i - 1] + 1

    plt.figure(figure_number)
    subplots = []
    order = [1, 6, 11, 2, 7, 12, 3, 8, 13, 4, 9, 14, 5, 10, 15]
    graph_rows = 1
    graph_columns = 1
    matplotlib.rcParams.update({'font.size': 22})
    for i in range(len(video_names)):
        subplots.append(plt.subplot(graph_rows, graph_columns, order[i]))
        plt.title('Rating of \"' + video_names[i] + '\"')
        plt.xlabel('Rating')
        plt.ylabel('Number of Votes')
        plt.bar([1, 2, 3, 4, 5], scores[video_names[i]])
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
    # plt.axes().set_title('Is there a correlation between the average change in pulse during a video and the video category?')
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
    # plt.axes().set_title('Is there a correlation between the pulse derivative average and the score given')
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
        scores_genre[i].extend(scores[(i * 3) + 1])
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
    # for i in range(len(intended_emotions)):
    #    genres.append([i + 1 for j in range(len(scores_genre[0]))])

    genres = [[i + 1 for j in range(5)] for i in range(5)]
    scores = [[j + 1 for j in range(5)] for i in range(5)]
    print genres
    matplotlib.rcParams.update({'font.size': 22})
    plt.figure(figure_number)
    plt.scatter(genres, scores, s=scores_amount_genre, color='#6699ff')
    # plt.axes().set_title('Is there a correleation between the average score for a video and the rating given?')
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
        facial_expressions_for_Sadness[i].extend(
            data.get_column_for_video(intended_emotions[i] + '_average', 'Interstellar'))
    for i in range(len(intended_emotions)):
        facial_expressions_for_Sadness[i] = sum(facial_expressions_for_Sadness[i]) / len(
            facial_expressions_for_Sadness[i])

    facial_expressions_for_Anger = []
    for i in range(len(intended_emotions)):
        facial_expressions_for_Anger.append([])
        facial_expressions_for_Anger[i].extend(
            data.get_column_for_video(intended_emotions[i] + '_average', 'Wheelchair'))
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
        facial_expressions_for_Surprise[i].extend(
            data.get_column_for_video(intended_emotions[i] + '_average', 'Magic Bird'))
        facial_expressions_for_Surprise[i].extend(
            data.get_column_for_video(intended_emotions[i] + '_average', 'Flying'))
        facial_expressions_for_Surprise[i].extend(
            data.get_column_for_video(intended_emotions[i] + '_average', 'Cocaine'))
    for i in range(len(intended_emotions)):
        facial_expressions_for_Surprise[i] = sum(facial_expressions_for_Surprise[i]) / len(
            facial_expressions_for_Surprise[i])

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
            facial_expressions_for_video[i - 1].append(
                data.get_column_for_video(intended_emotions[j] + '_average', id_stimuli[i]))

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


def scatter_smile_contempt(data, figure_number):
    smile = []
    contempt = []
    for i in range(15):
        smile.extend(data.get_column_for_video('Smile_average', id_stimuli[i + 1]))
        contempt.extend(data.get_column_for_video('Contempt_average', id_stimuli[i + 1]))

    plt.figure(figure_number)
    plt.scatter(smile, contempt)
    plt.axes().set_ylabel('Contempt')
    plt.axes().set_xlabel('Smile')


def bar_diagram_video_rating_total_binarized(data, figure_number):
    names = stimuli_id.keys()
    names = sorted(names, key=lambda name: stimuli_id[name])

    scores = [0, 0]

    for name in names:
        survey_scores = data.get_survey_question_for_video(name, 'One a scale of 1 to 5, how would you rate the video?')
        for s in survey_scores:
            scores[s / 4] = scores[s / 4] + 1

    plt.figure(figure_number)

    plt.title('One a scale of 1 to 5, how would you rate the video?')
    plt.xlabel('Score')
    plt.ylabel('Number of votes')
    plt.bar(['1-3', '4-5'], scores)

    print scores
    print sum(scores)


def plot_one_pulse_file(filename, figurenum):
    time = []
    pulse = []
    with open(filename) as f:
        for line in f:
            line = line.replace('(', '').replace(')', '')
            line = line.split(' ')
            time.append(line[0])
            pulse.append(line[1])

    pulse = [
        (float(pulse[i]) + float(pulse[i - 1]) + float(pulse[i - 2]) + float(pulse[i - 3]) + float(pulse[i - 4])) / 5
        for i in range(5, len(pulse))]
    plt.figure(figurenum)
    plt.plot(time[4:len(time) - 1], pulse)


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

    # The results from running above code, saved here to make it run faster
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
    data = load_data.Data('/home/gustaf/Downloads/data/final/')
    # bar_diagram_video_rating(data, 1)
    # box_pulse_video(data, 2)
    # box_pulse_score(data, 3)
    # scatter_pulse_score(data, 4)
    # scatter_genre_scores(data, 5)
    # box_joy_video(data, 6)
    # hist_emotion_facial_expressions(data, 7)
    # box_video_facial_expression(data, 8)
    # scatter_smile_contempt(data, 9)
    # bar_diagram_video_rating_total_binarized(data, 10)

    # hist_emotion_facial_expressions(data, 1)
    # bar_chart_video_watch_similar(data, 1)
    # bar_chart_video_watch_similar_selective(data, 1,['Despicable','Dog'])
    # bar_chart_video_watch_similar_selective(data, 1, ['Shining'], 1, 1)
    # histogram_score(data,1)
    # bar_diagram_video_rating_total(data, 1)
    # bar_chart_video_watch_similar_total(data,2)

    # prepare_face_files()
    # calculate_percentage_of_face()
    plot_one_pulse_file('/home/gustaf/Downloads/data/1/pulse_files/pulse_Amish_1.txt', 11)
    plt.show()


if __name__ == '__main__':
    Analysis()
