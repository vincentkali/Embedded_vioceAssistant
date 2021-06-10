# -*- coding: utf-8 -*-
from dataBase import DataBase
from raspberryPi import *
import os
import picamera
import time


def lineNotifyMessage(token, msg):
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
    way = input("Hi, which way you want to login? password/face/sound\n")
    flag = False
    if way == "face":
        # take a picture
        faceID = None # get faceID
        
        
        userName = db.login_faceID(faceID)
        if userName != False:
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
    userName = input("Please input your user name\n")
    db.add_user(userName)
    password = input("input password\n")
    db.add_password(userName, password)
    
    flag = input("want face ID?\n")
    if flag == "yes":
        print("get your face ID\n")
    
    flag = input("want sound ID?\n")
    if flag == "yes":
        print("get your sound ID\n")
def logout():
    global user
    global db
    user = "guest"
    print("Success logout")

def using():
    global user
    global db
    global opration
    
    if opration == "delete user":
        userName = input("Please input the user name which you want to delete\n")
        db.delete_user(userName)
    elif opration == "light up" :
        print("light up\n")
    elif opration == "set clock time" :
        clocktTime = input("input the clock time\n")
        #db.put_clockTime(user, clocktTime)
        print("clockTime "+clocktTime+"\n")
    elif opration == "clock up" :
        print("clock up\n")
    elif opration == "play song" :
        print("play song\n")
    else:
        print("Unkonw command\n")

##### initial setup #####
def init_setup():
    # create song diractory
    # create record diractory
    pass
############ alarm function (if login failure)#############
def alarm_lineNotify():
    global db
    msg = "Alert!! This person attempt to login\n"
    for userName in db.get_all_userName():
        token = db.get_lineToken(userName)
        lineNotifyMessage(token, msg)
    print("line notify\n")

def alarm_buzzer():
    print("buzzer\n")

def alarm_lightTwinkle():
    print("light twinkle")

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
                print("Unkown command\n")
        else:
            opration = input("Hi "+user+", how can I help you?\n")
            if opration == "logout":
                logout()
            else:
                using()
except KeyboardInterrupt:
    pass
