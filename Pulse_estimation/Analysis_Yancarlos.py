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

file = open("Video Rating.csv")
dataFile = csv.reader(file)


def emotionCount(video):

    happiness = 0
    sadness = 0
    surprise = 0
    fear = 0
    anger = 0
    disgust = 0
    contempt = 0
    for line in dataFile:
        word = line[2]
        if video == line[5]:
            if "Happiness" in word:
                happiness += 1
            if "Sadness" in word:
                sadness += 1
            if "Surprise" in word:
                surprise += 1
            if "Fear" in word:
                fear += 1
            if "Anger" in word:
                anger += 1
            if "Disgust" in word:
                disgust += 1
            if "Contempt" in word:
                contempt += 1

    emotions = ["Happiness", "Sadness", "Surprise", "Fear", "Anger", "Disgust", "Contempt"]
    y_pos = np.arange(len(emotions))
    values = [happiness, sadness, surprise, fear, anger, disgust, contempt]
    for i in range(0,len(values)):
        values[i] = values[i] * 100 / 30
    plt.bar(y_pos, values, align='center', alpha=0.5)
    plt.xticks(y_pos, emotions)
    plt.ylabel("Percentage of users")
    plt.title("Emotions for Video " + str(video))

    plt.show()

    String = "Happiness: " + str(happiness) + "\n" \
        + "Sadness: " + str(sadness) + "\n" \
        + "Surprise: " + str(surprise) + "\n" \
        + "Fear: " + str(fear) + "\n" \
        + "Anger: " + str(anger) + "\n" \
        + "Disgust: " + str(disgust) + "\n" \
        + "Contempt: " + str(contempt) + "\n"

    print(String)

def dominant_emotion(video):
    happiness = 0
    sadness = 0
    surprise = 0
    fear = 0
    anger = 0
    disgust = 0
    contempt = 0

    for user in [i for i in range(1,31) if i != 13]:
        facefile = open("FacialData/" + str(user) + "-" + video + ".txt")
        for line in facefile:
            line = line.split()
            threshold = 50
            if line[9].isdigit() and len(line) > 15:
                if float(line[41]) > threshold + 20:
                    happiness += float(line[41])
                if float(line[39]) > threshold:
                    sadness += float(line[39])
                if float(line[42]) > threshold:
                    surprise += float(line[42])
                if float(line[43]) > threshold:
                    fear += float(line[43])
                if float(line[38]) > threshold:
                    anger += float(line[38])
                if float(line[40]) > threshold:
                    disgust += float(line[40])
                if float(line[44]) > threshold:
                    contempt += float(line[44])
        facefile.close()
    string = "Happiness: " + str(happiness) + "\n" \
             + "Sadness: " + str(sadness) + "\n" \
             + "Surprise: " + str(surprise) + "\n" \
             + "Fear: " + str(fear) + "\n" \
             + "Anger: " + str(anger) + "\n" \
             + "Disgust: " + str(disgust) + "\n" \
             + "Contempt: " + str(contempt) + "\n"
    print(string)
    return[happiness, sadness, surprise, fear, anger, disgust, contempt]

def common_emotion(video):
    happiness = 0
    sadness = 0
    surprise = 0
    fear = 0
    anger = 0
    disgust = 0
    contempt = 0

    for user in [i for i in range(1,31) if i != 13]:
        facefile = open("FacialData/" + str(user) + "-" + video + ".txt")
        for line in facefile:
            line = line.split()
            threshold = 10
            if line[9].isdigit() and len(line) > 15:
                if float(line[41]) > threshold:
                    happiness += 1
                if float(line[39]) > threshold:
                    sadness += 1
                if float(line[42]) > threshold:
                    surprise += 1
                if float(line[43]) > threshold:
                    fear += 1
                if float(line[38]) > threshold:
                    anger += 1
                if float(line[40]) > threshold:
                    disgust += 1
                if float(line[44]) > threshold:
                    contempt += 1
        facefile.close()
    string = "Happiness: " + str(happiness) + "\n" \
             + "Sadness: " + str(sadness) + "\n" \
             + "Surprise: " + str(surprise) + "\n" \
             + "Fear: " + str(fear) + "\n" \
             + "Anger: " + str(anger) + "\n" \
             + "Disgust: " + str(disgust) + "\n" \
             + "Contempt: " + str(contempt) + "\n"
    print(string)
    return[happiness, sadness, surprise, fear, anger, disgust, contempt]

