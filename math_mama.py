'''
#######################################################################
 __  __       _   _           __  __
|  \/  | __ _| |_| |__       |  \/  | __ _ _ __ ___   __ _
| |\/| |/ _` | __| '_ \ _____| |\/| |/ _` | '_ ` _ \ / _` |
| |  | | (_| | |_| | | |_____| |  | | (_| | | | | | | (_| |
|_|  |_|\__,_|\__|_| |_|     |_|  |_|\__,_|_| |_| |_|\__,_|

 __  __           _       _
|  \/  | ___   __| |_   _| | ___
| |\/| |/ _ \ / _` | | | | |/ _ \
| |  | | (_) | (_| | |_| | |  __/
|_|  |_|\___/ \__,_|\__,_|_|\___|

######################################################################
'''



import math

class math_mama():
    def __init__(self):
        pass

    def add(self,*argv):
        list1 = argv[0]
        return self.ResponseGen(sum(list1))

    def diff(self,*argv):
        list1 = argv[0]
        return self.ResponseGen(list1[0]-sum(list1[1:]))

    def multiply(self,*argv):
        list1=argv[0]
        try:
            total = 1
            for each in list1:
                total = each * total
        except:
            if len(list1) == 1:
                return list1[0]
            else:
                return 1
        return self.ResponseGen(total)

    def divide(self,*argv):
        list1 = argv[0]
        return list1[0]/self.multiply(list1[1:])

    def power(self,*argv):
        list1 = argv[0]
        return self.ResponseGen(math.pow(list[0],list[1]))

    def sqRoot(self,*argv):
        list1 = argv[0]
        return self.ResponseGen(math.sqrt(list1[0]))

    def exponential(self,*argv):
        list1 = argv[0]
        return self.ResponseGen(math.exp(list1[0]))

    def ResponseGen(self,finalValue):
        return " The total comes up to {}".format(finalValue)

