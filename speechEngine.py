'''
########################################################################
 ____                       _       _____             _
/ ___| _ __   ___  ___  ___| |__   | ____|_ __   __ _(_)_ __   ___
\___ \| '_ \ / _ \/ _ \/ __| '_ \  |  _| | '_ \ / _` | | '_ \ / _ \
 ___) | |_) |  __/  __/ (__| | | | | |___| | | | (_| | | | | |  __/
|____/| .__/ \___|\___|\___|_| |_| |_____|_| |_|\__, |_|_| |_|\___|
      |_|                                       |___/
 __  __           _       _
|  \/  | ___   __| |_   _| | ___
| |\/| |/ _ \ / _` | | | | |/ _ \
| |  | | (_) | (_| | |_| | |  __/
|_|  |_|\___/ \__,_|\__,_|_|\___|

#######################################################################
'''

#----------SPEECH PROCESSING MODULES---------------
import speech_recognition as sr
from gtts import gTTS
import playsound

#------------Basic PYTHON IMPORTS------------------
import time
from threading import Timer
import json

#----------IMPORT THE CHINNI-MAPI MODULE------------
import Chinni_MAPI
CapturedAudio = ''
DEBUG_SECTION  = True
TEST_STRING = "how is the weather in Seattle for next 3 days"
'''
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
CLASS SPEECH_ENGINE
This Class is used to convert the voice input into text and is responsible to parse
the information to the respective modules to get appropriate results.
    defined FUNCTIONS:
        SET_TIMER       :   A timer set to allow SpeechEngine to record consecutive 
                            requests, tie them and analyze the request generated.
                            For example: 
                                REQ1            : Hey, I need a total.
                                REQ2            : the numbers are 10, 20 and 30.
                                ACTUAL request : get the total of 10,20 and 30.
                                (Testing under progress)
        TIMER_TIMEOUT   :   To reset the timer to end multiple request
        SPEECH_PROCESS  :   VOICE TO TEXT CONVERSION FUNCTION
        REQUEST_PROCESSING: The function to link multiple request and pass it 
                            further processing.
        JSON_PARSER     :   This is used to parse the JSON file that contains the
                            mappping of keywords to functions.
        TTS_ENGINE      :   Text-to-speech conversion function

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
'''
class speechEngine():
    def __init__(self):
        self.CapturedAudio = ''
        self.requestRxcd = False
        self.language = 'en'
        self.num_list = []
        self.DEBUG = DEBUG_SECTION
        if self.DEBUG:
            print("DEBUGGING MODE IS ON")
        self.setTimer()
        self.TotalRequest = ''
        self.moreRequests = False

    def setTimer(self):
        self.t = Timer(10.0,self.timerTimeout)
        self.breakout = False
        self.moreRequests = True

    def timerTimeout(self):
        print("Going into Sleep mode")
        self.moreRequests = False

    def speech_process(self):
        temp_capture = ''
        # get audio from the microphone
        while(1):
            if (temp_capture == ''):
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source)
                    print("Speak:")
                    audio = r.listen(source)
                try:
                    print("You said " + r.recognize_google(audio))
                    str1 = r.recognize_google(audio)
                    temp_capture = str1
                    if temp_capture != '':
                        self.CapturedAudio = temp_capture
                        temp_capture = ''
                    if "hey" in str1 or self.DEBUG or self.moreRequests:
                        print("I got a request")
                        self.requestRxcd = True
                        self.requestProcessing()
                        self.DEBUG = False
                        if self.moreRequests:
                            print("waiting for more info")
                            continue
                        self.TTS_engine("Is there anything, Boss?", "timeout_response.mp3")
                        # need to invoke the machine to process the request
                except sr.UnknownValueError:
                    if self.DEBUG == True:
                        self.requestRxcd = True
                        self.requestProcessing()
                    print("Could not understand audio")
                    self.requestRxcd = False
                    break
                except sr.RequestError as e:
                    print("Could not request results; {0}".format(e))
                    self.requestRxcd = False

    def requestProcessing(self):
        # Need to determine here if there are more than one requests(a single requests with follow on information)
        if self.moreRequests and self.requestRxcd:
            if self.DEBUG:
                self.TotalRequest = TEST_STRING
            else:
                self.TotalRequest = self.TotalRequest+" "+self.CapturedAudio
        else:
            if self.requestRxcd or self.DEBUG:
                if self.DEBUG:
                    self.TotalRequest = TEST_STRING
                else:
                    self.TotalRequest = self.CapturedAudio
        self.JSON_parser("questions.json", self.TotalRequest)


    def JSON_parser(self, filename, string1):
        with open(filename, 'r') as fh:
            JSON_DATA = json.load(fh)
            print("Scanning through audio")
            for each in JSON_DATA.keys():
                if each in string1:
                    secondHint = string1.replace(each, "")
                    print(secondHint)
                    for every in JSON_DATA[each].keys():
                        if every in secondHint:
                            gotit = True
                            FuncCall = JSON_DATA[each][every]
                            #Extract all the numerical information
                            self.num_list = [int(s) for s in secondHint.split() if s.isdigit()]
                            if not self.num_list:
                                print("No numerical information")

                            print(" The Number List is {}".format(self.num_list))
                            print(FuncCall)
                            print(every)
                            print(each)
                            break
                    if not gotit:
                        return

                    API_CALLS = Chinni_MAPI.MAPI()
                    Response = API_CALLS.getMAPI(FuncCall,self.num_list,secondHint)

                    '''
                    except:
                        Response = "I'm Unable to solve this. I need an upgrade boss"
                    '''
                    self.TTS_engine(Response, "Response.mp3")
                    self.t.start()  #Start the Timer, wait for futher questions
                    print("Sikthu baddi maga")
                    # print(JSON_DATA[each])

    '''
    FUNCTION: TTS_engine(string1)

    Passing the text to the engine, 
    here we have marked slow=False.Which tells 
    the module that the converted audio should have a high speed
    '''
    def TTS_engine(self,string1, filename):
        tempfile = gTTS(text=string1, lang=self.language, slow=False)
        tempfile.save(filename)
        # Playing the converted file
        playsound.playsound(filename, True)
        time.sleep(1)

