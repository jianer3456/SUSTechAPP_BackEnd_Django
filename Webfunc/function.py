# -*- coding: UTF-8 -*-
from jwxt_ClassProcess import *
import time
from threading import Thread
import base64
ONLINE_INTERVAL = 1800
CHECK_INTERVAL = 1790

user_list = []

def getOnlineUsers():
    global user_list
    return len(user_list)

def CleanUser():
    global user_list
    global ONLINE_INTERVAL
    global CHECK_INTERVAL
    if len(user_list)!=0:
        for user in user_list:
            if user.logintime + ONLINE_INTERVAL >= time.time() and user.xking==False:
                user_list.remove(user)
    time.sleep(CHECK_INTERVAL)
    cleanThread = Thread(target=CleanUser)

cleanThread = Thread(target=CleanUser)
cleanThread.setDaemon(True)
cleanThread.start()

def Login(userName,password):
    # global cp
    # global isLogin
    cp = Class_Process(userName,password)
    isLogin = cp.login.sucess
    name = cp.login.user_name
    sid = cp.login.user_sid

    cp.logintime = time.time()
    cp.pwd = password
    cp.usr = userName
    cp.name = name

    for user in user_list:
        if user.usr==userName:
            return isLogin,name,sid        

    cp.xking = False
    if isLogin:
        user_list.append(cp)
    return isLogin,name,sid

def getClassNameList(sid,pwd):
    global user_list
    if len(user_list)!=0:
        for user in user_list:
            if user.usr==sid and user.pwd==pwd:
                Classname = user.showAllClassName()        
                res = ""
                for i in Classname:
                    res += i+"@"
                return res
    return "未登录"
    

def getClasstable(classNamelist,usr,pwd):
    global user_list
    if len(user_list)!=0:
        for user in user_list:
            if user.usr==usr and user.pwd==pwd:
                tablelist = user.GetAllPossibleClassList(classNamelist)[0:50]
                user.tablelist = tablelist
                order = 0
                resultDic = {}
                for table in tablelist:
                    Table = {}
                    classOrder = 0
                    for i in table:
                        Obj = {}
                        Obj["class_name"] = i.Class_name
                        Obj["major"] = i.Class_major
                        Obj["time"] = i.Class_time_code
                        Obj["loc"] = i.Class_location
                        Obj["teacher"] = i.Class_teacher
                        Obj["point"] = i.score
                        Table["_"+str(classOrder)] = Obj
                        classOrder += 1
                    resultDic["_"+str(order)] = Table
                    order += 1
                return resultDic
    return "未登录"

def getClassLink(num,usr,pwd):
    global user_list
    if len(user_list)!=0:
        for user in user_list:
            if user.usr==usr and user.pwd==pwd:
                if len(user.tablelist)>=1:
                    return user.getXKlink(user.tablelist[int(num)-1])
                else:
                    return []
    return "未登录"

def gotoXK(**kwargs):
    order = kwargs.get("order")
    user = kwargs.get("user")
    time = kwargs.get("time")
    user.chooseAtTime(str(time),user.tablelist[int(order)-1])

def startXK(order,time,usr,pwd):
    global user_list
    if len(user_list)!=0:
        for index,user in enumerate(user_list):
            if user.usr==usr and user.pwd==pwd and user.xking==False:
                try:
                    user.tryChooseClass(user.tablelist[int(order)-1])
                    XKThread = Thread(target=gotoXK,kwargs={"order":order,"user":user,"time":time})
                    XKThread.setDaemon(True)
                    XKThread.start()
                    user_list[index].xking = True
                except Exception as e:
                    print e
                    user_list[index].xking = False
                    return False
                else:
                    user_list[index].xking = True
                    return True
    return "未登录"


def getAllXKresult():
    """
    @ result :   {"11612110":{"success":{"ClassName":"message"},"fail":{"ClassName":"message"}}}
    """
    global user_list
    result = {}
    for user in user_list:
        if user.xking==True or user.login.XK_success_result or user.login.XK_fail_result:
            success = user.login.XK_success_result
            fail = user.login.XK_fail_result
            result[user.usr]={"success":success,"fail":fail}
    return result

from itsdangerous import URLSafeTimedSerializer as utsr
class Token:
    def __init__(self, security_key):
        self.security_key = security_key
        self.salt = base64.encodestring(security_key)
    def generate_validate_token(self, username):
        serializer = utsr(self.security_key)
        return serializer.dumps(username, self.salt)
    def confirm_validate_token(self, token, expiration=86400):
        serializer = utsr(self.security_key)
        return serializer.loads(token, salt=self.salt, max_age=expiration)
    def remove_validate_token(self, token):
        serializer = utsr(self.security_key)
        return serializer.loads(token, salt=self.salt)