import tkinter as tk
from tkinter import *
import sqlite3
import cv2
import numpy as np
import face_recognition
import os
import datetime
import sqlite3
from utils import *
from matplotlib import pyplot as plt
import os
import pyttsx3
import time
from playsound import playsound

import subprocess
import speech_recognition as sr

from gtts import gTTS
import pandas
from tkinter import  messagebox
import pyttsx3
from socket import *
from threading import *
from utils import *
from matplotlib import pyplot as plt
import os
import pyttsx3
import time
from playsound import playsound
import cv2
import subprocess
from gtts import gTTS
from tkinter import *
import pyttsx3
import speech_recognition as sr
engine=pyttsx3.init()
import speech_recognition as sr
r=sr.Recognizer()
from socket import *
from threading import *
import os
from tkinter import *
import pyttsx3
import speech_recognition as sr
import threading
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
rate=engine.getProperty('rate')
engine.setProperty('rate',rate-85)


r=sr.Recognizer()
engine=pyttsx3.init()
def face_login():
    database=sqlite3.connect('face_recognizer')
    cursor=database.cursor()

    path = 'Training_images'
    images = []
    classNames = []
    myList = os.listdir(path)
    print(myList)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    print(classNames)


    def findEncodings(images):
        encodeList = []


        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    encodeListKnown = findEncodings(images)
    print('Encoding Complete')

    cap = cv2.VideoCapture(0)
    login=False
    while True:
        success, img = cap.read()

        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                print(name)
                login=True

                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('Webcam', img)

        if login==True:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()


    cv2.destroyAllWindows()
    main_application(name)

def face_register(name=''):
    engine=pyttsx3.init()
    engine.say("what is your name...")
    engine.runAndWait()

    ###################################  N A M E #################################
    while True:
        # Exception handling to handle
        # exceptions at the runtime
        try:

            # use the microphone as source for input.
            with sr.Microphone() as source2:

                # wait for a second to let the recognizer
                # adjust the energy threshold based on
                # the surrounding noise level
                r.adjust_for_ambient_noise(source2, duration=0.2)

                # listens for the user's input
                audio2 = r.listen(source2)

                # Using ggogle to recognize audio

                speech_text = r.recognize_google(audio2)
                speech_text = speech_text.lower()
                print(speech_text)
                name=speech_text


                camera = cv2.VideoCapture(0)
                for i in range(1):
                    engine = pyttsx3.init()
                    engine.say("please standby")
                    engine.runAndWait()
                    time.sleep(5)

                    return_value, image = camera.read()
                    cv2.imwrite('Training_images\{}'.format(name) + '.jpg', image)
                    return False
                del (camera)
                main_application(name)



        except sr.UnknownValueError:
            print("unknown error occured")
            engine.say("cant recognize ,say it again")
            engine.runAndWait()



def welcome():
    engine.say('say login for login and register for signup')
    engine.runAndWait()

database=sqlite3.connect('user_data')
cur=database.cursor()
cur.execute("create table if not exists user_db(username varchar(50),password varchar(50),mobile varchar(50))")