def averageRating(video):
    users = 0
    total = 0
    file.seek(0)
    for line in dataFile:
        rating = line[3]
        if rating.isdigit() and video==line[5]:
            total += float(rating)
            users += 1
    return total/users

def SDRating(video):
    average = averageRating(video)
    sd = 0
    file.seek(0)
    for line in dataFile:
        rating = float(line[3])
        if video == line[5]:
            deviation = math.pow(rating - average, 2)
            sd += deviation
    return math.sqrt(sd/14)

def averageClicks(video):
    totalClicks = 0
    for i in range(1,31):
        if i != 20:
            filename = "data/" + str(i) + "/" + video + "/clicker.txt"
            file = open(filename)
            clicks = 0
            for line in file:
                clicks += 1
            totalClicks += float(clicks)
            file.close()
    return totalClicks/14

def SDClicks(video):
    average = averageClicks(video)
    sd = 0
    for i in range(1,31):
        if i != 20 and i % 2 == 0:
            filename = "data/" + str(i) + "/" + video + "/clicker.txt"
            file = open(filename)
            clicks = 0
            for line in file:
                clicks += 1
            deviation = math.pow(clicks - average,2)
            sd += deviation
            file.close()
    return math.sqrt(sd/14)

def clicksVSRating():
    file.seek(0)

    ratings1 = []
    ratings2 = []
    ratings3 = []
    ratings4 = []
    ratings5 = []
    clicks1 = []
    clicks2 = []
    clicks3 = []
    clicks4 = []
    clicks5 = []
    user = 1
    i = 1
    for line in dataFile:
        rating = float(line[3])
        video = line[5]
        clickerfile = open("data/" + str(user) + "/" + str(video) + "/clicker.txt")
        clicks = 0
        for line in clickerfile:
            clicks += 1
        if clicks != 0:
            if video == "1":
                ratings1.append(rating)
                clicks1.append(clicks)
            elif video == "2":
                ratings2.append(rating)
                clicks2.append(clicks)
            elif video == "3":
                ratings3.append(rating)
                clicks3.append(clicks)
            elif video == "4":
                ratings4.append(rating)
                clicks4.append(clicks)
            elif video == "5":
                ratings5.append(rating)
                clicks5.append(clicks)
        if i % 5 == 0:
            user += 1
        i += 1
        clickerfile.close()

    x1 = np.array(ratings1)
    y1 = np.array(clicks1)
    c1 = pearsonr(ratings1, clicks1)

    x2 = np.array(ratings2)
    y2 = np.array(clicks2)
    c2 = pearsonr(ratings2, clicks2)

    x3 = np.array(ratings3)
    y3 = np.array(clicks3)
    c3 = pearsonr(ratings3, clicks3)

    x4 = np.array(ratings4)
    y4 = np.array(clicks4)
    c4 = pearsonr(ratings4, clicks4)

    x5 = np.array(ratings5)
    y5 = np.array(clicks5)
    c5 = pearsonr(ratings5, clicks5)


    plt.scatter(y1, x1, s=100, c="r", marker="^", alpha=1)
    plt.title("Average vs Clicks\n Correlation: " + str(c1[0]))
    plt.xlabel("Clicks")
    plt.ylabel("Ratings")
    plt.xlim(0.5, 16.5)
    plt.ylim(0.5, 5.5)
    plt.show()
    plt.scatter(y2, x2, s=100, c="b", marker="s", alpha=1)
    plt.title("Average vs Clicks\n Correlation: " + str(c2[0]))
    plt.xlabel("Clicks")
    plt.ylabel("Ratings")
    plt.xlim(0.5, 16.5)
    plt.ylim(0.5, 5.5)
    plt.show()
    plt.scatter(y3, x3, s=100, c="g", marker="o", alpha=1)
    plt.title("Average vs Clicks\n Correlation: " + str(c3[0]))
    plt.xlabel("Clicks")
    plt.ylabel("Ratings")
    plt.xlim(0.5, 16.5)
    plt.ylim(0.5, 5.5)
    plt.show()
    plt.scatter(y4, x4, s=100, c="y", marker="P", alpha=1)
    plt.title("Average vs Clicks\n Correlation: " + str(c4[0]))
    plt.xlabel("Clicks")
    plt.ylabel("Ratings")
    plt.xlim(0.5, 16.5)
    plt.ylim(0.5, 5.5)
    plt.show()
    plt.scatter(y5, x5, s=100, c="m", marker="D", alpha=1)
    plt.title("Average vs Clicks\n Correlation: " + str(c5[0]))
    plt.xlabel("Clicks")
    plt.ylabel("Ratings")
    plt.xlim(0.5, 16.5)
    plt.ylim(0.5, 5.5)
    plt.show()

