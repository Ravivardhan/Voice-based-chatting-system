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


def client():
    r=sr.Recognizer()

    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    hostIp = "127.0.0.1"
    portNumber = 7500

    clientSocket.connect((hostIp, portNumber))

    window = Tk()

    window.title("Connected To: "+ hostIp+ ":"+str(portNumber))

    txtMessages = Text(window, width=50)
    txtMessages.grid(row=0, column=0, padx=10, pady=10)

    txtYourMessage = Entry(window, width=50)
    txtYourMessage.grid(row=1, column=0, padx=10, pady=10)

    def sendMessage():



        clientMessage = txtYourMessage.get()
        txtMessages.insert(END, "\n"  + clientMessage)
        clientSocket.send(clientMessage.encode("utf-8"))


    btnSendMessage = Button(window, text="Send", width=20, command=sendMessage)
    btnSendMessage.grid(row=2, column=1, padx=10, pady=10)
    voice_btn=Button(window,text="voice msg",width=20)
    voice_btn.grid(row=2,column=0,padx=10,pady=10)

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
                    txtYourMessage.insert(0,   speech_text)
                    sendMessage()
                    engine.runAndWait()
            except sr.UnknownValueError as e:
                print("unknown error occurred")
                engine.say("speak again i didnt understand")
                engine.runAndWait()











        speak=pyttsx3.init()
        while True:

            serverMessage = clientSocket.recv(1024).decode("utf-8")
            print(serverMessage)
            speak.say(serverMessage)
            txtMessages.insert(END, "\n"+serverMessage)
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
                        txtYourMessage.delete(0,END)
                        txtYourMessage.insert(0,speech_text)
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






client()