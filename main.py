'''

#####################################################################
#  ____            _           _      ____ _     _             _    #
# |  _ \ _ __ ___ (_) ___  ___| |_   / ___| |__ (_)_ __  _ __ (_)   #
# | |_) | '__/ _ \| |/ _ \/ __| __| | |   | '_ \| | '_ \| '_ \| |   #
# |  __/| | | (_) | |  __/ (__| |_  | |___| | | | | | | | | | | |   #
# |_|   |_|  \___// |\___|\___|\__|  \____|_| |_|_|_| |_|_| |_|_|   #
#               |__/                                                #
#                                                                   #
#####################################################################


$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
$   AUTHOR:                                                         $
$  _   _   _   _   _     _   _   _   _   _   _   _   _   _          $
$ / \ / \ / \ / \ / \   / \ / \ / \ / \ / \ / \ / \ / \ / \         $
$( R | A | J | I | V ) ( B | A | S | A | V | A | R | A | J )        $
$ \_/ \_/ \_/ \_/ \_/   \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/         $
$         _   _   _   _   _                                         $
$        / \ / \ / \ / \ / \                                        $
$       ( P | A | T | I | L )                                       $
$        \_/ \_/ \_/ \_/ \_/                                        $
$                                                                   $
$   BUILD: 1.0.0.0                                                  $
$   DATE: 3/14/2019                                                 $
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
'''


import datetime
from speechEngine import speechEngine, CapturedAudio
import threading

USER = "Rajiv Patil"
uname = USER.split()[0]
TEMP_TYPE = "celsius"

# The text that you want to convert to audio
def greeting(str1):
    t = datetime.datetime.now()
    TimeOfDay = int(str(t).split()[1].split(':')[0])
    print(TimeOfDay)
    if str1 == 'greeting':
        if TimeOfDay < 12:
            return "Good Morning"
        elif TimeOfDay <= 17:
            return "Good Afternoon"
        else:
            return "Good Evening"
    else:
        if TimeOfDay <= 17:
            return "Have a Good Day"
        else:
            return "Have a good evening"

#**************************
# GREETING FUNCTION
#*************************
def begin(Voice):
    Hi = greeting('greeting')
    salute = Hi+", Mr. "+uname
    Voice.TTS_engine(salute, "welcome.mp3")

'''
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
-----------------MAIN CLASS---------------------
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
'''
if __name__ == '__main__':
    Speech = speechEngine()
    begin(Speech)
    speechRecog = threading.Thread(target=Speech.speech_process())
    speechRecog.start()










