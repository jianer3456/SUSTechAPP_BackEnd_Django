# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from Webfunc.function import *
from Market.Useful_function import *
import time
from Market.models import *
from Webfunc.models import *
import json
from django.http import HttpResponse
import sys
import datetime
from threading import Thread
reload(sys)
sys.setdefaultencoding('utf-8')
# Create your views here.


token_confirm = Token("dj!21e12d21[1;_KEY,Wohisyourdaddy")


def pushXKresult(xktime):
    """
    # result :   {"11612110":{"success":{"ClassName":"message"},"fail":{"ClassName":"message"}}}
    """
    def getTimeNow():
        now = datetime.datetime.now()
        return now.strftime("%Y%m%d%H%M")
    while True:
        if int(xktime) + 1 <= int(getTimeNow()):
            result = getAllXKresult()
            for usr, item in result.iteritems():
                user = User.objects.get(jwxt_usr=usr)
                info = ""
                if len(item["success"]) > 0:
                    for index, item in enumerate(item["success"]):
                        info += str(index) + "--" + item + "\n"
                if len(item["fail"]) > 0:
                    for index, item in enumerate(item["fail"]):
                        info += str(index) + "--" + item + "\n"
                if info:
                    sendmail(subject="选课结果", text=info, receivers=[
                             "%s@mail.sustc.edu.cn" % usr], kind="plain")
                    for user in user_list:
                        if user.usr == usr:
                            if user.xking:
                                user_list.remove(user)
            break
        time.sleep(1)


def setXKtime(request):
    response = myResponse(request)
    if request.method == 'POST':
        payload = request.POST
        time = payload.get("time")
        with open("info", "wb") as file:
            file.write(time)
            pushThread = Thread(target=pushXKresult, kwargs={"xktime": time})
            pushThread.setDaemon(True)
            pushThread.start()
        response.write("success")
    else:
        response.write("err")
    return response


def app_getKey(request):
    response = myResponse(request)
    if request.method == 'POST':
        payload = request.POST
        usr = payload.get('usr')
        token = token_confirm.generate_validate_token(usr)
        result = {"token": token}
        response = myResponse(request, result)
    else:
        response.write("err")
    return response


def login(request):
    response = myResponse(request)
    if request.method == 'POST':
        payload = request.POST
        user = payload.get('usr')
        word = payload.get('pwd')
        islogin, name, sid = Login(user, word)
        result = {"loginResult": islogin, "username": name, "sid": sid}
        response = myResponse(request, result)
    else:
        response.write("非法访问!")
    return response


def _getClassNameList(request):
    response = myResponse(request)
    if request.method == 'POST':

        payload = request.POST
        usr = payload.get('usr')
        pwd = payload.get('pwd')

        res = getClassNameList(usr, pwd)
        result = {"namelist": res}
        response = myResponse(request, result)
    else:
        response.write("非法访问!")
    return response


def _getClasstable(request):
    global cache_table_payload
    global cache_classTable
    response = myResponse(request)
    if request.method == 'POST':
        request.POST = request.POST.copy()

        payload = request.POST
        usr = payload.get('usr')
        pwd = payload.get('pwd')
        del payload["usr"]
        del payload["pwd"]
        del payload["getClasstable"]

        classnamelist = []
        for jjj in payload.itervalues():
            if jjj[0] == "@":
                classnamelist.append(str(jjj[1:]))
        result = getClasstable(classnamelist, usr, pwd)
        response = myResponse(request, result)
    else:
        response.write("非法访问!")
    return response


def _GetClassLink(request):
    response = myResponse(request)
    if request.method == 'POST':
        payload = request.POST
        usr = payload.get('usr')
        pwd = payload.get('pwd')
        num = payload.get("classNum")
        result = getClassLink(num, usr, pwd)
        response = myResponse(request, result)
    else:
        response.write("非法访问!")
    return response


def _getCheckPay(request):
    response = myResponse(request)
    if request.method == 'POST':
        payload = request.POST
        usr = payload.get('usr')
        pwd = payload.get('pwd')
        millis = int(round(time.time() * 1000))
        result = {"IsGetPayInAnyWay": millis}
        response = myResponse(request, result)
    else:
        response.write("非法访问!")
    return response


def _getClassXKed(request):
    response = myResponse(request)
    if request.method == 'POST':
        payload = request.POST
        usr = payload.get('usr')
        pwd = payload.get('pwd')
        num = payload.get("classNum")
        key = payload.get("key")

        try:
            token = token_confirm.confirm_validate_token(key)
        except Exception as e:
            result = {"result": "badtoken"}
            response = myResponse(request, result)
            return response
        else:
            if usr != token_confirm.confirm_validate_token(key):
                result = {"result": "badtoken"}
                response = myResponse(request, result)
                return response

        with open("info", "r") as file:
            time = file.read()

        if startXK(order=num, time=time, usr=usr, pwd=pwd):
            result = {"result": True}
        else:
            result = {"result": False}
        response = myResponse(request, result)
    else:
        response.write("ERROR!")
    return response


def myResponse(request, dictcontent=None):
    if dictcontent == None:
        response = HttpResponse()
    else:
        response = HttpResponse(json.dumps(dictcontent))
    response["Access-Control-Allow-Origin"] = request.META.get("HTTP_ORIGIN")
    response["Access-Control-Allow-Credentials"] = "true"
    return response
