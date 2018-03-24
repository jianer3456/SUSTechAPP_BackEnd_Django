# -*- coding: UTF-8 -*-
from jwxt_Login import Login
from jwxt_Class import Class
import os
import pickle
import datetime
import time
import sys
import urllib2
from prettytable import PrettyTable
from itertools import *
reload(sys)
sys.setdefaultencoding('utf8')
# 需求：账号密码    显示选课单     输入课程名称   输出课程表    选择课程表    自动选课


class Class_Process(object):
    """docstring for ClassProcess"""
    login = ""
    JHXK_ClassList = []
    KZYXK_ClassList = []
    KNJXK_ClassList = []
    GXK_ClassList = []
    saveList = []
    Class_Date = ""
    filename = ""
    # 所有课程列表
    All_ClassList = []
    PreChooseClassList = []

    def __init__(self, usr, psw):
        # 测试时不登录
        self.filename = usr + "xkData.txt"
        self.initLogin(usr, psw)
        if self.login.sucess:
            if os.path.exists(self.filename):
                self.load_ClassDataToList()
                # print "加载选课数据成功"
            else:
                try:
                    self.initAllClassList()
                    self.save_ClassDataToFile()
                    # print "保存选课数据成功"
                except Exception as e:
                    # print "从服务器初始化数据失败，加载本地数据"
                    self.filename = "xkData.txt"
                    self.load_ClassDataToList()
                    pass

    def initLogin(self, usr, psw):
        if usr != "" and psw != "":
            self.login = Login(usr, psw)
            if not self.login.sucess:
                # print "登录失败，使用默认数据集"
                self.filename = "xkData.txt"

    def initAllClassList(self):
        self.JHXK_ClassList = self.initClassToClassList(
            self.getJHXKinfo(), "JHXK")
        self.KZYXK_ClassList = self.initClassToClassList(
            self.getKZYXKinfo(), "KZYXK")
        self.KNJXK_ClassList = self.initClassToClassList(
            self.getKNJXKinfo(), "KNJXK")
        self.GXK_ClassList = self.initClassToClassList(
            self.getGXKinfo(), "GXK")
        self.All_ClassList = self.JHXK_ClassList + self.KZYXK_ClassList + \
            self.KNJXK_ClassList + self.GXK_ClassList

    def showAllClassName(self):
        # nameList = []
        oblist = []
        for i in self.All_ClassList:
            # if not i.Class_name in oblist:
            Stss = i.Class_name + "$" + \
                str(i.score) + "$" + i.Class_major + "$" + i.Class_location
            oblist.append(str(Stss))
            # nameList.append(i)
        return oblist

    def initClassToClassList(self, RawClassInfo, CLASSTYPE):
        classListData = RawClassInfo["aaData"]
        ClassList = []
        for i in classListData:
            # 不存在为null
            name = i["kcmc"]
            major = i["dwmc"]

            # 体育为 类型如散打    其他课程为null
            num = i["fzmc"]

            if num != None:
                name += "-" + num

            xkid = i["jx0404id"]
            time = i["sksj"]

            if time == "&nbsp;":
                continue
            code = i["kch"]
            teacher = i["skls"]

            if "英语" in name:
                name += "-" + teacher

            location = i["skdd"]
            # 学分！！！
            score = i["xf"]
            # 以下数据还不知道
            howHard = None
            isNecessary = None

            newClass = Class(score, name, code, major, num, time,
                             teacher, location, xkid, howHard, isNecessary, CLASSTYPE)
            newClass.date = i["xnxq01id"]
            self.Class_Date = newClass.date
            ClassList.append(newClass)
        return ClassList

    def getJHXKinfo(self):
        url = "http://jwxt.sustc.edu.cn/jsxsd/xsxkkc/xsxkBxqjhxk?kcxx=&skls=&skxq=&skjc=&sfym=false&sfct=false"
        return self.login.getRawClass_Info(url)

    def getKZYXKinfo(self):
        url = "http://jwxt.sustc.edu.cn/jsxsd/xsxkkc/xsxkFawxk?kcxx=&skls=&skxq=&skjc=&sfym=false&sfct=false"
        return self.login.getRawClass_Info(url)

    def getGXKinfo(self):
        url = "http://jwxt.sustc.edu.cn/jsxsd/xsxkkc/xsxkGgxxkxk?kcxx=&skls=&skxq=&skjc=&sfym=false&sfct=false&szjylb="
        return self.login.getRawClass_Info(url)

    def getKNJXKinfo(self):
        url = "http://jwxt.sustc.edu.cn/jsxsd/xsxkkc/xsxkKnjxk?kcxx=&skls=&skxq=&skjc=&sfym=false&sfct=false"
        return self.login.getRawClass_Info(url)

    def save_ClassDataToFile(self):
        self.saveList = [self.JHXK_ClassList, self.KZYXK_ClassList,
                         self.GXK_ClassList, self.KNJXK_ClassList]
        file = open(self.filename, 'wb')
        pickle.dump(self.saveList, file)
        file.close()

    def load_ClassDataToList(self):
        file = open(self.filename, 'rb')
        self.saveList = pickle.load(file)
        file.close()
        self.JHXK_ClassList = self.saveList[0]
        self.KZYXK_ClassList = self.saveList[1]
        self.GXK_ClassList = self.saveList[2]
        self.KNJXK_ClassList = self.saveList[3]
        self.All_ClassList = self.JHXK_ClassList + self.KZYXK_ClassList + \
            self.KNJXK_ClassList + self.GXK_ClassList

    def showClassTable(self, aClassList=None, showTeacher=False):
        x = PrettyTable()
        x.padding_width = 1
        if aClassList == None:
            return
        cl_list = ["节数", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        # 星期五|3|4
        for iTitle in cl_list:
            if iTitle == "节数":
                x.add_column("节数", ["1", "2", "3", "4", "5",
                                    "6", "7", "8", "9", "10", "11", "12"])
            info_list = []
            for i in range(0, 12):
                info_list.append("")
            for Class in aClassList:
                for _Class_time_code in Class.Class_time_code:
                    if _Class_time_code[0:9] == iTitle:
                        code = _Class_time_code[9:].split("|")
                        #eg|3|6 ----- ['', '3', '6']
                        for j in range(int(code[1]), int(code[2]) + 1):
                            # eg :[3, 4, 5, 6]
                            if j != "":
                                if showTeacher:
                                    info_list[int(
                                        j) - 1] = str(Class.Class_name) + " " + str(Class.Class_teacher)
                                else:
                                    info_list[int(
                                        j) - 1] = str(Class.Class_name)
                            # else:

            if iTitle != "节数":
                x.add_column(iTitle, info_list)
        x.align = "r"
        return str(x)
    # 无偏好排课函数

    def chooseClassByNameList(self, whenTochoose, wantToChooseClassList):
        self.GetPreChooseClass(wantToChooseClassList)
        TotalPossibleDic = self.countList()
        chosssss = []
        for i in self.PreChooseClassList:
            for name, classlis in TotalPossibleDic.iteritems():
                if i.Class_name == name:
                    chosssss += classlis
        self.chooseAtTime(whenTochoose, chosssss)

    def isClassTableOK(self, ClassTable):
        # [class1,class2]
        ClassTable = list(ClassTable)
        for i in ClassTable:
            ClassTable.remove(i)
            if not self.isJoinable(i, ClassTable):
                return False
        return True

    def isClassRepeated(self, classtable):
        classtable = list(classtable)
        for i in classtable:
            main = i.Class_name
            sub = i.Class_number
            stringMainName = main[0:len(main) - len(sub) - 1]
            classtable.remove(i)
            for j in classtable:
                main1 = j.Class_name
                sub1 = j.Class_number
                stringMainName1 = main[0:len(main1) - len(sub1) - 1]
                if stringMainName == stringMainName1:
                    return False
        return True

    def ChooseByClassList(self, classlist):
        for i in classlist:
            self.login.chooseByClassObject(i)

    def GetAllPossibleClassList(self, wantToChooseClassList, LoseClass=2, wantTeacher=None, wantLocation=None, wantFirstClass=None):
        # 课程名称转化为对象
        self.PreChooseClassList = []
        self.GetPreChooseClass(wantToChooseClassList)
        TotalPossibleDic = self.countList()
        # {“课程名称”：【有相同课程名称的课程对象】}
        # 课程对象列表   可能有名称重复---  时间冲突   ，计算累计学分   输出为【【list1】，【】，【】】
        listNum = 1
        for i in TotalPossibleDic.itervalues():
            listNum *= len(i)

        self.tempClasstable = []
        self.AllFinalOK_ClassList = []

        for i in range(0, len(self.PreChooseClassList)):
            a = combinations(self.PreChooseClassList, i + 1)
            for j in a:
                if self.isClassTableOK(j) and self.isClassRepeated(j):
                    self.AllFinalOK_ClassList.append(j)
        self.AllFinalOK_ClassList.reverse()
        return self.AllFinalOK_ClassList

    def isJoinable(self, Class, classlist):
        if (not self.isSameClassNameInTheList(Class, classlist)) and self.isTimeOK(Class, classlist):
            return True
        return False

    # wantToChooseClassList为用户想要选择的课程名称列表
    def GetPreChooseClass(self, wantToChooseClassList):
        for i in wantToChooseClassList:
            for j in self.All_ClassList:
                if i in j.Class_name:
                    self.PreChooseClassList.append(j)

        # for i in self.PreChooseClassList:

    # 统计重复的课程数目  并返回总共可能的排序数目

    # 产生可选的课程列表  按照学分高低划分
    def GetChoosableClass(self):
        return

    def countList(self):
        countDic = {}
        for i in self.PreChooseClassList:
            if i.Class_name not in countDic:
                countDic[i.Class_name] = []
                countDic[i.Class_name].append(i)
            else:
                countDic[i.Class_name].append(i)
        return countDic
    # 改为class，和list

    def isTimeOK(self, Class, classlist):
        for i in classlist:
            if not self.isTimeCodeOK(i.Class_time_code, Class.Class_time_code):
                return False
        return True

    def isTimeCodeOK(self, timeCode1, timeCode2):
        for i in timeCode1:
            for j in timeCode2:
                if i[0:9] == j[0:9]:
                    for mm in i[10:].split("|"):
                        for nn in j[10:].split("|"):
                            if mm == nn:
                                return False
        return True

    def isSameClassNameInTheList(self, Class, ChosenClassList):
        for i in ChosenClassList:
            if i.Class_name == Class.Class_name:
                return True
        return False

    def getTimeNow(self):
        now = datetime.datetime.now()
        return now.strftime("%Y%m%d%H%M")

    def chooseAtTime(self, whenTochoose, classlist):
        while True:

            if int(whenTochoose) <= int(self.getTimeNow()):
                for i in classlist:
                    self.Class_Date = i.date
                try:
                    self.ChooseByClassList(classlist)
                except Exception as e:
                    pass
                if (len(self.login.XK_fail_result) + len(self.login.XK_success_result)) >= len(classlist):
                    break
            # 201705222200
            if int(whenTochoose) + 2 <= int(self.getTimeNow()):
                break
            time.sleep(1)

    def tryChooseClass(self, classlist):
        self.ChooseByClassList(classlist)

    def isNetworkOK(self):
        try:
            urllib2.urlopen("http://www.baidu.com")
            return True
        except Exception as e:
            return False

    def getXKlink(self, classOBlist):
        result = {}
        for j in classOBlist:
            result[j.Class_name] = self.login.getXKlinkByClassObject(j)
        return result


def countScore(classlist):
    score = 0
    for i in classlist:
        score += i.score
    return score
