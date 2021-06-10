# -*- coding: utf-8 -*-
from dataBase import DataBase
import fun
import os
import picamera
import time
from math import sqrt

from imutils import face_utils
import numpy as np
import imutils
import dlib
import cv2

import picamera
import time
from gtts import gTTS
import os
import RPi.GPIO as GPIO
import time
from threading import Thread
import speech_recognition as sr
import librosa
import matplotlib.pyplot as plt
import numpy as np
import librosa.display


global mfccs
global text
##LED
LED_PIN = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_PIN, GPIO.OUT)
 
def txt2voice(talk: str):
    tts = gTTS(text=talk, lang='en')
    print(tts)
    tts.save('txt2voice.mp3')
    os.system('omxplayer -o local -p txt2voice.mp3 > /dev/null 2>&1')

def voice2txt():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        os.system('omxplayer -o local -p say.mp3 > /dev/null 2>&1')
        audio =r.listen(source)
        talk = r.recognize_google(audio,language="en")
        print(talk)
        return talk

def LED_on():
    GPIO.output(LED_PIN, GPIO.HIGH)
    os.system('omxplayer -o local -p LEDon.mp3 > /dev/null 2>&1')

def LED_off():
    GPIO.output(LED_PIN, GPIO.LOW)
    os.system('omxplayer -o local -p LEDoff.mp3 > /dev/null 2>&1')

def music():
    os.system('omxplayer -o local -p music1.mp3 > /dev/null 2>&1')

def record():
    os.system('omxplayer -o local -p say.mp3 > /dev/null 2>&1')
    os.system('arecord  -f cd -d 3 record.mp3')

def play_record():
    os.system('omxplayer -o local -p record.mp3 > /dev/null 2>&1')

def get_faceID():
    global camera
    image_file = "img.jpg"
    detector_file = "model/haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(detector_file)
    predictor_file = "model/shape_predictor_68_face_landmarks.dat"
    predictor = dlib.shape_predictor(predictor_file)
    
    time.sleep(1)
    camera.capture(image_file)
    
    image = cv2.imread(image_file)
    image = imutils.resize(image, width=500)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
        minNeighbors=5, minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE)  
    
    face_counter = 0
    for (x, y, w, h) in rects:
        rect = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))
    
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        shape = list(shape)
        print(shape)
        print(len(shape))
        print(shape[0])
        print(shape[0][0])
        face_counter = face_counter + 1
    return shape

def lineNotifyMessage(token, msg):
    global debug
    camera = picamera.PiCamera()
    time.sleep(2) # Camera warm-up time
    camera.capture('image.jpg')

    
    os.system("curl -X POST https:/notify-api.line.me/api/notify \
              -H 'Authorization: Bearer "+ token+"' \
              -F 'message=" + msg + "' -F 'imageFile=@./image.jpg' ")
        
##### login #####
def login():
    global user
    global db
    global debug
    #way = input("Hi, which way you want to login?") # password/face/sound
    txt2voice("Hi which way you want to login")
    way = voice2txt()
    flag = False
    if way == "face":
        
        faceID = get_faceID()
        
        userName = db.login_faceID(faceID)
        if userName != None:
            flag = True
            user = userName
    elif way == "sound":
        # getsound
        soundID = None # get faceID
        
        
        userName = db.login_faceID(soundID)
        if userName != False:
            flag = True
            user = userName
    elif way == "password":
        #userName = input("Please input your user name")
        txt2voice("Please input your user name")
        userName = voice2txt()
        
        txt2voice("Please input your password")
        password = input()
        flag = db.login_password(userName, password)
        
        if flag == True:
            user = userName
    
    return flag
        
##### add user #####
def adduser():
    global user
    global db
    global debug
    #userName = input("Please input your user name")
    txt2voice("Please input your user name")
    userName = voice2txt()
    db.add_user(userName)
    #password = input("input password\n")
    txt2voice("input password\n")
    password = input()
    db.add_password(userName, password)
    
    #flag = input("do you want to use face ID")
    txt2voice("do you want to use face ID")
    flag = voice2txt()
    if flag == "yes":
        faceID = get_faceID()
        db.add_faceID(userName, faceID)
        if debug: print("get your face ID\n")
    
def logout():
    global user
    global db
    global debug
    user = "guest"
    if debug: print("Success logout")

def using():
    global user
    global db
    global opration
    global debug
    
    if opration == "delete user":
        #userName = input("Please input the user name which you want to delete")
        txt2voice("Please input the user name which you want to delete")
        userName = voice2txt()
        db.delete_user(userName)
        
    elif opration == "light up" :
        LED_on()
        if debug: print("light up\n")
        
    elif opration == "light off" :
        LED_off()
        if debug: print("light off\n")
    
    elif opration == "play song" :
        music()
        if debug: print("play song\n")
    
    elif opration == "record" :
        record()
        if debug: print("record")
    
    elif opration == "play record" :
        play_record()
        if debug: print("play record\n")
    
    else:
        if debug: print("Unkonw command\n")

############ alarm function (if login failure)#############
def alarm_lineNotify():
    global db
    global debug
    msg = "Alert!! This person attempt to login\n"
    for userName in db.get_all_userName():
        token = db.get_lineToken(userName)
        lineNotifyMessage(token, msg)
    if debug: print("line notify\n")

def alarm_buzzer():
    global debug
    os.system('omxplayer -o local -p alarm.mp3 > /dev/null 2>&1')
    if debug: print("buzzer\n")

def alarm_lightTwinkle():
    global debug
    LED_PIN = 12
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LED_PIN, GPIO.OUT)
 
    for i in range(1,10): 
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(0.25)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(0.25)
    if debug: print("light twinkle")

def alarm():
    alarm_lineNotify()
    alarm_buzzer()
    alarm_lightTwinkle()

##### main #####
opration = "login" # login, using, adduser
user = "guest"
db = DataBase()
db.add_user("admin")
db.add_password("admin", "admin")
db.put_lineToken("admin", "KeSXfKSpZCtL0scXNdeaapuvn45FmbSBMAZVIEN4h1m")

debug = True

camera = picamera.PiCamera()
try:
    while(True):
        if user == "guest":
            #opration = input("Hi do you want to login or add user")
            txt2voice("Hi do you want to login or add user")
            opration = voice2txt()
            if opration == "login":
                flag = login()
                if flag == False:
                    alarm()
            elif opration == "adduser":
                adduser()
            else:
                if debug: print("Unkown command\n")
        else:
            #opration = input("Hi "+user+", how can I help you?\n")
            txt2voice("Hi "+user+" how can I help you")
            opration = voice2txt()
            if opration == "logout":  
                logout()
            else:
                using()
except KeyboardInterrupt:
    pass
