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
from youtubesearchpython import VideosSearch
from sympy import sympify, sin, cos, tan, pi, symbols, log , ln, acos, asin, atan, factorial
from sympy.parsing.sympy_parser import parse_expr
import requests
from datetime import datetime
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



    def evaluate_expression(self, expression):
        # replace "degrees" with "*pi/180" to convert to radians
        #expression = expression.replace("degrees", "*pi/180")
        #expression = expression.replace("degree", "*pi/180")
        ##expression = expression.replace("°", "*pi/180")

        local_dict = {
        "sin": sin,
        "cos": cos,
        "tan": tan,
        "pi": pi,
        "log": log,
        "ln" : ln,
        "asin" :asin,
        "acos" :acos,
        "atan" :atan,
        "factorial" : factorial,
        }

        expr = parse_expr(expression, evaluate=True, local_dict=local_dict)
        print(f"bout to calculate  ==>> {expr}")
        return float(expr.evalf())  #  Convert to float here


    def Search(self, text):    
        print("In Search method")
        found = False
        try:
            for i in search(text, num_results=2, sleep_interval=5):
                if i and i.startswith("http"):  # Only open full URLs
                    print("Found result:", i)
                    wb.open_new_tab(i)
                    found = True
                else:
                    print("Skipping invalid result:", i)
        except Exception as e:
            print("Search failed:", e)

        if not found:
            print("No valid results found or search was blocked.")

    
    def spoken_to_math(self, expr):
        import re

        multi_word_ops = {
        'to the power of': '**',
        'to the power ' : '**',
        'divided by': '/',
        'multiplied by': '*',
        'equal to': '=',
        'square root of': 'sqrt',
        'cube root of': 'cbrt'

        }

        for phrase, symbol in multi_word_ops.items():
            expr = expr.replace(phrase, symbol)

        words_to_ops = {
            'plus': '+', 'sumation':'+' , 'minus': '-', 'times': '*', 'multiplied with': '*', 'multiplied by' : '*',
            'divided by': '/', 'over': '/', 'mod': '%', 'modulo': '%','by': '/',
            'power': '**', 'to the power of': '**', 'into': '*',
            'equals': '=', 'equal to': '=',

            'sin': 'sin', 'cosine': 'cos', 'cos': 'cos' , 'tangent': 'tan', 'tan':'tan',
            'pi': 'pi' ,
            'log': 'log',        # log base 10
            'natural log': 'ln',  # ln = natural logarithm
            'loan': 'ln',
            'lon': 'ln','sin inverse': 'asin', 'cos inverse': 'acos', 'tan inverse': 'atan',
            'antilog': '10 **'
        }

        # Fix sin/cos/tan so it becomes sin(45 * pi/180) etc.
        for word, symbol in words_to_ops.items():
            expr = expr.replace(word, symbol)
            
        # Convert "sin 30 degrees" to "sin(30 * pi / 180)"
        #expr = re.sub(r'(sin|cos|tan|asin|acos|atan)\s+(\d+)', r'\1(\2 * pi / 180)', expr)

        # Fix expressions like "sin pi by 180", "cos pi by 90", etc.
        expr = re.sub(r'(sin|cos|tan|asin|acos|atan)(?:\s+of)?\s+pi\s+by\s+(\d+)', r'\1(pi / \2)', expr)

        #fix of inverse with fractions
        expr = re.sub(r'(sin|cos|tan|asin|acos|atan)\s+([0-9]+(?:\.[0-9]+)?)', r'\1(\2 * pi / 180)', expr)

        # Fix cases like "factorial 5" or "factorial 0.5"
        expr = re.sub(r'factorial\s+(\d+(\.\d+)?)', r'factorial(\1)', expr)

        # Convert "log 100" to "log(100, 10)"
        expr = re.sub(r'\blog\s+([\d\.]+)', r'log(\1, 10)', expr)

        # Convert "ln 5" to "ln(5)"
        expr = re.sub(r'\bln\s+([\d\.]+)', r'ln(\1)', expr)
        
        # Square root and cube root cleanup
        expr = re.sub(r'sqrt\s+(\d+(\.\d+)?)', r'sqrt(\1)', expr)
        expr = re.sub(r'cbrt\s+(\d+(\.\d+)?)', r'(\1) ** (1/3)', expr)  # Using exponent for cube root
        
        # Handle "cube of 4" => "4 ** 3", and "square of 5" => "5 ** 2"
        expr = re.sub(r'cube of\s+(\d+(\.\d+)?)', r'(\1 ** 3)', expr)
        expr = re.sub(r'square of\s+(\d+(\.\d+)?)', r'(\1 ** 2)', expr)
        
        # Handle "2 square" => "2 ** 2", and "5 cube" => "5 ** 3"
        expr = re.sub(r'(\d+(\.\d+)?)\s*square', r'(\1 ** 2)', expr)
        expr = re.sub(r'(\d+(\.\d+)?)\s*cube', r'(\1 ** 3)', expr)

        # Cleanup extra spaces
        expr = re.sub(r'\s+', ' ', expr).strip()
        
        # Fix cases like: factorial 5 → factorial(5)
        expr = re.sub(r'factorial\s+(\d+)', r'factorial(\1)', expr)

        # Fix "sin 30" → "sin(30 * pi / 180)"
        expr = re.sub(r'(sin|cos|tan)\s+([\d\.]+)', r'\1(\2 * pi / 180)', expr)
        
        # Fix "sin pi by 180"
        expr = re.sub(r'(sin|cos|tan)\s+pi\s+by\s+(\d+)', r'\1(pi / \2)', expr)

        # Remove degree words AFTER trig substitution
        expr = expr.replace('degrees', '')
        expr = expr.replace('degree', '')
        expr = expr.replace('°', '')
        #remove X for *
        expr = expr.replace(" x ", " * ")

        return expr


    def get_location_key(self, city_name, api_key):
        url = f"http://dataservice.accuweather.com/locations/v1/cities/search"
        params = {
            "apikey": api_key,
            "q": city_name
        }
        response = requests.get(url, params=params)
        data = response.json()
        if data:
            return data[0]['Key'], data[0]['LocalizedName']
        return None, None

    def get_weather(self,city_name, api_key):
        key, localized_name = self.get_location_key(city_name, api_key)
        if not key:
            return f"Couldn't find weather for {city_name}"
        
        url = f"http://dataservice.accuweather.com/currentconditions/v1/{key}"
        params = {
            "apikey": api_key,
            "details": "true"
        }
        response = requests.get(url, params=params)
        weather_data = response.json()
        
        if weather_data:
            weather = weather_data[0]
            print(weather)
            text = weather['WeatherText']
            temp = weather['Temperature']['Metric']['Value']
            print(f"The current weather in {localized_name} is {text} with a temperature of {temp}°C.")
            return f"The current weather in {localized_name} is {text} with a temperature of {temp}°C."
        
        return f"Weather info for {city_name} is unavailable."


    def handle_weather(self, user_text):
        api_key = "N6f3inYvZxWJs10rlJD9Az81Qzm04BEM"

        # Ask the user for the city
        self.speaker.say("I don't access your location. Please tell me which city's weather you want.")
        self.speaker.runAndWait()

        try:
            with speech_recognition.Microphone() as mic:
                self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = self.recognizer.listen(mic)
                city = self.recognizer.recognize_google(audio).lower()
                print("Recognized city:", city)
        except speech_recognition.UnknownValueError:
            self.speaker.say("Sorry, I couldn't understand the city name. Please try again.")
            self.speaker.runAndWait()
            return  # exit early if city can't be understood

        # Step 1: Get Location Key
        try:
            location_url = f"http://dataservice.accuweather.com/locations/v1/cities/search"
            params = {"apikey": api_key, "q": city}
            loc_response = requests.get(location_url, params=params)
            location_data = loc_response.json()

            if not location_data:
                self.speaker.say("I couldn't find that city. Try a different one.")
                self.speaker.runAndWait()
                return

            location_key = location_data[0]['Key']
            city_name = location_data[0]['LocalizedName']

            # Step 2: Get Current Weather
            weather_url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}"
            params = {"apikey": api_key, "details": "true"}
            weather_response = requests.get(weather_url, params=params)
            weather_data = weather_response.json()

            if weather_data:
                weather_text = weather_data[0]['WeatherText']
                temperature = weather_data[0]['Temperature']['Metric']['Value']
                weather_report = f"The current weather in {city_name} is {weather_text} with a temperature of {temperature}°C."
                
                # Handle umbrella/sunshine responses
                if any(x in user_text for x in ["sunny", "raining", "umbrella", "cloudy", "rain"]):
                    if "rain" or "umbrella" or "raining" in weather_text.lower():
                        self.speaker.say("Yes, it looks like it's raining. You should take an umbrella.")
                    elif "sun" in weather_text.lower():
                        self.speaker.say("Yes, it's sunny outside.")
                    else:
                        self.speaker.say(f"The weather in {city_name} is currently {weather_text}.")
                else:
                    self.speaker.say(weather_report)
                self.speaker.runAndWait()
            else:
                self.speaker.say("Sorry, I couldn't retrieve the weather data.")
                self.speaker.runAndWait()
        except Exception as e:
            print("Weather error:", e)
            self.speaker.say("There was an error getting the weather.")
            self.speaker.runAndWait()
    
            
    def run_assistant(self):
        active = False
        while True:
            try:
                with speech_recognition.Microphone() as mic :
                    print("in here > things started")
                    self.recognizer.adjust_for_ambient_noise(mic, duration=0.1)
                    print("in here2 > actively listening")
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
                            break 

                        elif "play" in text :

                            self.speaker.say(f"okay trying to play {text[4:]}")
                            self.speaker.runAndWait()
                            self.label.configure(text_color="red")
                            print("searching")
                            print(text)

                            #self.search(text) <==== method 1
                            #wb.open_new_tab(f"https://www.youtube.com/results?search_query={text}") <==== method 2
                            
                            videosSearch = VideosSearch(text, limit=1) #<==== method 3
                            first_result = videosSearch.result()['result'][0]['link']
                            print(first_result)
                            wb.open_new_tab(first_result)

                            self.label.configure(text_color="white") 

                        elif text == "turn off pc":
                            self.speaker.say("ARE U SURE TO TURN OFF PC? Say Affirmative or Negative")
                            self.speaker.runAndWait()
                            with speech_recognition.Microphone() as confirm_mic:
                                self.recognizer.adjust_for_ambient_noise(confirm_mic, duration=0.2)
                                print("Listening for confirmation...")
                                audio = self.recognizer.listen(confirm_mic)
                                try:
                                    confirm_text = self.recognizer.recognize_google(audio).lower()
                                    print(f"Confirmation received: {confirm_text}")
                                    if "affirmative" in confirm_text:
                                        print("damn bro")
                                        # os.system('shutdown /s /t 0')
                                    else:
                                        self.speaker.say("okay doing nothing")    
                                        self.label.configure(text_color="white") 
                                        self.speaker.runAndWait()
                                except Exception as e:
                                    print("Error during confirmation:", repr(e))

                                    self.speaker.say("Sorry, I didn't catch that.")
                                    self.speaker.runAndWait()
                        
                        
                        elif "calculate" in text or "how much is" in text :
                            try:
                                expression = text.replace("calculate", "").replace("how much is", "").strip()
                                expression = self.spoken_to_math(expression)
                                print("Parsed Expression:", expression)

                                result = self.evaluate_expression(expression)
                                print(round(result,2))
                                self.speaker.say(f"The result is {round(result, 2)}")
                                self.speaker.runAndWait()
                                self.label.configure(text_color="#FFD700")

                            except Exception as e:
                                print("Math error:", e)
                                self.speaker.say("Sorry, I couldn't calculate that.")
                                self.speaker.runAndWait()

                        elif text.startswith("what is"):  # Only checking "what is" questions
                            expression = text.replace("what is", "").strip()
                            
                            if "weather" in expression or any(word in expression for word in ["sunny", "rainy", "umbrella", "hot", "cold", "temperature","raining"]):
                                self.handle_weather(expression)

                            elif "time" in expression:
                                now = datetime.now()
                                current_time = now.strftime("%I:%M %p")
                                print("Time:", current_time)
                                self.speaker.say(f"The current time is {current_time}")
                                self.speaker.runAndWait()

                            # 📅 Date check
                            elif "date" in expression or "day" in expression:
                                today = datetime.now().strftime("%A, %B %d, %Y")
                                print("Date:", today)
                                self.speaker.say(f"Today is {today}")
                                self.speaker.runAndWait()

                                
                            else:
                                math_keywords = { 
                                    'plus': '+', 'sumation':'+' , 'minus': '-', 'times': '*', 'multiplied with': '*', 'multiplied by' : '*',
                                    'divided by': '/', 'over': '/', 'mod': '%', 'modulo': '%','by': '/',
                                    'power': '**', 'to the power of': '**', 'into': '*',
                                    'equals': '=', 'equal to': '=',
                                    '+': '+',  
                                    '-': '-', 
                                    'x': '*', 
                                    '/': '/',
                                    
                                    'sin': 'sin', 'cosine': 'cos', 'cos': 'cos' , 'tangent': 'tan', 'tan':'tan',
                                    'pi': 'pi' ,
                                    'log': 'log',        # log base 10
                                    'natural log': 'ln',  # ln = natural logarithm
                                    'loan': 'ln',
                                    'lon': 'ln','sin inverse': 'asin', 'cos inverse': 'acos', 'tan inverse': 'atan',
                                    'antilog': '10 **',        'to the power of': '**',
                                    'to the power ' : '**',
                                    'divided by': '/',
                                    'multiplied by': '*',
                                    'equal to': '=',
                                    'square root of': 'sqrt',
                                    'cube root of': 'cbrt',
                                    'factorial' : 'factorial'
                                }

                                # Check if the expression contains a math-related word
                                if any(word in expression.split() for word in math_keywords):
                                    # Call your math evaluation function
                                    expression = self.spoken_to_math(expression)  # Convert to math syntax
                                    print("Parsed Expression:", expression)
                                    
                                    try:
                                        result = self.evaluate_expression(expression)
                                        print(round(result,2))
                                        self.speaker.say(f"The result is {round(result, 2)}")
                                        self.speaker.runAndWait()
                                        self.label.configure(text_color="#FFD700")
                                    except Exception as e:
                                        print("Math error:", e)
                                        self.speaker.say("Sorry, I couldn't calculate that.")
                                        self.speaker.runAndWait
                                
                                else:
                                    # If it's not a math query, do a Google search
                                    self.Search(text)
                        
                        elif "umbrella" and "take" in text:
                            self.handle_weather(text)

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

                        elif "weather" in text.lower():
                            self.speaker.say("I don't access your location. Please tell me which city's weather you want.")
                            self.speaker.runAndWait()

                            try:
                                with speech_recognition.Microphone() as mic:
                                    print("Listening for city name...")
                                    self.label.configure(text_color="cyan")
                                    self.recognizer.adjust_for_ambient_noise(mic, duration=0.1)
                                    audio = self.recognizer.listen(mic)
                                    city = self.recognizer.recognize_google(audio)
                                    city = city.lower().strip()
                                    print(f"City recognized ---> {city}")

                                    # Now call the weather function
                                    weather_report = self.get_weather(city, "N6f3inYvZxWJs10rlJD9Az81Qzm04BEM")
                                    self.speaker.say(weather_report)
                                    self.speaker.runAndWait()

                            except speech_recognition.UnknownValueError:
                                self.speaker.say("Sorry, I couldn't understand the city name.")
                                self.speaker.runAndWait()
                            except Exception as e:
                                print("Weather error:", e)
                                self.speaker.say("Something went wrong while getting the weather.")
                                self.speaker.runAndWait()

                        

                        elif "time" in text.lower():
                            now = datetime.now()
                            current_time = now.strftime("%I:%M %p")
                            print("Time:", current_time)
                            self.speaker.say(f"The current time is {current_time}")
                            self.speaker.runAndWait()

                        elif "date" in text.lower() or "day" in text.lower():
                            today = datetime.now().strftime("%A, %B %d, %Y")
                            print("Date:", today)
                            self.speaker.say(f"Today is {today}")
                            self.speaker.runAndWait()

 
                                                     
                        else:
                            print("searching.... "+ text)
                            self.speaker.say(f"trying to find the best match for {text}")
                            self.speaker.runAndWait()
                            self.Search(text)
                            self.label.configure(text_color="white") 

            except:
                self.label.configure(text_color="white")   
                continue          

Assistant()

                