################################currency detector######################################33
def currency_detector(name=''):


    max_val = 8
    max_pt = -1
    max_kp = 0

    orb = cv2.ORB_create()

    camera = cv2.VideoCapture(0)
    for i in range(1):
        engine = pyttsx3.init()
        engine.say("please standby")
        engine.runAndWait()
        time.sleep(4)
        engine.say("capturing image please dont move")
        engine.runAndWait()
        return_value, image = camera.read()
        cv2.imwrite('webcurrency' + str(i) + '.png', image)
        test_img = read_img('webcurrency' + str(i) + '.png')
    del (camera)
    # orb is an alternative to SIFT

    # test_img = read_img('files/test_100_2.jpg')
    # test_img = read_img('files/test_50_2.jpg')

    # test_img = read_img('files/test_100_3.jpg')
    # test_img = read_img('files/test_20_4.jpg')

    # resizing must be dynamic
    original = resize_img(test_img, 0.4)
    #display('original', original)

    # keypoints and descriptors
    # (kp1, des1) = orb.detectAndCompute(test_img, None)
    (kp1, des1) = orb.detectAndCompute(test_img, None)

    training_set = ['files/20.jpg', 'files/50.jpg', 'files/100.jpg', 'files/500.jpg']

    for i in range(0, len(training_set)):
        # train image
        train_img = cv2.imread(training_set[i])

        (kp2, des2) = orb.detectAndCompute(train_img, None)

        # brute force matcher
        bf = cv2.BFMatcher()
        all_matches = bf.knnMatch(des1, des2, k=2)

        good = []
        # give an arbitrary number -> 0.789
        # if good -> append to list of good matches
        for (m, n) in all_matches:
            if m.distance < 0.789 * n.distance:
                good.append([m])

        if len(good) > max_val:
            max_val = len(good)
            max_pt = i
            max_kp = kp2

        print(i, ' ', training_set[i], ' ', len(good))

    if max_val != 8:
        print(training_set[max_pt])
        print('good matches ', max_val)

        train_img = cv2.imread(training_set[max_pt])
        img3 = cv2.drawMatchesKnn(test_img, kp1, train_img, max_kp, good, 4)

        note = str(training_set[max_pt])[6:-4]
        print('\nDetected denomination: Rs. ', note)
        engine.say(note, 'Rupees')
        engine.runAndWait()
        '''audio_file = 'audio/{}.mp3'.format(note)'''
        # audio_file = "value.mp3"
        # tts = gTTS(text=speech_out, lang="en")
        # tts.save(audio_file)
        # return_code = subprocess.call(["afplay", audio_file])
        # playsound(audio_file)
        #(plt.imshow(img3), plt.show())

    else:
        engine.say("cant detect any currency .........please try again later")
        engine.runAndWait()
        print('No Matches')
        engine.say("no currency detected")
        engine.say("say exit to exit the application and say detect to run the note detection application again")
        engine.runAndWait()
        for i in range(10):
            # Exception handling to handle
            # exceptions at the runtime
            try:

                # use the microphone as source for input.
                with sr.Microphone() as source2:

                    # wait for a second to let the recognizer
                    # adjust the energy threshold based on
                    # the surrounding noise level
                    r.adjust_for_ambient_noise(source2, duration=0.2)

                    # listens for the user's input
                    audio2 = r.listen(source2)

                    # Using ggogle to recognize audio

                    speech_text = r.recognize_google(audio2)
                    speech_text = speech_text.lower()
                    if speech_text=="exit":
                        main_application(name)
                    if speech_text=='detect':
                        currency_detector(name)


            except sr.UnknownValueError:
                print("unknown error occured")












def listen():
    engine.say("say something...")
    engine.runAndWait()
    for i in range(10):
        # Exception handling to handle
        # exceptions at the runtime
        try:

            # use the microphone as source for input.
            with sr.Microphone() as source2:

                # wait for a second to let the recognizer
                # adjust the energy threshold based on
                # the surrounding noise level
                r.adjust_for_ambient_noise(source2, duration=0.2)

                # listens for the user's input
                audio2 = r.listen(source2)

                # Using ggogle to recognize audio

                speech_text = r.recognize_google(audio2)
                speech_text = speech_text.lower()
                return  (speech_text)



        except sr.UnknownValueError:
            print("unknown error occured")
############################################### C H A T T I N G   S E R V E R ##############################################################

from socket import *
from threading import *
from tkinter import *
import pyttsx3
import speech_recognition as sr
import speech_recognition as sr
engine=pyttsx3.init()
r=sr.Recognizer()
def listen():
    engine.say("say something to send the message")
    engine.runAndWait()
    for i in range(5):
        # Exception handling to handle
        # exceptions at the runtime
        try:

            # use the microphone as source for input.
            with sr.Microphone() as source2:

                # wait for a second to let the recognizer
                # adjust the energy threshold based on
                # the surrounding noise level
                r.adjust_for_ambient_noise(source2, duration=0.2)

                # listens for the user's input
                audio2 = r.listen(source2)

                # Using ggogle to recognize audio

                speech_text = r.recognize_google(audio2)
                speech_text = speech_text.lower()
                return  (speech_text)



        except sr.UnknownValueError:
            print("unknown error occured")
            engine.say("please say again i didnt get that")
            engine.runAndWait()


