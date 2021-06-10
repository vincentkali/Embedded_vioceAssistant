# -*- coding: utf-8 -*-
from dataBase import DataBase
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
    way = input("Hi, which way you want to login? password/face/sound\n")
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
        userName = input("Please input your user name\n")
        password = input("Please input your password\n")
        flag = db.login_password(userName, password)
        
        if flag == True:
            user = userName
    
    return flag
        
##### add user #####
def adduser():
    global user
    global db
    global debug
    userName = input("Please input your user name\n")
    db.add_user(userName)
    password = input("input password\n")
    db.add_password(userName, password)
    
    flag = input("want face ID?\n")
    if flag == "yes":
        faceID = get_faceID()
        db.add_faceID(userName, faceID)
        if debug: print("get your face ID\n")
    
    flag = input("want sound ID?\n")
    if flag == "yes":
        if debug: print("get your sound ID\n")
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
        userName = input("Please input the user name which you want to delete\n")
        db.delete_user(userName)
    elif opration == "light up" :
        if debug: print("light up\n")
    elif opration == "set clock time" :
        clocktTime = input("input the clock time\n")
        #db.put_clockTime(user, clocktTime)
        if debug: print("clockTime "+clocktTime+"\n")
    elif opration == "clock up" :
        if debug: print("clock up\n")
    elif opration == "play song" :
        if debug: print("play song\n")
    else:
        if debug: print("Unkonw command\n")

##### initial setup #####
def init_setup():
    # create song diractory
    # create record diractory
    pass
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
    if debug: print("buzzer\n")

def alarm_lightTwinkle():
    global debug
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
            opration = input("Hi, do you want to login or add user?\n")
            if opration == "login":
                flag = login()
                if flag == False:
                    alarm()
            elif opration == "adduser":
                adduser()
            else:
                if debug: print("Unkown command\n")
        else:
            opration = input("Hi "+user+", how can I help you?\n")
            if opration == "logout":
                logout()
            else:
                using()
except KeyboardInterrupt:
    pass
