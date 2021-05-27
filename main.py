# -*- coding: utf-8 -*-
        
##### login #####
def login():
    global user
    global db
    way = input("Hi, which way you want to login? password/face/sound")
    if way == "face":
        # take a picture
        faceID = None # get faceID
        
        
        userName = db.login_faceID(faceID)
        if userName != False:
            user = userName
    elif way == "sound":
        # getsound
        soundID = None # get faceID
        
        
        userName = db.login_faceID(soundID)
        if userName != False:
            user = userName
    elif way == "password":
        userName = input("Please input your user name")
        password = input("Please input your password")
        flag = login_password(userName, password)
        
        if flag == True:
            user = userName
        
##### add user #####
def adduser():
    global user
    global db
    userName = input("Please input your user name")
    db.add_user(userName)

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
        userName = input("Please input the user name which you want to delete")
        db.delete_user(userName)
    elif opration == "light up" :
        pass # light up
    elif opration == "set clock time" :
        clocktTime = None# get time
        db.put_clockTime(user, clocktTime)
    elif opration == "clock up" :
        pass # need add signal
    elif opration == "add song" :
        songName = None # get song name
        songPath = None
        db.add_intoSongList(user, songPath)
    elif opration == "play song" :
        pass # play song
    elif opration == "record" :
        pass
    elif opration == "play record" :
        pass
    else:
        print("Unkonw command")

##### initial setup #####
def init_setup():
    # create song diractory
    # create record diractory
    pass
############ alarm function (if login failure)#############
def alarm_lineNotify():
    pass

def alarm_buzzer():
    pass

def alarm_lightTwinkle():
    pass

##### main #####
opration = "login" # login, using, adduser
user = "guest"
db = DataBase()
db.add_user("admin")
db.add_password("admin", "admin")

while(True):
    if user == "guest":
        opration = input("Hi, do you want to login or add user?")
        if opration == "login":
            flag = login()
            if flag == False:
                alarm()
        elif opration == "adduser":
            adduser()
        else:
            print("Unkown command")
    else:
        opration = input("Hi "+user+", how can I help you?")
        if opration == "logout":
            logout()
        else:
            using()
            
            
            
