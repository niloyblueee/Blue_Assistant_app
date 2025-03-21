import webbrowser as wb
import os
from AppOpener import open
from AppOpener import close
import sys
import threading
import customtkinter 
from  googlesearch import search
import speech_recognition
import pyttsx3 as tts 

class Assistant:

    def __init__(self):
        self.recognizer = speech_recognition.Recognizer()
        self.speaker = tts.init()
        self.speaker.setProperty("rate", 200)
        self.speaker.setProperty("volume", 1.0)

        self.window = customtkinter.CTk()
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")
        self.window.geometry ("360x360")
        self.window.title("Blue assistant")
        self.label= customtkinter.CTkLabel(master=self.window, text="[X_^]", font=("impact", 120 , "bold"))
        self.label.place(relx=0.5,rely=0.5,anchor="center")
 

        threading.Thread(target=self.run_assistant).start()

        self.window.mainloop()

    def search(self,text):    
        for i in search(text,tld='com',num=1,stop=1,pause=2) :
            #wb.open(i)
            wb.open_new_tab(i)
            
    def run_assistant(self):
        active = False
        while True:
            try:
                with speech_recognition.Microphone() as mic :
                    print("in here > things started")
                    self.recognizer.adjust_for_ambient_noise(mic, duration=0.1)
                    print("in here2 > aactively listening")
                    audio = self.recognizer.listen(mic)
                    print("in here3 > listened")
                    text = self.recognizer.recognize_google(audio)
                    text= text.lower()
                    print(f"Recognized ---> {text}")
                    if "hey blue" in text:
                        print("initiated")
                        active = True #active or not
                        self.speaker.say("hello, how may i help?")
                        self.label.configure(text_color="#0eb9ff")
                        self.speaker.runAndWait()
                        audio = self.recognizer.listen(mic)
                        text = self.recognizer.recognize_google(audio)
                        text = text.lower()
                        print("recognized audio")
                    
                    if active is True:

                        if text == 'stop':
                            print("stoping")
                            self.speaker.say("Certainly")
                            active = False
                            self.speaker.runAndWait()
                            self.window.destroy()
                            os._exit(0)
                    

                        elif "play" in text :
                            self.speaker.say(f"okay trying to play {text[4:]}")
                            self.speaker.runAndWait()
                            self.label.configure(text_color="red")
                            print("searching")
                            print(text)
                            self.search(text)
                            self.label.configure(text_color="white") 

                        elif text == "turn off pc" :
                            #self.speaker.say("ARE U SURE TO TURN OFF PC?")
                            #self.speaker.runAndWait()
                            #audio = self.recognizer.listen(mic)
                            #text = self.recognizer.recognize_google(audio)
                            #text = text.lower()
                            #print(text)
                            #if text == "yes" :
                            os.system('shutdown /s /t 0')  
                            #else: 
                            #    self.speaker.say("okay doing nothing")    
                            #    self.label.configure(text_color="white") 
                            #    self.speaker.runAndWait()
                                
                        elif text == "who created you" :
                            self.speaker.say("Mr.NiloyBlueee created me!")
                            wb.open_new_tab("https://www.linkedin.com/in/niloy-blueee-30787b294/")
                            self.label.configure(text_color="white")
                            self.speaker.runAndWait()

                        elif "open" in text :
                            print(text)
                            self.speaker.say(f"trying to open {text[4:]}")
                            self.speaker.runAndWait()
                            self.label.configure(text_color="#2E8B57")
                            open(text.split()[1])
                            self.label.configure(text_color="white") 
                               
                        elif "close" in text :
                            print(text)
                            self.speaker.say(f"trying to close {text[5:]}")
                            self.speaker.runAndWait()
                            self.label.configure(text_color="#880808")
                            close(text.split()[1])
                            self.label.configure(text_color="white") 
                                                     
                        else:
                            print("searching.... "+ text)
                            self.speaker.say(f"trying to find the best match for {text}")
                            self.speaker.runAndWait()
                            self.search(text)
                            self.label.configure(text_color="white") 

            except:
                self.label.configure(text_color="white")   
                continue          

Assistant()
                