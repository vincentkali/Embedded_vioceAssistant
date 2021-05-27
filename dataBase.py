########### DataBase Class #############################
class DataBase:
    def __init__(self):
        self.MAXUSER = 3
        self.MAXSONG = 3
        self.MAXRECORD = 3
        self.userNum = 0
        self.userDict = dict()
        self.faceLoginThreshold = float("inf") # 允許誤差
        self.soundLoginThreshold = float("inf") # 允許誤差
        
    ##### add/delete user #####
    def add_user(self, userName: str):
        if self.userNum == self.MAXUSER:
            print("Database is full, it can only contain "+str(self.MAXUSER)+" users")
            return False
        elif userName in list(self.userDict.keys()):
            print(userName+" is already in database")
            return False
        else:
            tempDict = {
                "password": None,
                "soundID": None,
                "faceID": None,
                "clockTime": [0]*3, # [幾點, 幾分, 幾秒]
                "songList": list(), # 歌曲清單, 資料類型: string, 內容: 歌曲的名稱
                "recordList": list(), # 影音日記, 資料類型: string, 內容 影音的路徑 
                "lineToken": "" # line notify 時要用的token
                                }  
                                    
            self.userDict.update({userName: tempDict})
            self.userNum += 1
            print("Success add "+userName+" into database")
            return True
    
    def delete_user(self, userName: str):
        if self.userNum == 0:
            print("There is no user in database")
            return False
        elif userName not in list(self.userDict.keys()):
            print(userName+" is not in database")
            return False
        else:
            self.userDict.pop(userName)
            self.userNum -= 1
            print("Success delete "+userName+" from database")
            return True
    
    ##### Clock function #####
    def put_clockTime(self, userName: str, clockTime: list):
        if userName not in list(self.userDict.keys()):
            print(userName+" is not in database")
            return False
        else:
            self.userDict[userName]["clockTime"] = clockTime
            print("Success add "+userName+"'s clockTime into database")
            return True
    
    def get_clockTime(self, userName: str):
        if userName not in list(self.userDict.keys()):
            print(userName+" is not in database")
            return False
        else:
            return self.userDict[userName]["clockTime"]
        
    ##### song function #####
    def add_intoSongList(self, userName: str, songPath: str):
        if userName not in list(self.userDict.keys()):
            print(userName+" is not in database")
            return False
        elif len(self.userDict[userName]["songList"]) == self.MAXSONG:
            print(userName+"'s song list is full, it can only contain "+str(self.MAXSONG)+" songs")
            return False
        else:
            self.userDict[userName]["songList"].append(songPath)
            print("Success add "+userName+"'s song into song list")
            return True
    
    def delete_wholeSongList(self, userName: str):
        if userName not in list(self.userDict.keys()):
            print(userName+" is not in database")
            return False
        else:
            print("Success delete "+userName+"'s whole song list from database")
            self.userDict[userName]["songList"] = list()
    
    ##### record log function #####
    def add_intoRecordList(self, userName: str, recordPath: str):
        if userName not in list(self.userDict.keys()):
            print(userName+" is not in database")
            return False
        elif len(self.userDict[userName]["recordList"]) == self.MAXRECORD:
            print(userName+"'s record list is full, it can only contain "+str(self.MAXRECORD)+" records")
            return False
        else:
            self.userDict[userName]["recordList"].append(recordPath)
            print("Success add "+userName+"'s record into record list")
            return True
    
    def delete_wholeRecordList(self, userName: str):
        if userName not in list(self.userDict.keys()):
            print(userName+" is not in database")
            return False
        else:
            print("Success delete "+userName+"'s whole record list from database")
            self.userDict[userName]["recordList"] = list()
            
    ##### line token #####
    def put_lineToken(self, userName: str, token: str):
        if userName not in list(self.userDict.keys()):
            print(userName+" is not in database")
            return False
        else:
            self.userDict[userName]["lineToken"] = token
            print("Success add "+userName+"'s line token into database")
            return True
    
    def get_lineToken(self, userName: str):
        if userName not in list(self.userDict.keys()):
            print(userName+" is not in database")
            return False
        else:
            return self.userDict[userName]["lineToken"]
    
    ##### password #####
    def add_password(self, userName: str, password:str):
        if userName not in list(self.userDict.keys()):
            print(userName+" is not in database")
            return False
        else:
            self.userDict[userName]["password"] = password
            print("Success set "+userName+"'s password")
            return True
    
    def login_password(self, userName: str, password: str):
        if userName not in list(self.userDict.keys()):
            print(userName+" is not in database")
            return False
        elif self.userDict[userName]["password"] == None:
            print(userName+" does not set password yet")
            return False
        elif self.userDict[userName]["password"] == password:
            print(userName+" success login with password")
            return True
     
    ##### face #####
    def add_faceID(self, userName: str, faceID: str):
        if userName not in list(self.userDict.keys()):
            print(userName+" is not in database")
            return False
        else:
            self.userDict[userName]["faceID"] = faceID
            print("Success set "+userName+"'s faceID")
            return True
    
    def login_faceID(self, faceID: str):
        minError = float("inf")
        mostLikePerson = None
        
        for userName, userData in self.userDict.items():
            if userData["faceID"] == None:
                continue
            else:
                error = abs(faceID - userData["faceID"]) # 類似概念, 要再改一下
                if error < minError:
                    minError = error
                    mostLikePerson = userName
        
        if mostLikePerson == None:
            print("There is no any faceID in database")
            return False
        elif minError > self.faceLoginThreshold:
            print("Face login fail")
            return False
        else:
            print(mostLikePerson+" success login with faceID")
            return mostLikePerson
            
    ##### sound #####
    def add_soundID(self, userName: str, soundID: list):
        if userName not in list(self.userDict.keys()):
            print(userName+" is not in database")
            return False
        else:
            self.userDict[userName]["soundID"] = soundID
            print("Success set "+userName+"'s soundID")
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
            print("There is no any soundID in database")
            return False
        elif minError > self.soundLoginThreshold:
            print("Face login fail")
            return False
        else:
            print(mostLikePerson+" success login with soundID")
            return mostLikePerson