def Client(name=''):
    engine = pyttsx3.init()
    r = sr.Recognizer()

    def client(name):
        r = sr.Recognizer()

        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        hostIp = "127.0.0.1"
        portNumber = 7500

        clientSocket.connect((hostIp, portNumber))

        window = Tk()

        window.title("Connected To: " + hostIp + ":" + str(portNumber))

        txtMessages = Text(window, width=50)
        txtMessages.grid(row=0, column=0, padx=10, pady=10)

        txtYourMessage = Entry(window, width=50)
        txtYourMessage.grid(row=1, column=0, padx=10, pady=10)

        def sendMessage():

            clientMessage = name+'says'+txtYourMessage.get()
            txtMessages.insert(END, "\n" + clientMessage)
            clientSocket.send(clientMessage.encode("utf-8"))

        btnSendMessage = Button(window, text="Send", width=20, command=sendMessage)
        btnSendMessage.grid(row=2, column=1, padx=10, pady=10)
        voice_btn = Button(window, text="voice msg", width=20)
        voice_btn.grid(row=2, column=0, padx=10, pady=10)

        def recvMessage():

            engine.say("say something to send the message")
            engine.runAndWait()
            for i in range(1):
                # Exception handling to handle
                # exceptions at the runtime
                try:
                    # use the microphone as source for input.
                    with sr.Microphone() as source2:
                        # wait for a second to let the recognizer
                        # adjust the energy threshold based on
                        # the surrounding noise level
                        r.adjust_for_ambient_noise(source2, duration=0.2)

                        # listens for the user's input
                        audio2 = r.listen(source2)

                        # Using ggogle to recognize audio

                        speech_text = r.recognize_google(audio2)
                        speech_text = speech_text.lower()
                        txtYourMessage.delete(0, END)
                        txtYourMessage.insert(0, speech_text)
                        sendMessage()
                        engine.runAndWait()
                except sr.UnknownValueError as e:
                    print("unknown error occurred")
                    engine.say("speak again i didnt understand")
                    engine.runAndWait()

            speak = pyttsx3.init()
            while True:

                serverMessage = clientSocket.recv(1024).decode("utf-8")
                print(serverMessage)
                speak.say(serverMessage)
                txtMessages.insert(END, "\n" + serverMessage)
                speak.runAndWait()
                engine.say("say something to send the message")
                engine.runAndWait()
                while True:
                    # Exception handling to handle
                    # exceptions at the runtime
                    try:
                        # use the microphone as source for input.
                        with sr.Microphone() as source2:
                            # wait for a second to let the recognizer
                            # adjust the energy threshold based on
                            # the surrounding noise level
                            r.adjust_for_ambient_noise(source2, duration=0.2)

                            # listens for the user's input
                            audio2 = r.listen(source2)

                            # Using ggogle to recognize audio

                            speech_text = r.recognize_google(audio2)
                            speech_text = speech_text.lower()
                            txtYourMessage.delete(0, END)
                            txtYourMessage.insert(0, speech_text)
                            sendMessage()
                            engine.runAndWait()
                            return False
                    except sr.UnknownValueError as e:
                        print("unknown error occurred")
                        engine.say("speak again i didnt understand")
                        engine.runAndWait()

        recvThread = Thread(target=recvMessage)
        recvThread.daemon = True
        recvThread.start()

        window.mainloop()

    client(name)





########################################### L O G I N   F R A M E##############################################################

def listen():
    engine.say("say something...")
    engine.runAndWait()
    for i in range(10):
        # Exception handling to handle
        # exceptions at the runtime
        try:

            # use the microphone as source for input.
            with sr.Microphone() as source2:

                # wait for a second to let the recognizer
                # adjust the energy threshold based on
                # the surrounding noise level
                r.adjust_for_ambient_noise(source2, duration=0.2)

                # listens for the user's input
                audio2 = r.listen(source2)

                # Using ggogle to recognize audio

                speech_text = r.recognize_google(audio2)
                speech_text = speech_text.lower()
                return  (speech_text)



        except sr.UnknownValueError:
            print("unknown error occured")

