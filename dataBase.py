########### DataBase Class #############################
from math import sqrt

class DataBase:
    def __init__(self):
        self.MAXUSER = 3
        self.userNum = 0
        self.userDict = dict()
        self.faceLoginThreshold = float("inf") # 允許誤差
        self.soundLoginThreshold = float("inf") # 允許誤差
        self.debug = True
        
    ##### add/delete user #####
    def add_user(self, userName: str):
        if self.userNum == self.MAXUSER:
            if self.debug: print("Database is full, it can only contain "+str(self.MAXUSER)+" users")
            return False
        elif userName in list(self.userDict.keys()):
            if self.debug: print(userName+" is already in database")
            return False
        else:
            tempDict = {
                "password": None,
                "soundID": None,
                "faceID": None,
                "clockTime": [0]*3, # [幾點, 幾分, 幾秒]
                "lineToken": "" # line notify 時要用的token
                                }  
                                    
            self.userDict.update({userName: tempDict})
            self.userNum += 1
            if self.debug: print("Success add "+userName+" into database")
            return True
    
    def delete_user(self, userName: str):
        if self.userNum == 0:
            if self.debug: print("There is no user in database")
            return False
        elif userName not in list(self.userDict.keys()):
            if self.debug: print(userName+" is not in database")
            return False
        else:
            self.userDict.pop(userName)
            self.userNum -= 1
            if self.debug: print("Success delete "+userName+" from database")
            return True
    
    ##### Clock function #####
    def put_clockTime(self, userName: str, clockTime: list):
        if userName not in list(self.userDict.keys()):
            if self.debug: print(userName+" is not in database")
            return False
        else:
            self.userDict[userName]["clockTime"] = clockTime
            if self.debug: print("Success add "+userName+"'s clockTime into database")
            return True
    
    def get_clockTime(self, userName: str):
        if userName not in list(self.userDict.keys()):
            if self.debug: print(userName+" is not in database")
            return False
        else:
            return self.userDict[userName]["clockTime"]

    ##### line token #####
    def put_lineToken(self, userName: str, token: str):
        if userName not in list(self.userDict.keys()):
            if self.debug: print(userName+" is not in database")
            return False
        else:
            self.userDict[userName]["lineToken"] = token
            if self.debug: print("Success add "+userName+"'s line token into database")
            return True
    
    def get_lineToken(self, userName: str):
        if userName not in list(self.userDict.keys()):
            if self.debug: print(userName+" is not in database")
            return False
        else:
            return self.userDict[userName]["lineToken"]
    
    ##### password #####
    def add_password(self, userName: str, password:str):
        if userName not in list(self.userDict.keys()):
            if self.debug: print(userName+" is not in database")
            return False
        else:
            self.userDict[userName]["password"] = password
            if self.debug: print("Success set "+userName+"'s password")
            return True
    
    def login_password(self, userName: str, password: str):
        if userName not in list(self.userDict.keys()):
            if self.debug: print(userName+" is not in database")
            return False
        elif self.userDict[userName]["password"] == None:
            if self.debug: print(userName+" does not set password yet")
            return False
        elif self.userDict[userName]["password"] == password:
            if self.debug: print(userName+" success login with password")
            return True
        else:
            if self.debug: print(userName+" failure login, wrong password")
            return False
     
    ##### face #####
    def add_faceID(self, userName: str, faceID: list):
        if userName not in list(self.userDict.keys()):
            if self.debug: print(userName+" is not in database")
            return False
        else:
            self.userDict[userName]["faceID"] = faceID
            if self.debug: print("Success set "+userName+"'s faceID")
            return True
    
    def login_faceID(self, faceID: list):
        minError = float("inf")
        mostLikePerson = None
        
        for userName, userData in self.userDict.items():
            if userData["faceID"] == None:
                continue
            else:
                error = 0
                for test, db in zip(faceID, userData["faceID"]):
                    error += sqrt(pow(test[0]-db[0],2) + pow(test[1]-db[1],2))

                if self.debug: print(userName+"'s error: "+str(error))
                
                if error < minError:
                    minError = error
                    mostLikePerson = userName
        
        if mostLikePerson == None:
            if self.debug: print("There is no any faceID in database")
            return False
        elif minError > self.faceLoginThreshold:
            if self.debug: print("Face login fail")
            return False
        else:
            if self.debug: print(mostLikePerson+" success login with faceID")
            return mostLikePerson
            
    ##### sound #####
    def add_soundID(self, userName: str, soundID: list):
        if userName not in list(self.userDict.keys()):
            if self.debug: print(userName+" is not in database")
            return False
        else:
            self.userDict[userName]["soundID"] = soundID
            if self.debug: print("Success set "+userName+"'s soundID")
            return True
    
    def login_soundID(self, soundID: list):
        minError = float("inf")
        mostLikePerson = None
        
        for userName, userData in self.userDict.items():
            if userData["soundID"] == None:
                continue
            else:
                error = abs(soundID - userData["soundID"]) # 類似概念, 要再改一下
                if error < minError:
                    minError = error
                    mostLikePerson = userName
        
        if mostLikePerson == None:
            if self.debug: print("There is no any soundID in database")
            return False
        elif minError > self.soundLoginThreshold:
            if self.debug: print("Face login fail")
            return False
        else:
            if self.debug: print(mostLikePerson+" success login with soundID")
            return mostLikePerson
    
    def check_db(self):
        if self.debug: print(self.userDict)
    
    def get_all_userName(self):
        if self.debug: print(list(self.userDict.keys()))
        return list(self.userDict.keys())
    
    def colse_debug(self):
        self.debug = False
    
    def open_debug(self):
        self.debug = True
        
