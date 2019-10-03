from PIL import Image
from gtts import gTTS

# ocr import
import os
import pytesseract
import subprocess
from subprocess import call
import picamera
import numpy as np
import cv2
import pyttsx3
import datetime
#switch import
import RPi.GPIO as GPIO
import time
import imutils
from picamera import PiCamera
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(13, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(15, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

# Face recognition function
def faceRecog():
    
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('/home/pi/Desktop/switch/FacialRecognitionProject/trainer/trainer.yml')
    cascadePath = "/home/pi/Desktop/switch/FacialRecognitionProject/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath);
    
    font = cv2.FONT_HERSHEY_SIMPLEX

    #iniciate id counter
    id = 0

    # names related to ids: example ==> Marcelo: id=1,  etc
    names = ['None', 'ahmed', 'ibrahim', 'safi', 'najmul', 'Sakib'] 
    
    # Initialize and start realtime video capture
    #cam = cv2.VideoCapture(0)

    
    # initialize the camera and grab a reference to the raw camera capture
    cam = PiCamera()
    cam.resolution = (1080, 720)
    cam.framerate = 32
    cam.rotation = 90
    cam.brightness=60
    
    #cam.set(3, 640) # set video widht
    #cam.set(4, 480) # set video height


    # Define min window size to be recognized as a face
    minW = 0.1*1080
    minH = 0.1*720

    def speechCallName(text_str):
        engine = pyttsx3.init()
        engine.setProperty('voice', 'english+f3')  # changes the voice
        engine.setProperty('rate', 125)  
        engine.say(text_str)     
        engine.runAndWait()
    
    
    def face_recognition():
        
        while not (GPIO.input(11) or GPIO.input(13) or GPIO.input(15)):
        #while True:
            print("yes3")        
            cam.capture("/home/pi/Desktop/switch/face1.png")
            #img = np.asarray(Image.open("/home/pi/Desktop/switch/FacialRecognitionProject/face1.png"))
            #img =cam.read()
            img = cv2.imread("/home/pi/Desktop/switch/face1.png")
            img = cv2.flip(img, -1) # Flip vertically
            img=imutils.rotate(img,angle=180)

            
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale( 
                gray,
                scaleFactor = 1.2,
                minNeighbors = 5,
                minSize = (int(minW), int(minH)),
               )

            for(x,y,w,h) in faces:

                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
                r=(2*x+w)/2

                id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

                # Check if confidence is less them 100 ==> "0" is perfect match 
                if ((100 - confidence)>40):
                    id = names[id]
                    confidence = "  {0}%".format(round(100 - confidence))
                    if (r>540):
                        engine=pyttsx3.init()
                        engine.say("go left")
                        engine.say("it's "+str(id))
                        engine.runAndWait()
                    else:
                        engine=pyttsx3.init()
                        engine.say("go right")
                        engine.say("it's "+str(id))
                        engine.runAndWait()
                    #file1 = open("MyFile.txt","a")
                    #file1.write("\n"+str(id)+ " at: "+str(datetime.datetime.now()))
                else:
                    id = "unknown"
                    confidence = "  {0}%".format(round(100 - confidence))
                    if (r>540):
                        engine=pyttsx3.init()
                        engine.say("go left")
                        engine.runAndWait()
                    else:
                        engine=pyttsx3.init()
                        engine.say("go right")
                        engine.runAndWait()
                
                cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
                cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)
               
            cv2.imshow('camera',img) 
            print("yes3")
            #if str(id)!= "unknown":
             #   speechCallName(str(id))
            k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
            if k == 27:
                break

        
        
    face_recognition()
    cam.close()
    cam.release()
    cv2.destroyAllWindows()
# End face recognition function
faceRecog()