def main_application(name=''):
        engine.say("say chat to enter chatting server or say  detect to detect currency notes")
        engine.runAndWait()
        for i in range(10):
            # Exception handling to handle
            # exceptions at the runtime
            try:
                # use the microphone as source for input.
                with sr.Microphone() as source2:
                    # wait for a second to let the recognizer
                    # adjust the energy threshold based on
                    # the surrounding noise level
                    r.adjust_for_ambient_noise(source2, duration=0.2)

                    # listens for the user's input
                    audio2 = r.listen(source2)

                    # Using ggogle to recognize audio

                    speech_text = r.recognize_google(audio2)
                    speech_text = speech_text.lower()
                    print(speech_text)
                    if speech_text=='chat':
                        Client(name)
                    elif speech_text=='detect':
                        currency_detector(name)
            except sr.UnknownValueError as e:
                print("unknown error occurred")
                engine.say("cant recognize.... speak again")
                engine.runAndWait()
                main_application(name)


################################## L O G I N    F U N C T I O N ######################


def sign_new():
    signup_frame = tk.Tk()
    signup_frame.geometry('700x700')

    label_sig=Label(signup_frame,text="SIGN UP",font=('Helvatice',44)).place(x=270,y=50)

    sign_label_username=Label(signup_frame,text="Username :",font=('Helvatica',22)).place(x=200,y=220)
    sign_input_username=Entry(signup_frame,width=30)
    sign_input_username.place(x=360,y=219,height=39)

    sign_pass_label=Label(signup_frame,text="Password :",font=("Helvatica",22)).place(x=200,y=320)
    sign_pass_entry=Entry(signup_frame,width=30,show="*")
    sign_pass_entry.place(x=360,y=319,height=39)
    sign_mobile_label=Label(signup_frame,text="Mobile :",font=("Helvatice",22)).place(x=200,y=400)
    sign_mobile_entry=Entry(signup_frame,width=30)
    sign_mobile_entry.place(x=360,height=39,y=400)

    def signup(name='',password=''):
     with sqlite3.connect("user_data") as db:
        cur = db.cursor()
        name=sign_input_username.get()
        password=sign_pass_entry.get()

        query="insert into user_db(username,password) values('{}','{}')".format(name,password)
        cur.execute(query)
        db.commit()

        signup_frame.destroy()
        engine.say("successfully logged in")
        global active_user
        active_user=name
        global active_password
        active_password=password
        main_application(name)


    def speak_sign():



            for i in range(10):
                # Exception handling to handle
                # exceptions at the runtime
                try:
                    engine.say('say your username')
                    engine.runAndWait()

                    # use the microphone as source for input.
                    with sr.Microphone() as source2:

                        # wait for a second to let the recognizer
                        # adjust the energy threshold based on
                        # the surrounding noise level
                        r.adjust_for_ambient_noise(source2, duration=0.2)

                        # listens for the user's input
                        audio2 = r.listen(source2)

                        # Using ggogle to recognize audio

                        speech_text = r.recognize_google(audio2)
                        username = speech_text.lower()
                        print(username)
                        sign_input_username.delete(0,END)
                        sign_input_username.insert(0, username)
                        if len(sign_input_username.get()) > 0:
                            break



                except sr.UnknownValueError:
                    print("unknown error occured")
                    engine.say('say your username')
                    engine.runAndWait()
            for i in range(10):
                # Exception handling to handle
                # exceptions at the runtime
                try:
                    engine.say('say your password')
                    engine.runAndWait()
                    # use the microphone as source for input.
                    with sr.Microphone() as source2:

                        # wait for a second to let the recognizer
                        # adjust the energy threshold based on
                        # the surrounding noise level
                        r.adjust_for_ambient_noise(source2, duration=0.2)

                        # listens for the user's input
                        audio2 = r.listen(source2)

                        # Using ggogle to recognize audio

                        speech_text = r.recognize_google(audio2)
                        password = speech_text.lower()
                        print(password)
                        sign_pass_entry.delete(0,END)
                        sign_pass_entry.insert(0, password)
                        if len(sign_pass_entry.get()) > 0:
                            engine.say('say continue to signup')
                            engine.runAndWait()
                            for i in range(10):
                                # Exception handling to handle
                                # exceptions at the runtime
                                try:

                                    # use the microphone as source for input.
                                    with sr.Microphone() as source2:

                                        # wait for a second to let the recognizer
                                        # adjust the energy threshold based on
                                        # the surrounding noise level
                                        r.adjust_for_ambient_noise(source2, duration=0.2)

                                        # listens for the user's input
                                        audio2 = r.listen(source2)

                                        # Using ggogle to recognize audio

                                        proceed = r.recognize_google(audio2)
                                        proceed = proceed.lower()
                                        print(proceed)

                                        if len(proceed) > 0:
                                            if proceed == 'continue':
                                                return signup(name=username, password=password)
                                            break


                                except sr.UnknownValueError:
                                    print("unknown error occured")
                                    engine.say('say continue to signup')
                                    engine.runAndWait()
                            break



                except sr.UnknownValueError:
                    print("unknown error occured")
                    engine.say('say your password')
                    engine.runAndWait()

            engine.runAndWait()
    threading.Thread(target=speak_sign).start()
    threading.Thread(target=signup_frame.mainloop()).start()


