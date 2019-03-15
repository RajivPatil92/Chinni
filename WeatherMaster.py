'''
#################################################################################
#   __        __         _   _                 __  __           _               #
#   \ \      / /__  __ _| |_| |__   ___ _ __  |  \/  | __ _ ___| |_ ___ _ __    #
#    \ \ /\ / / _ \/ _` | __| '_ \ / _ \ '__| | |\/| |/ _` / __| __/ _ \ '__|   #
#     \ V  V /  __/ (_| | |_| | | |  __/ |    | |  | | (_| \__ \ ||  __/ |      #
#      \_/\_/ \___|\__,_|\__|_| |_|\___|_|    |_|  |_|\__,_|___/\__\___|_|      #
#        __  __           _       _                                             #
#       |  \/  | ___   __| |_   _| | ___                                        #
#       | |\/| |/ _ \ / _` | | | | |/ _ \                                       #
#       | |  | | (_) | (_| | |_| | |  __/                                       #
#       |_|  |_|\___/ \__,_|\__,_|_|\___|                                       #
#                                                                               #
#################################################################################

MODULE DESCRIPTION:

THIS MODULE IS USED TO EXTRACT THE WEATHER DETAILS FROM THE WEBSITE USING THE LIBRARY
    - PYOWM

'''
import pyowm                                #Weather forecast library

WhereamI = "Boulder"                        #Default Location used to testing purposes
TEMP_TYPE = "celsius"                       #Temperature type needed
API_KEY='9216e5bdc92ec9d01a26f5c0ab65c189'  #WEATHER-API key for the website

'''
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
CLASS WEATHERMASTER
Main Class that provides weather infromation requsted 
by the user from the speech engine.
    Defined Functions:
        GET_LOCATION        :   Extract the location information from the speech
        GET_WEATHER         :   Fetches the weather details for a given location
        TODAY_WEATHER       :   Provides only Today's Forecast
        ADDITIONALINFO      :   Provides additional information about rain and snow
        FORECAST_EXTRACTOR  :   Provides a multiple day forecast.
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
'''
class WeatherMaster():
    def __init__(self):
        self.WhereamI = "Boulder"
        self.TEMP_TYPE = "celsius"
        self.API_KEY = '9216e5bdc92ec9d01a26f5c0ab65c189'
        self.owm = pyowm.OWM(API_KEY)
        pass

    def get_location(self,speech):
        try:
            Locationdetails = speech.split()

            if "at" in Locationdetails:
                atLoc = Locationdetails.index("at")
            elif "in" in Locationdetails:
                atLoc = Locationdetails.index("in")
            print(atLoc)
            print("FOUND LOCATION {}".format(Locationdetails[atLoc+1]))
            return Locationdetails[atLoc+1]
        except:
            return "NotFound" #Failure case

    def getWeather(self,*argv):
        numlist = argv[0]
        if argv[1]:
            moreInfo = argv[1]
        else:
            moreInfo=""

        self.WhereamI = self.get_location(moreInfo)
        #print(moreInfo) DEBUG CODE
        if "tomorrow" in moreInfo or "next day" in moreInfo:
            return self.forecast_extractor(2)
        elif "days" in moreInfo:
            return self.forecast_extractor(numlist[0])
        else:
            return self.today_weather()

    def today_weather(self):
        try:
            observation = self.owm.weather_at_place(self.WhereamI)
        except:
            return " I'm Sorry. I could not find the place called {}".format(self.WhereamI)
        self.Wdetails =observation.get_weather()
        print(self.Wdetails)
        additionalInfo = self.additionalInfo(self.Wdetails)
        return ("Temperature for today will be around {} {}.The Humidity will remain {} %. You can "
                   "expect {} too. {}".format(self.Wdetails.get_temperature(unit=self.TEMP_TYPE)['temp'],
                                                                self.TEMP_TYPE, self.Wdetails.get_humidity(),
                                                        self.Wdetails.get_detailed_status(),additionalInfo))

    def additionalInfo(self,WObject):
        if not (WObject.get_snow() and WObject.get_rain()):
            return "Forecast predicts no snow or rain today."
        elif WObject.get_rain():
            return " It is going to rain for {} hours. Expected volume would be {} millimeters".format(
                WObject.get_rain().keys()[0],WObject.get_rain()[0])
        if WObject.get_snow():
            return " It is going to snow for {} hours. Expected volume would be {} millimeters".format(
                WObject.get_snow().keys()[0],WObject.get_snow()[0])

    def forecast_extractor(self,number_of_days):
        observation = self.owm.daily_forecast(self.WhereamI, limit=number_of_days)
        f = observation.get_forecast()
        lst1 = f.get_weathers()
        if number_of_days == 2: #tomorrow forecast
            additionalInfo = self.additionalInfo(lst1[1])
            return ("{} Forecast for Tomorrow is as follows : Max Temperature is {} degree celsius. Minimum "
                    "Temperature is "
                    "{} degree celsius. On an Average it will be around {} degree celsius. "
                    "The Humidity will remain {} %. You can expect {} too.".format(self.WhereamI,
                                                lst1[1].get_temperature(unit=self.TEMP_TYPE)['max'],
                                                lst1[1].get_temperature(unit=self.TEMP_TYPE)['min'],
                                                lst1[1].get_temperature(unit=self.TEMP_TYPE)['day'],
                                                lst1[1].get_humidity(),
                                                lst1[1].get_detailed_status()))

        else:
            final = ""
            for every in range(0,len(lst1)):
                additionalInfo = self.additionalInfo(lst1[every])
                final = final + ("{} Forecast. DAY {}: Maximum Temperature will be {} degree celsius. Minimum "
                                 "Temperature will be{} degree celsius. On an Average it will be around {} degree "
                                 "celsius. The Humidity remains,{} %. You can expect {} too.".format(self.WhereamI,
                                                                                                     every,
                                                    lst1[every].get_temperature(unit=self.TEMP_TYPE)['max'],
                                                    lst1[every].get_temperature(unit=self.TEMP_TYPE)['min'],
                                                    lst1[every].get_temperature(unit=self.TEMP_TYPE)['day'],
                                                    lst1[every].get_humidity(),
                                                    lst1[every].get_detailed_status()))
            #Return the Final response- the total forecast as requested
            return final

