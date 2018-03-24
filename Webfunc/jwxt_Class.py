# -*- coding: UTF-8 -*-
class Class(object):
    """docstring for Class_info"""
    score = 0
    Class_name = ""
    Class_code = []
    Class_major = ""
    # 班级号码
    Class_number = ""

    Class_time = ""
    Class_time_code = ""

    # 课程类别（用来选课）  
    # JHXK    KZYXK KNJXK   GXK    MR默认值
    Class_Type = "MR"

    Class_teacher = ""

    Class_location = ""
    # 一教二教教工之家都为山下1   荔园为0 (其他为1)
    Class_location_code = ""

    # if is English
    Class_HowHard = None

    Class_isNecessary = None

    date = ""
    xkID = ""
    def __init__(self,score,Class_name,Class_code,Class_major,Class_number,Class_time,Class_teacher,Class_location,xkID,Class_HowHard=None,Class_isNecessary=None,Class_Type="MR"):
        self.score = score
        self.Class_name = Class_name
        self.Class_code = Class_code
        self.Class_major = Class_major
        self.Class_number = Class_number
        self.Class_time = Class_time
        self.Class_teacher = Class_teacher
        self.Class_location = Class_location
        self.Class_HowHard = Class_HowHard
        self.Class_isNecessary = Class_isNecessary
        self.xkID = xkID
        self.Class_Type = Class_Type
        self.Class_location_code = self.getLocation_code()
        self.Class_time_code = self.getTime_code()

    def getTime_code(self):
        a = str(self.Class_time)
        time_code = []
        for i in a.split("<br>"):
            infoTuple = i.split(" ")
            week = infoTuple[-3] 
            day = infoTuple[-2]
            classNum = infoTuple[-1]
            c = classNum[0:-3]
            a = c.split("-")
            num=""
            for i in a:
                num += "|"+str(i)
            result = day+num
            time_code.append(result)
        return time_code   
    def getLocation_code(self):
        if "荔园" or "慧园" in self.Class_location:
            return 0
        return 1

        