def login_base():
            window=tk.Tk()
            window.geometry('700x700')

            log_title=Label(window,text="LOGIN",font=("Helvatica",40)).place(x=300,y=50)

            username_label=Label(window,text="Username:",font=("Helvatica",22)).place(x=200,y=220)
            username_entry=Entry(window,width=30)
            #,
            username_entry.place(x=360,y=219,height=39)

            password_label=Label(window,text="Password:",font=("Helvatica",22)).place(x=200,y=320)
            password_entry=Entry(window,width=30,show="*")
            password_entry.place(x=360,y=319,height=39)
            #,

            Login=Button(window,text="Login",command=lambda : login()).place(x=370,y=420,height=50,width=100)
            #

            sign=Label(window,text="already have an account?").place(y=520,x=270)

            sign_up=Button(window,text="signup here",command=lambda :sign_new()).place(x=430,y=515,height=40,width=120)
            #,



            forget=Button(window,text="forget password?").place(x=470,y=359,height=30,width=130)


            def login(name,password):
               with sqlite3.connect("user_data") as db:
                cur=db.cursor()
                '''name = username_entry.get()
                password = password_entry.get()'''
                user_login = "select * from user_db where username='{}' and password='{}'".format(name, password)
                cur.execute(user_login)
                data=cur.fetchone()
                db.commit()

                if data==None:

                    engine.say("invalid username or password please try again")
                    engine.runAndWait()
                    speak_log()

                if len(data) >= 1:
                    window.destroy()
                    engine.say("successfully logged in")
                    global active_user
                    active_user = name
                    global active_passwor3d
                    active_password = password
                    '''engine.say("say chat to enter chat ..................and two to enter currency detector")
                    engine.runAndWait()'''
                    main_application(active_user)

                ################################################-----M  A  I  N    A  P  P  L  I  C  A  T  I  O  N-----#######################################
                                    ###########################################-----C L I E N T ------------------------###############################


            #,

            def speak_log():

                engine.say('say your username....')


                engine.runAndWait()
                for i in range(10):
                    # Exception handling to handle
                    # exceptions at the runtime
                    try:

                        # use the microphone as source for input.
                        with sr.Microphone() as source2:

                            # wait for a second to let the recognizer
                            # adjust the energy threshold based on
                            # the surrounding noise level
                            r.adjust_for_ambient_noise(source2, duration=0.2)

                            # listens for the user's input
                            audio2 = r.listen(source2)

                            # Using ggogle to recognize audio

                            speech_text = r.recognize_google(audio2)
                            username = speech_text.lower()
                            print(username)
                            username_entry.delete(0,END)
                            username_entry.insert(0,username)
                            if len(username_entry.get())>0:
                                break
                        engine.say("say your username")
                        engine.runAndWait()


                    except sr.UnknownValueError:
                        print("unknown error occured")
                for i in range(10):
                    # Exception handling to handle
                    # exceptions at the runtime
                    try:
                        engine.say('say your password')
                        engine.runAndWait()
                        # use the microphone as source for input.
                        with sr.Microphone() as source2:

                            # wait for a second to let the recognizer
                            # adjust the energy threshold based on
                            # the surrounding noise level
                            r.adjust_for_ambient_noise(source2, duration=0.2)

                            # listens for the user's input
                            audio2 = r.listen(source2)

                            # Using ggogle to recognize audio

                            speech_text = r.recognize_google(audio2)
                            password = speech_text.lower()
                            print(password)
                            password_entry.delete(0,END)
                            password_entry.insert(0,password)
                            if len(password_entry.get()) > 0:
                                engine.say('say continue to login')
                                engine.runAndWait()
                                for i in range(10):
                                    # Exception handling to handle
                                    # exceptions at the runtime
                                    try:

                                        # use the microphone as source for input.
                                        with sr.Microphone() as source2:

                                            # wait for a second to let the recognizer
                                            # adjust the energy threshold based on
                                            # the surrounding noise level
                                            r.adjust_for_ambient_noise(source2, duration=0.2)

                                            # listens for the user's input
                                            audio2 = r.listen(source2)

                                            # Using ggogle to recognize audio

                                            proceed = r.recognize_google(audio2)
                                            proceed = proceed.lower()
                                            print(proceed)

                                            if len(proceed) > 0:
                                                if proceed=='continue':
                                                    return login(name=username,password=password)
                                                break


                                    except sr.UnknownValueError:
                                        print("unknown error occured")
                                        engine.say("say continue to login")
                                        engine.runAndWait()
                                break
                            engine.say('say your password')
                            engine.runAndWait()


                    except sr.UnknownValueError:
                        print("unknown error occured")


            engine.runAndWait()
            threading.Thread(target=speak_log).start()
            threading.Thread(target=window.mainloop()).start()



