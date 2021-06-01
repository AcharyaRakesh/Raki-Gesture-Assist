import cv2
import numpy as np
import time
import os
import hand as hd
from playsound import playsound
import text as tx
import speech_recognition as sr
import datetime
import wikipedia

import pyttsx3
import pywhatkit
import pyjokes
from pydub import AudioSegment
import sounddevice as sd
from scipy.io.wavfile import write





# Sampling frequency
freq = 48000

# Recording duration
duration = 5



listener = sr.Recognizer()

engine = pyttsx3.init()

#voices = engine.getProperty('voices')
#engine.setProperty('voice', voices[1].id)  # for female voice



def talk(text):
    engine.say(text)
    engine.runAndWait()




folder_path = "Header"

l=0
brushThick = 10
ereserThick = 100

mylist = os.listdir(folder_path)
font = cv2.FONT_HERSHEY_DUPLEX

# print(mylist)

overlaylist = []




imgCanva = np.zeros((720, 1280, 3), np.uint8)
for imPath in mylist:
    image = cv2.imread(f'{folder_path}/{imPath}')
    overlaylist.append(image)

# print(len(overlaylist))
header = overlaylist[0]

drawColor = (255, 0, 255)

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = hd.handdetector(detectionCon=0.85)
x0, y0 = 0, 0

while True:
    sucess, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmlist = detector.findimg(img, draw=False)

    if len(lmlist) != 0:
        # print(lmlist)

        # tip of Index
        x1, y1 = lmlist[8][1:]
        x2, y2 = lmlist[12][1:]

        fingers = detector.fingertipUp()
        # print(fingers)

        if fingers[1] and fingers[2]:
            x0, y0 = 0, 0

            # print('selection')
            # Checking Click
            if y1 < 125:
                if 0 < x1 < 425:
                    header = overlaylist[0]
                    drawColor = (255, 0, 255)


                elif 430 < x1 < 845:
                    header = overlaylist[1]
                    drawColor = (0, 0, 0)

                elif 845 < x1 < 1280:
                    header = overlaylist[2]
                    drawColor = (255, 0, 0)
                    img_name1 = "raki{}.png".format(l)
                    cv2.imwrite(img_name1, imgin)
                    imtext1 = tx.textimg(img_name1)
                    imtext1 = imtext1.strip('\n')
                    if imtext1 == "song" or imtext1 == "Song":
                        pywhatkit.playonyt("song")
                    elif imtext1 == "raki" or imtext1 == "Raki":
                        talk('Hai Iam Raki, How can i help you')
                    elif imtext1 == 'time':
                        time = datetime.datetime.now().strftime('%I:%M:%S %p')
                        talk('time is' + time)
                    elif 'who' in imtext1:
                        talk("I'm a hand gesture detector ")
                    elif 'are' in imtext1:
                        talk("No I'm in relationship with alexa, Alexa I Love you ")

                    elif imtext1 == "help" or imtext1 == "HELP":
                        playsound("Alert1.wav")
                    elif imtext1 == 'jokes' or imtext1 == "JOKES":
                        talk(f"{pyjokes.get_joke()}")

                    else:
                        talk('Sorry I dint get')
                    print(imtext1)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    #cv2.putText(img, imtext1, (10, 500), font, 3, (255, 255, 255), 7, cv2.LINE_AA)
                    #engine.say(f"{imtext1}")
                    l=l+1

            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

        if fingers[1] and fingers[2] == False:

            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            # print('drawing')
            if x0 == 0 and y0 == 0:
                x0, y0 = x1, y1

            if drawColor == (0, 0, 0):
                cv2.line(img, (x0, y0), (x1, y1), drawColor, ereserThick)
                cv2.line(imgCanva, (x0, y0), (x1, y1), drawColor, ereserThick)
            else:
                cv2.line(img, (x0, y0), (x1, y1), drawColor, brushThick)
                cv2.line(imgCanva, (x0, y0), (x1, y1), drawColor, brushThick)

            x0, y0 = x1, y1

    imgGray = cv2.cvtColor(imgCanva, cv2.COLOR_BGR2GRAY)
    _, imgin = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgin = cv2.cvtColor(imgin, cv2.COLOR_GRAY2RGB)
    img = cv2.bitwise_and(img, imgin)
    img = cv2.bitwise_or(img, imgCanva)

    img[0:125, 0:1280] = header
    # img =cv2.addWeighted(img,0.5,imgCanva,0.5,0)
    cv2.imshow('imge', img)
    # cv2.imshow('imgC', imgCanva)
    cv2.waitKey(100)

    # print(img.shape)
    # print(imgCanva.shape)
