import csv
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
import numpy as np
import math
import datetime
import pytz
import matplotlib.dates as md
from scipy.stats.stats import pearsonr
from scipy.interpolate import spline

def count_file(user, video):
    facefile = open("FacialData/" + user + "-" + video + ".txt")
    heartfile = open("data/" + user + "/" + video + "/heartdata.txt")
    clickerfile = open("data/" + user + "/" + video + "/clicker.txt")
    line1 = 0
    for line in facefile:
        line1 += 1
    line2 = 0
    for line in heartfile:
        line2 += 1
    line3 = 0
    for line in clickerfile:
        line3 += 1
    print("Face lines:" + str(line1))
    print("Heart lines:" + str(line2))
    print("Clicker lines:" + str(line3))

def read_file(user, video):
    facefile = open("FacialData/" + user + "-" + video + ".txt")
    threshold = 10
    emotions = {"Happiness": 0, "Sadness": 0, "Surprise": 0, "Fear": 0, "Anger": 0, "Disgust": 0, "Contempt": 0, "Neutral": 0}
    time = []
    for line in facefile:
        line = line.split()
        values = {"Happiness": 0, "Sadness": 0, "Surprise": 0, "Fear": 0, "Anger": 0, "Disgust": 0, "Contempt": 0}
        if line[9].isdigit() and len(line) > 15:
            values["Happiness"] = float(line[41])
            values["Sadness"] = float(line[39])
            values["Surprise"] = float(line[42])
            values["Fear"] = float(line[43])
            values["Anger"] = float(line[38])
            values["Disgust"] = float(line[40])
            values["Contempt"] = float(line[44])
            sort = sorted(values, key=values.get, reverse=True)
            if values[sort[0]] > threshold:
                emotions[sort[0]] += 1
                time.append(sort[0])
            else:
                emotions["Neutral"] += 1
                time.append("Neutral")
    return time

def dominant_emotion(array):
    emotions = {"Happiness": 0, "Sadness": 0, "Surprise": 0, "Fear": 0, "Anger": 0, "Disgust": 0, "Contempt": 0}
    for value in array:
        if value == "Happiness":
            emotions["Happiness"] += 1
        elif value == "Sadness":
            emotions["Sadness"] += 1
        elif value == "Surprise":
            emotions["Surprise"] += 1
        elif value == "Fear":
            emotions["Fear"] += 1
        elif value == "Anger":
            emotions["Anger"] += 1
        elif value == "Disgust":
            emotions["Disgust"] += 1
        elif value == "Contempt":
            emotions["Contempt"] += 1

    sort = sorted(emotions, key=emotions.get, reverse=True)
    return sort[0]

def percent_users(video):
    emotion_names = ["Happiness", "Sadness", "Surprise", "Fear", "Anger", "Disgust", "Contempt"]
    emotions = [0] * 7
    for user in [i for i in range(1, 31) if i != 13]:
        dominant = dominant_emotion(read_file(str(user),video))
        if "Happiness" in dominant:
            emotions[0] += 1
        if "Sadness" in dominant:
            emotions[1] += 1
        if "Surprise" in dominant:
            emotions[2] += 1
        if "Fear" in dominant:
            emotions[3] += 1
        if "Anger" in dominant:
            emotions[4] += 1
        if "Disgust" in dominant:
            emotions[5] += 1
        if "Contempt" in dominant:
            emotions[6] += 1
    plt.pie(emotions, labels=emotion_names, autopct='%1.0f%%')
    plt.axis("equal")
    plt.show()
    return emotions

def get_heartrate(user, video):
    # Open the files
    heartfile = open("data/" + user + "/" + video + "/heartdata.txt")
    clickerfile = open("data/" + user + "/" + video + "/clicker.txt")

    # Create a x and y arrays for heartrate
    values = []
    times = []
    start = None

    # Create x and y arrays for clicks
    points = []
    moments = []
    j = 0

    clicks = []
    seen = []

    for line in clickerfile:
        line = line.split()
        clicks.append(float(line[0]))

    for line in heartfile:
        line = line.split()
        values.append(float(line[1]))
        timeStamp = float(line[0])
        time = md.num2date(timeStamp)
        for i in range(0, len(clicks)):
            click = round(clicks[i], 5)
            rate = round(timeStamp, 5)
            if click == rate and click not in seen:
                points.append(float(line[1]))
                moments.append(j)
                seen.append(click)

        if start == None:
            start = time
            time = datetime.timedelta()
        else:
            time = time - start
        times.append(float(j))
        j += 1

    return [[times,values],[moments,points]]

def plot_emotions(user, video):
    #Get emotion array
    emotions = read_file(user, video)

    things = get_heartrate(user, video)
    heartrate = things[0][1]
    times = things[0][0]
    hearttime = []
    clicks = things[1][1]
    moments = things[1][0]
    clicktime = []

    print(len(emotions))
    print(len(heartrate))
    modulo = int(float(len(emotions))/float(len(heartrate)))
    rate = float(len(emotions))/float(len(heartrate))

    # Generate x axis
    time = []
    j = 0
    previous = 0
    for i in range(0, len(emotions)):
        time.append(i)
        if i % modulo == 0 and len(hearttime) < len(heartrate):
            hearttime.append(previous + rate)
            if times[j] in moments:
                clicktime.append(previous + rate)
            previous += rate
            j += 1

    #Color array
    colors = []
    for value in emotions:
        if value == "Happiness":
            colors.append("lightgreen")
        elif value == "Sadness":
            colors.append("powderblue")
        elif value == "Surprise":
            colors.append("lemonchiffon")
        elif value == "Fear":
            colors.append("lightsalmon")
        elif value == "Anger":
            colors.append("lightcoral")
        elif value == "Disgust":
            colors.append("darkkhaki")
        elif value == "Contempt":
            colors.append("mediumpurple")
        else:
            colors.append("w")

    for i in range(0, len(time) - 1):
        plt.axvspan(time[i], time[i+1], facecolor=colors[i], alpha=0.5)

    x2 = np.array(hearttime)
    y2 = np.array(heartrate)

    x_smooth = np.linspace(x2.min(), x2.max(), 100)
    y_smooth = spline(x2, y2, x_smooth)

    plt.plot(x_smooth, y_smooth)

    x3 = np.array(clicktime)
    y3 = np.array(clicks)
    plt.scatter(x3, y3, s=50, c="k", marker="o", alpha=1)
    plt.title("Pulse vs. time")

    plt.show()

plot_emotions("22", "5")