def command():
    for i in range(10):
        # Exception handling to handle
        # exceptions at the runtime
        try:

            # use the microphone as source for input.
            with sr.Microphone() as source2:

                # wait for a second to let the recognizer
                # adjust the energy threshold based on
                # the surrounding noise level
                r.adjust_for_ambient_noise(source2, duration=0.2)

                # listens for the user's input
                audio2 = r.listen(source2)

                # Using ggogle to recognize audio

                speech_text = r.recognize_google(audio2)
                speech_text = speech_text.lower()
                print(speech_text)
                if speech_text=='login':
                    login_base()
                    break

                elif speech_text=='register':
                    sign_new()
                    break



        except sr.UnknownValueError:
            print("unknown error occured")
            engine.say("say something")
            engine.runAndWait()

def face_log():
    engine.say("say login to to face login or  say register to create an account with face detection")
    engine.runAndWait()

    while True:
        # Exception handling to handle
        # exceptions at the runtime
        try:

            # use the microphone as source for input.
            with sr.Microphone() as source2:

                # wait for a second to let the recognizer
                # adjust the energy threshold based on
                # the surrounding noise level
                r.adjust_for_ambient_noise(source2, duration=0.2)

                # listens for the user's input
                audio2 = r.listen(source2)

                # Using ggogle to recognize audio

                speech_text = r.recognize_google(audio2)
                speech_text = speech_text.lower()
                print(speech_text)
                if speech_text=='login':
                    face_login()
                if speech_text=='register':
                    face_register()



        except sr.UnknownValueError:
            engine.say("say something")
            engine.runAndWait()




'''welcome()


command()'''
engine.say("say login to login with face recognition and voice login to manually login with voice")
engine.runAndWait()
while True:
    # Exception handling to handle
    # exceptions at the runtime
    try:

        # use the microphone as source for input.
        with sr.Microphone() as source2:

            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            r.adjust_for_ambient_noise(source2, duration=0.2)

            # listens for the user's input
            audio2 = r.listen(source2)

            # Using ggogle to recognize audio

            speech_text = r.recognize_google(audio2)
            speech_text = speech_text.lower()
            print(speech_text)
            if speech_text == 'face login':
                engine.say("logging you in with face detection algorithm")
                face_log()
                break
            elif speech_text=='voice login':
                welcome()
                command()



    except sr.UnknownValueError:
        print("unknown error occured")
        engine.say("say something")
        engine.runAndWait()