def readHeartData(user, video):

    # Open the files
    heartfile = open("data/" + user + "/" + video + "/heartdata.txt")
    clickerfile = open("data/" + user + "/" + video + "/clicker.txt")

    # Create a x and y arrays for heartrate
    values = []
    times = []
    start = None

    #Create x and y arrays for clicks
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
        for i in range(0,len(clicks)):
            click = round(clicks[i], 5)
            rate = round(timeStamp, 5)
            if click == rate and click not in seen:
                points.append(float(line[1]))
                moments.append(time)
                seen.append(click)

        if start == None:
            start = time
            time = datetime.timedelta()
        else:
            time = time - start
        times.append(float(j))
        j += 1

    x1 = np.array(times)
    y1 = np.array(values)

    x_smooth = np.linspace(x1.min(), x1.max(), 100)
    y_smooth = spline(x1, y1, x_smooth)

    plt.plot(x_smooth, y_smooth)
    plt.ylabel("Heart Rate")

    x2 = np.array(moments)
    y2 = np.array(points)
    plt.scatter(x2, y2, s=50, c="b", marker="o", alpha=1)


    heartfile.close()
    clickerfile.close()

def plot_common_emotions():
    emotions = ["Happiness", "Sadness", "Surprise", "Fear", "Anger", "Disgust", "Contempt"]
    video1_emotions = common_emotion("1")
    video2_emotions = common_emotion("2")
    video3_emotions = common_emotion("3")
    video4_emotions = common_emotion("4")
    video5_emotions = common_emotion("5")
    emotion_count = []
    for i in range(0, 7):
        emotion = [video1_emotions[i], video2_emotions[i], video3_emotions[i], video4_emotions[i], video5_emotions[i]]
        emotion_count.append(emotion)

    for i in range(0, 5):
        total = 0
        for j in range(0, 7):
            total += emotion_count[j][i]
        for j in range(0, 7):
            emotion_count[j][i] = emotion_count[j][i] * 100 / total

    plt.pie(video1_emotions, labels=emotions, autopct='%1.1f%%')
    plt.title("Interstellar")
    plt.axis("equal")
    plt.show()
    plt.pie(video2_emotions, labels=emotions, autopct='%1.1f%%')
    plt.title("Up")
    plt.axis("equal")
    plt.show()
    plt.pie(video3_emotions, labels=emotions, autopct='%1.1f%%')
    plt.title("Sherlock")
    plt.axis("equal")
    plt.show()
    plt.pie(video4_emotions, labels=emotions, autopct='%1.1f%%')
    plt.title("Watsons")
    plt.axis("equal")
    plt.show()
    plt.pie(video5_emotions, labels=emotions, autopct='%1.1f%%')
    plt.title("Fluffy")
    plt.axis("equal")
    plt.show()

