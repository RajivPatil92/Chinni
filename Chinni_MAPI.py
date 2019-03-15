
'''
#########################################################################
#    __  __    _    ____ ___   __  __  ___  ____  _   _ _     _____     #
#   |  \/  |  / \  |  _ \_ _| |  \/  |/ _ \|  _ \| | | | |   | ____|    #
#   | |\/| | / _ \ | |_) | |  | |\/| | | | | | | | | | | |   |  _|      #
#   | |  | |/ ___ \|  __/| |  | |  | | |_| | |_| | |_| | |___| |___     #
#   |_|  |_/_/   \_\_|  |___| |_|  |_|\___/|____/ \___/|_____|_____|    #
#                                                                       #
#########################################################################

MODULE DESCRIPTION: THIS IS A MODULE THAT IS USED TO MAP THE FUNCTIONS
THAT NEEDS TO BE INVOKED BASED ON VOICE INPUT REQUEST. FOR EVERY KEYWORD
REGISTERED IN THE VOICE INPUT, A SPECIFIC FUNCTION IS INVOKED ACCORDINGLY
AND ADDITIONAL INFORMATION IS ALSO PASSED ON TO THEM TO DO FURTHER DETAILED
PROCESSING OF REQUEST.
'''



import WeatherMaster
import math_mama
#DICTIONARY THAT WILL STORE THE MAPPINGS
MAPI_MAP = {
}
'''
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
CLASS MAPI
Main Class that is used to map the functions for specific keywords matching 
against the voice input recieved.
    DEFINED FUNCTIONS:
        CREATE_MAPPING  :   A basic MAPPING method. multiple keywords to one function
                            mapping is established here. This needs to be done dynamically
                            to have a better scalability.
        getMAPI         :   This is API function that talks to main function which provides 
                            the function required to run based on keyword.
                        
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 
'''
class MAPI():
    def __init__(self):
        self.create_MAPPING()

    def create_MAPPING(self):
        WAPI = WeatherMaster.WeatherMaster()
        MATHY = math_mama.math_mama()
        MAPI_MAP[10000] = WAPI.getWeather
        MAPI_MAP[10010] = MATHY.add
        MAPI_MAP[10011] = MATHY.diff
        MAPI_MAP[10012] = MATHY.multiply
        MAPI_MAP[10013] = MATHY.divide
        MAPI_MAP[10020] = MATHY.sqRoot
        MAPI_MAP[10021] = MATHY.power
        MAPI_MAP[10022] = MATHY.exponential

    def getMAPI(self,number,args,moreinfo):
        return MAPI_MAP[number](args,moreinfo)