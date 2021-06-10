Skip to content
Search or jump to…

Pull requests
Issues
Marketplace
Explore
 
@vincentkali 
vincentkali
/
Embedded_vioceAssistant
1
00
Code
Issues
Pull requests
1
Actions
Projects
Wiki
Security
Insights
Settings
Embedded_vioceAssistant/fun.py /
@poyenchen-d
poyenchen-d Create fun.py
Latest commit 3b58724 12 minutes ago
 History
 1 contributor
86 lines (68 sloc)  1.86 KB
  
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
 
def mfcc():
 os.system('arecord  -f cd -d 3 mfcc.mp3')
 y, sr = librosa.load('mfcc.mp3')
 global mfccs
 mfccs = librosa.feature.mfcc(y=y, sr=sr)

 print (mfccs)
 
def txt2voice():
 global talk
 tts = gTTS(text=talk, lang='en')
 tts.save('txt2voice.mp3')
 os.system('omxplayer -o local -p txt2voice.mp3 > /dev/null 2>&1')

def voice2txt():
 global talk
 r=sr.Recognizer()
 with sr.Microphone() as source:
  r.adjust_for_ambient_noise(source, duration=1)
  os.system('omxplayer -o local -p say.mp3 > /dev/null 2>&1')
  audio =r.listen(source)
  talk = r.recognize_google(audio,language="en")

def LED_on():
 GPIO.output(LED_PIN, GPIO.HIGH)
 os.system('omxplayer -o local -p LEDon.mp3 > /dev/null 2>&1')

def LED_off():
 GPIO.output(LED_PIN, GPIO.LOW)
 os.system('omxplayer -o local -p LEDoff.mp3 > /dev/null 2>&1')

def alarm_buzzer():
 os.system('omxplayer -o local -p alarm.mp3 > /dev/null 2>&1')

def alarm_lightTwinkle():
 LED_PIN = 12
 GPIO.setmode(GPIO.BOARD)
 GPIO.setup(LED_PIN, GPIO.OUT)
 
 for i in range(1,10): 
  GPIO.output(LED_PIN, GPIO.HIGH)
  time.sleep(0.25)
  GPIO.output(LED_PIN, GPIO.LOW)
  time.sleep(0.25)

def music():
 os.system('omxplayer -o local -p music1.mp3 > /dev/null 2>&1')

def record():
 os.system('omxplayer -o local -p say.mp3 > /dev/null 2>&1')
 os.system('arecord  -f cd -d 3 record.mp3')

def play_record():
 os.system('omxplayer -o local -p record.mp3 > /dev/null 2>&1')


try:
 while True:
  mfcc()  
  break
except KeyboardInterrupt:
   print ("Exception: KeyboardInterrupt")

finally:
   GPIO.output(LED_PIN, GPIO.LOW)
   GPIO.cleanup()
© 2021 GitHub, Inc.
Terms
Privacy
Security
Status
Docs
Contact GitHub
Pricing
API
Training
Blog
About
Loading complete