def plot_dominant_emotions():
    emotions = ["Happiness", "Sadness", "Surprise", "Fear", "Anger", "Disgust", "Contempt"]
    video1_emotions = dominant_emotion("1")
    video2_emotions = dominant_emotion("2")
    video3_emotions = dominant_emotion("3")
    video4_emotions = dominant_emotion("4")
    video5_emotions = dominant_emotion("5")
    emotion_count = []
    for i in range(0, 7):
        emotion = [video1_emotions[i], video2_emotions[i], video3_emotions[i], video4_emotions[i], video5_emotions[i]]
        emotion_count.append(emotion)

    for i in range(0, 5):
        total = 0
        for j in range(0, 7):
            total += emotion_count[j][i]
        for j in range(0, 7):
            if total != 0:
                emotion_count[j][i] = emotion_count[j][i] * 100 / total
            else:
                emotion_count[j][i] = 0

    plt.pie(video1_emotions, labels=emotions, autopct='%1.1f%%')
    plt.title("Interstellar")
    plt.axis("equal")
    plt.show()
    #plt.pie(video2_emotions, labels=emotions, autopct='%1.1f%%')
    #plt.title("Up")
    #plt.axis("equal")
    #plt.show()
    #plt.pie(video3_emotions, labels=emotions, autopct='%1.1f%%')
    #plt.title("Sherlock")
    #plt.axis("equal")
    #plt.show()
    #plt.pie(video4_emotions, labels=emotions, autopct='%1.1f%%')
    #plt.title("Watsons")
    #plt.axis("equal")
    #plt.show()
    #plt.pie(video5_emotions, labels=emotions, autopct='%1.0f%%')
    #plt.title("Fluffy")
    #plt.axis("equal")
    #plt.show()

def relative_threshhold(user, video):
    file = open("FacialData/" + str(user) + "-" + video + ".txt")
    happiness = []
    sadness = []
    surprise = []
    fear = []
    anger = []
    disgust = []
    contempt = []
    for line in file:
        line = line.split()
        if line[9].isdigit() and len(line) > 15:
            happiness.append(float(line[41]))
            sadness.append(float(line[39]))
            surprise.append(float(line[42]))
            fear.append(float(line[43]))
            anger.append(float(line[38]))
            disgust.append(float(line[40]))
            contempt.append(float(line[44]))

    happiness.sort()
    happiness = happiness[int(len(happiness)*.8):]
    print("Happiness Lowest: " + str(happiness[0]) + "Highest: " + str(happiness[-1]))
    sadness.sort()
    sadness = sadness[int(len(sadness) * .8):]
    print("Sadness Lowest: " + str(sadness[0]) + "Highest: " + str(sadness[-1]))
    surprise.sort()
    surprise = surprise[int(len(surprise) * .8):]
    print("Surprise Lowest: " + str(surprise[0]) + "Highest: " + str(surprise[-1]))
    fear.sort()
    fear = fear[int(len(fear) * .8):]
    print("Fear Lowest: " + str(fear[0]) + "Highest: " + str(fear[-1]))
    anger.sort()
    anger = anger[int(len(anger) * .8):]
    print("Anger Lowest: " + str(anger[0]) + "Highest: " + str(anger[-1]))
    disgust.sort()
    disgust = disgust[int(len(disgust) * .8):]
    print("Disgust Lowest: " + str(disgust[0]) + "Highest: " + str(disgust[-1]))
    contempt.sort()
    contempt = contempt[int(len(contempt) * .8):]
    print("Contempt Lowest: " + str(contempt[0]) + "Highest: " + str(contempt[-1]))

    emotions = [happiness, sadness, surprise, fear, anger, disgust, contempt]
    values = [0, 0, 0, 0, 0, 0, 0]
    i = 0
    for emotion in emotions:
        total = 0
        for value in emotion:
             total += value
        values[i] = total
        i += 1
    emotionnames = ["Happiness", "Sadness", "Surprise", "Fear", "Anger", "Disgust", "Contempt"]
    plt.pie(values, labels=emotionnames, autopct='%1.1f%%')
    plt.title("Interstellar")
    plt.axis("equal")
    plt.show()

emotionCount("1")


