# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import cPickle as pickle
import json
import os
from django.core.files.base import ContentFile
from django.shortcuts import render
from django.contrib.auth import authenticate
import base64
import uuid
from django.http import HttpResponse
from Webfunc.jwxt_Login import *
from AttachedModule import *
from ratelimit.decorators import ratelimit
token_confirm = Token(django_settings.SECRET_KEY)
import random

from SUSTechAPP_Market.settings import DEBUG


@async
def ServerInit():
    pass


if not DEBUG:
    Thread(target=upDateInfo).start()
    ServerInit()

@Check_If_Available(NEED_PWD=False,NEED_JWXT=False,RETURN_VALUE=True)
@ratelimit(key='ip', rate='1000/h',block=True)
def getMainFunction(request):
    r = []
    for item in MainPageInfo.objects.all():
        r.append(item.toJson())
    return r

@Check_If_Available(NEED_PWD=False,NEED_JWXT=False,RETURN_VALUE=True)
@ratelimit(key='ip', rate='1000/h',block=True)
def getMainInfo(request):
    data = {}
    sell = SellInfo.objects.all()
    academic = AcademicForumInfo.objects.all()
    officialactivity = OfficialActivity.objects.all()
    blamewall = Blame_Wall.objects.all()
    if blamewall:
        blamewall = blamewall[len(blamewall)-1]
        data["blamewall"] = blamewall.toJson()
    if sell:
        sell = sell[len(sell)-1]
        data["sell"] = sell.toJson()
    if academic:
        academic = academic[0]
        data["academic"] = academic.toJson()
    if officialactivity:
        officialactivity=officialactivity[len(officialactivity)-1]
        data["officialactivity"] = officialactivity.toJson()
    phonenumber = request.POST.get("phonenumber")
    password = request.POST.get("password")
    if phonenumber:
        user = User.objects.get(phonenumber=phonenumber,password=password)
        data["appmsg"] = gogetAppMsg(user)
        data["nextclass"] = gogetNextClassInfo(user)
    else:
        data["nextclass"] = '未登录'
        data["appmsg"] = '未登录'
    return data


@Check_If_Available(NEED_PWD=True,NEED_JWXT=False,RETURN_VALUE=True)
@ratelimit(key='ip', rate='1000/h',block=True)
def getLimitedBlameWallInfo(request, user=None):
    """
    # 需要改的字段:BlameWall,open_Blame_Wall,Blame_Wall,blame_wall_info
    
    """          
    # funcinfo,created = FunctionUsedTimes.objects.get_or_create(User.objects.get(jwxt_usr="11612110"))
    # funcinfo.open_Blame_Wall = funcinfo.open_Blame_Wall + 1
    # funcinfo.save()
    result = []
    blame_wall_info = Blame_Wall.objects.all()
    count = 0
    loadedNum = request.POST.get("id")
    loadedNum = int(loadedNum)
    if int(loadedNum)==-1:
        blame_wall_info.reverse()
    
    for item in blame_wall_info:
        if item.id >= int(loadedNum) and int(loadedNum)!=-1:
            continue
        r = {}
        r["label"] = item.label
        r["img"] = getCompressed_ImageBase64(item.user.headImage,target=HeadImageHeight)
        r["name"] = item.user.username
        r["user_id"] = item.user.id
        r["time"] = date_trans(item.pub_date)
        r["content"] = item.content
        r["id"] = item.id
        r["thumbs_num"] = item.star
        r["comments_num"] = item.comment
        if len(Blame_star.objects.filter(user=user,blameID=item.id))>=1:
            r["is_thumbs"] = True
        else:
            r["is_thumbs"] = False 
        result.append(r)
        count += 1
        if count==6:
            break
    if int(loadedNum)!=-1:
        result.reverse()
    return result

@Check_If_Available(NEED_PWD=False,NEED_JWXT=False,RETURN_VALUE=True)
@ratelimit(key='ip', rate='1000/h', block=True)
def changepwd(request, user=None):
    phonenumber = request.POST.get("phonenumber")
    password = request.POST.get("password")
    user = User.objects.get(phonenumber=phonenumber)
    if user:
        user.password = password
        user.save()
        return OPERATION_SUCCESS
    else:
        return OPERATION_FAIL

@Check_If_Available(NEED_PWD=True,NEED_JWXT=False,RETURN_VALUE=True)
@ratelimit(key='ip', rate='1000/h', block=True)
def getLimitedActivity(request, user=None):
    result = []
    activity_wall = Activity_Wall.objects.all()
    loadedNum = request.POST.get("id")
    loadedNum = int(loadedNum)
    if int(loadedNum)==-1:
        activity_wall.reverse()
    count = 0
    for item in activity_wall:
        if item.id >= int(loadedNum) and loadedNum!=-1:
            continue
        if item.is_show:
            r = {}
            r["img"] = getCompressed_ImageBase64(
                item.user.headImage, target=HeadImageHeight)
            r["name"] = item.user.username
            r["user_id"] = item.user.id
            r["time"] = date_trans(item.pub_date)
            r["content"] = item.content
            r["id"] = item.id
            r["title"] = item.title
            r["content_img"] = []
            r["startTime"] = dateTransForActivityTofront(
                item.startTime)
            r["endTime"] = dateTransForActivityTofront(item.endTime)
            r["num_people"] = item.num_people
            r["location"] = item.location
            if len(JoinActivity.objects.filter(user=user, activity=item)) >= 1:
                r["is_joined"] = True
            else:
                r["is_joined"] = False
            result.append(r)
            count += 1
        if count==6:
            break
    if int(loadedNum)!=-1:
        result.reverse()
    return result




@ratelimit(key='ip', rate='1000/h',block=True)
def getUserNumberInfo(request):
    response = myResponse(request)
    users = User.objects.all()
    result = len(users)
    # newUsers = [item for item in users if isToday(item.date_joined)]
    # result["new_user_today"] = len(newUsers)
    response.write(result)
    return response

@Check_If_Available(RETURN_VALUE=True)
@ratelimit(key='ip', rate='100/h',block=True)
def getDeltaDateForCT(request,zhanwei):
    return getDeltaDays()
    # return delta.days/7+1

def isToday(Date):
    """
    @传入日期对象 返回是否是今天
    """
    return Date.strftime("%Y%m%d")==datetime.now().strftime("%Y%m%d")

def highLevelTemplate(request):
    response = myResponse(request)
    if request.method == 'POST':
        phonenumber = request.POST.get("phonenumber")
        password = request.POST.get("password")
        content = request.POST.get("content")
        userResult = User.objects.filter(phonenumber=phonenumber,password=password)
        if len(userResult)==0:
            response.write("ERROR!")
        else:
            user = userResult[0]
            if user.is_jwxt_checked:
                pass
            else:
                response.write(NOT_ALLOWED)
    else:
        response.write("非法访问！")
    return response

@ratelimit(key='ip', rate='100/h',block=True)
def getClassTableByWeekday(request):
    response = myResponse(request)
    # Will be true if the same IP makes more than 5 POST
    # requests/minute.
    # was_limited = getattr(request, 'limited', False)
    if request.method == 'POST':
        phonenumber = request.POST.get("phonenumber")
        password = request.POST.get("password")
        date = request.POST.get("date")
        dateid = request.POST.get("id")
        # weekday = request.POST.get("weekday")
        userResult = User.objects.filter(phonenumber=phonenumber,password=password)
        if len(userResult)==0:
            response.write("ERROR!")
        else:
            user = userResult[0]
            if user.is_jwxt_checked:
                filename = ClassTablePickle+str(user.jwxt_usr)
                if os.path.exists(filename):
                    with open(filename,"rb") as file:
                        result = pickle.load(file)
                        if result:
                            if date:
                                r = result["classtable"][date]
                            else:
                                date = result["date"][int(dateid)]
                                r = result["classtable"][date]

                            result = []
                            for index,item in enumerate(r):
                                item["id"] = index
                                result.append(item)
                            # itemlist = []
                            # for item in r:
                            #     if item["weekday"] == str(arrow.now().weekday()):
                            #         itemlist.insert(0,item)
                            #     else:
                            #         itemlist.append(item)
                            response = myResponse(request,result)
                        else:
                            response.write(NEED_TIME)            
                else:
                    # InitUser_AfterChecked(user)
                    response.write(NEED_TIME)    
            else:
                response.write(NOT_ALLOWED)
    else:
        response.write("非法访问！")
    return response

@ratelimit(key='ip', rate='100/h',block=True)
def checkoutVersion(request):
    response = myResponse(request)
    response.write(APP_VERSION)
    return response    


@ratelimit(key='ip', rate='100/h',block=True)
def getWenjuan(request):
    response = myResponse(request)
    response.write(Wenjuan_url)
    return response    
    

@Check_If_Available(NEED_PWD=True,NEED_JWXT=True,RETURN_VALUE=True)
@ratelimit(key='ip', rate='10/h',block=True)
def updateUserInfo(request,user):
    InitUser_AfterChecked(user)
    return "success"



@Check_If_Available(NEED_PWD=True,NEED_JWXT=True,RETURN_VALUE=True)
@ratelimit(key='ip', rate='1000/h',block=True)
def getNextClass(request,user):
    return gogetNextClassInfo(user)

@Check_If_Available(NEED_PWD=True,NEED_JWXT=True,RETURN_VALUE=True)
@ratelimit(key='ip', rate='1000/h',block=True)
def getAppMsg(request,user):
    return gogetAppMsg(user)



@Check_If_Available(NEED_PWD=True,NEED_JWXT=True,RETURN_VALUE=True)
@ratelimit(key='ip', rate='100/h',block=True)
def editClassdetail(request,user):
    className = request.POST.get("classname")
    xuefen = request.POST.get("xuefen")
    zhuanye = request.POST.get("zhuanye")
    bixiu = request.POST.get("bixiu")
    jiaocai = request.POST.get("jiaocai")
    description = request.POST.get("description")
    with open(ClassDetailPickle,"rb") as f:
        classdetail = pickle.load(f)
        for (name,infoid),j in classdetail.iteritems():
            if name==className:
                
                break


@Check_If_Available(NEED_PWD=True,NEED_JWXT=True,RETURN_VALUE=True)
@ratelimit(key='ip', rate='100/h',block=True)
def getClassdetail(request,user):
    termid = request.POST.get("termid")
    classid = request.POST.get("classid")
    filename = ClassTablePickle+str(user.jwxt_usr)
    if os.path.exists(filename):
        with open(filename,"rb") as file:
            result = pickle.load(file)
            if result:
                date = result["date"][int(termid)]
                className = result["classtable"][date][int(classid)]["classname"]
                with open(ClassDetailPickle,"rb") as f:
                    classdetail = pickle.load(f)
                for (name,infoid),j in classdetail.iteritems():
                    if name==className:
                        detail = j
                        break
                if detail:
                    return detail
                else:
                    newClassId = len(classdetail)-1
                    detail[(className,newClassId)] = {"id":newClassId,"classname":className}
                    with open(ClassDetailPickle,"wb") as f:
                        pickle.dump(classdetail,f)
                    return {"id":newClassId,"classname":className}
    else:
        InitUser_AfterChecked(user)
        response.write(NEED_TIME)    

@ratelimit(key='ip', rate='1000/h',block=True)
def getClassTableAvailabeDate(request):
    response = myResponse(request)
    if request.method == 'POST':
        phonenumber = request.POST.get("phonenumber")
        password = request.POST.get("password")
        userResult = User.objects.filter(phonenumber=phonenumber,password=password)
        if len(userResult)==0:
            response.write("ERROR!")
        else:
            user = userResult[0]
            if user.is_jwxt_checked:
                filename = ClassTablePickle+str(user.jwxt_usr)
                if os.path.exists(filename):
                    with open(filename,"rb") as file:
                        result = pickle.load(file)
                        if result!={}:
                            r = []
                            for index,date in enumerate(result["date"]):
                                m = {}
                                m["id"] = index
                                m["fValue"] = date
                                info = date.split("-")
                                if info[-1]=="1":
                                    temp = info[0]+"年春季"
                                elif info[-1]=="2":
                                    temp = info[0]+"年秋季"
                                elif info[-1]=="3":
                                    temp = info[0]+"年暑假"
                                m["fName"] = temp
                                r.append(m)
                            response = myResponse(request,r)
                        else:
                            response.write(NEED_TIME)            
                else:
                    # InitUser_AfterChecked(user)
                    response.write(NEED_TIME)    
            else:
                response.write(NOT_ALLOWED)
    else:
        response.write("非法访问！")
    return response

@ratelimit(key='ip', rate='100/h',block=True)
def getOtherActivity(request):
    response = myResponse(request)
    if request.method == 'POST':
        result = {}
        result1 = []
        for item in ClubActivity.objects.all():
            r = {}
            r["title"] = item.title
            r["location"] = item.location
            r["content"] = item.content
            r["host"] = item.host
            r["time"] = item.time
            result1.append(r)
        result["clubactivity"] = result1
        result2 = []
        for item in OfficialActivity.objects.all():
            r = {}
            r["title"] = item.title
            r["location"] = item.location
            r["content"] = item.content
            r["host"] = item.host
            r["time"] = item.time
            result2.append(r)
        result["officialactivity"] = result2

        response = myResponse(request,result)
    else:
        response.write("非法访问！")
    return response

@ratelimit(key='ip', rate='10/h',block=True)
def jwxtResign(request):
    response = myResponse(request)
    if request.method == 'POST':
        phonenumber = request.POST.get("phonenumber")
        password = request.POST.get("password")
        jwxt_usr = request.POST.get("jwxt_usr")
        jwxt_pwd = request.POST.get("jwxt_pwd")
        email = jwxt_usr + "@mail.sustc.edu.cn"
        userResult = User.objects.filter(phonenumber=phonenumber,password=password)
        if len(userResult)==0:
            response.write("ERROR!")
        else:
            user = userResult[0]
            # try:
            userlogin = Login(jwxt_usr,jwxt_pwd)
            if userlogin.sucess:
                user.is_jwxt_checked = True
                user.isInfoFilled = True
                user.realname = userlogin.user_name
                user.jwxt_usr = jwxt_usr
                user.jwxt_pwd = jwxt_pwd
                user.save()
                InitUser_AfterChecked(user)
                response.write("success")
            else:
                response.write("wrongjwxt")      
            # except Exception as e:
            #     raise e
                response.write("fail")
    else:
        response.write("非法访问！")
    return response

@ratelimit(key='ip', rate='1000/h',block=True)
def getSellDetail(request):
    response = myResponse(request)
    if request.method == 'POST':
        sellid = request.POST.get("id")
        info = SellInfo.objects.get(id=sellid)
        r = {}
        r["goodsname"] = info.goodsname
        r["description"] = info.description
        r["price"] = info.price
        r["username"] = info.pub_user.username
        r["id"] = info.id
        r["flag"] = info.flag
        r["picture"] = getCompressed_ImageBase64(info.picture,target=ContentImageHeight)
        r["userheadimage"] = getCompressed_ImageBase64(info.pub_user.headImage,target=HeadImageHeight)
        r["userid"] = info.pub_user.id
        r["time"] = date_trans(info.pub_change_date)
        response = myResponse(request,r)
    else:
        response.write("非法访问！")
    return response

@ratelimit(key='ip', rate='1000/h',block=True)
def getAllMyData(request):
    response = myResponse(request)
    if request.method == 'POST':
        phonenumber = request.POST.get("phonenumber")
        password = request.POST.get("password")
        try:
            userResult = User.objects.filter(phonenumber=phonenumber,password=password)
            if len(userResult)==0:
                response.write("ERROR!")
            else:
                user = userResult[0]
                result = {}

                joinedlist = JoinActivity.objects.filter(user=user)
                result0 = []
                for item in joinedlist:
                    i = item.activity
                    r = {}
                    r["title"] = i.title
                    r["startTime"] = dateTransForActivityTofront(i.startTime)
                    r["endTime"] = dateTransForActivityTofront(i.endTime)
                    r["content"] = i.content
                    r["location"] = i.location
                    r["id"] = i.id
                    r["activityid"] = i.id
                    join_info = JoinActivity.objects.filter(activity=i)
                    r["num_joined"] = str(len(join_info))
                    result0.append(r)
                result0.reverse()
                result["joinedactivity"] = result0

                result1 = []
                sendinfo = SellInfo.objects.filter(pub_user=user)
                count = 0
                for i in sendinfo:
                    if i.is_dealed==False:
                        r = {}
                        r["goodsname"] = i.goodsname
                        r["price"] = i.price
                        r["detail"] = i.description
                        r["picture"] = getCompressed_ImageBase64(i.picture)
                        r["id"] = i.id
                        r["xid"] = count
                        r["sellid"] = i.id
                        r["flag"] = i.flag
                        count+=1
                        result1.append(r)
                result1.reverse()
                result["dealingData"] = result1
                
                result2 = []
                activityInfo = Activity_Wall.objects.filter(user=user)
                for i in activityInfo:
                    if i.is_show:
                        r = {}
                        r["title"] = i.title
                        r["startTime"] = dateTransForActivityTofront(i.startTime)
                        r["endTime"] = dateTransForActivityTofront(i.endTime)
                        r["content"] = i.content
                        r["location"] = i.location
                        r["id"] = i.id
                        r["activityid"] = i.id
                        join_info = JoinActivity.objects.filter(activity=i)
                        r["num_joined"] = str(len(join_info))

                        result2.append(r)
                result2.reverse()
                result["activityData"] = result2

                result3 = []
                result4 = []
                for wallInfo in Blame_Wall.objects.filter(user=user):
                    for star in Blame_star.objects.filter(blameID=wallInfo.id):
                        if star.user!=user and isToday(star.pub_date):
                            r = {}
                            r["name"]=star.user.username
                            r["img"]=getCompressed_ImageBase64(star.user.headImage,target=HeadImageHeight)
                            r["user_id"] = star.user.id
                            r["content"] = wallInfo.content
                            r["time"] = date_trans(star.pub_date)
                            result3.append(r)
                    for comment in Blame_comment.objects.filter(blameID=wallInfo.id):
                        if comment.user!=user and isToday(comment.pub_date):
                            r1 = {}
                            r1["name"]=comment.user.username
                            r1["img"]=getCompressed_ImageBase64(comment.user.headImage,target=HeadImageHeight)
                            r1["content"] = comment.content
                            r1["mycontent"] = wallInfo.content
                            r1["user_id"] = comment.user.id
                            r1["kind"] = "blame"
                            r1["blameid"] = wallInfo.id
                            r1["time"] = date_trans(comment.pub_date)
                            result4.append(r1)
                
                for sellinfo in SellInfo.objects.filter(pub_user=user):
                    for comment in Sell_comment.objects.filter(sellID=sellinfo.id):
                        if comment.user!=user:
                            r1 = {}
                            r1["name"]=comment.user.username
                            r1["img"]=getCompressed_ImageBase64(comment.user.headImage,target=HeadImageHeight)
                            r1["content"] = comment.content
                            r1["mycontent"] = sellinfo.description
                            r1["user_id"] = comment.user.id
                            r1["kind"] = "sell"
                            r1["blameid"] = sellinfo.id
                            r1["time"] = date_trans(comment.pub_date)
                            result4.append(r1)

                result3.reverse()
                result4.reverse()
                result["mystar"] = result3
                result["mycomment"] = result4
                response = myResponse(request,result)
        except Exception as e:
            raise e
            response.write("err")
    else:
        response.write("非法访问！")

    return response

def addActivityToCalendar(request):
    response = myResponse(request)
    if request.method == 'POST':
        phonenumber = request.POST.get("phonenumber")
        password = request.POST.get("password")
        infoid = request.POST.get("activityid")
        userResult = User.objects.filter(phonenumber=phonenumber,password=password)
        if len(userResult)==0:
            response.write("ERROR!")
        else:
            user = userResult[0]
            activity = Activity_Wall.objects.get(id=infoid)
            activity.num_people = activity.num_people+1
            activity.save()
            
            if user!=activity.user:
                pushinfo = str(JoinActivityInfo%(user.username,activity.title))
                to = activity.user.phonenumber
                jpushInfo(information=pushinfo,users=to)
            JoinActivity.objects.create(user=user,activity=activity)
            result = {}
            result["title"] = activity.title
            result["location"] = activity.location
            result["notes"] = activity.content
            result["start"] = activity.startTime
            result["end"] = activity.endTime
            result["calendarName"] = "My Activity"
            response = myResponse(request,result)   
    else:
        response.write("非法访问！")
    return response

@ratelimit(key='ip', rate='10/h',block=True)
def cancelActivity(request):
    response = myResponse(request)
    if request.method == 'POST':
        phonenumber = request.POST.get("phonenumber")
        password = request.POST.get("password")
        infoid = request.POST.get("activityid")
        userResult = User.objects.filter(phonenumber=phonenumber,password=password)
        if len(userResult)==0:
            response.write("ERROR!")
        else:
            user = userResult[0]
            activity = Activity_Wall.objects.get(id=infoid)
            if activity.user==user:
                userlist = []
                for item in JoinActivity.objects.filter(activity=activity):
                    if item.user!=user:
                        userlist.append(item.user.phonenumber)
                to = userlist
                pushinfo = DeleteActivity%(user.username,activity.title)
                jpushInfo(information=pushinfo,users=to)
                activity.delete()
            else:
                to = str(activity.user.phonenumber)
                pushinfo =  CancelActivity%(user.username,activity.title)
                jpushInfo(information=pushinfo,users=to)
                JoinActivity.objects.get(user=user,activity=activity).delete()
                if activity.num_people>0:
                    activity.num_people = activity.num_people-1
                activity.save()
            response.write("success")
    else:
        response.write("非法访问！")
    return response
    
@ratelimit(key='ip', rate='100/h',block=True)
def appointTeacher(request):
    response = myResponse(request)
    if request.method == 'POST':
        phonenumber = request.POST.get("phonenumber")
        password = request.POST.get("password")
        email = request.POST.get("email")
        selfdescroption = request.POST.get("selfdescroption")
        otherinfo = request.POST.get("otherinfo")
        reason = request.POST.get("reason")
        
        userResult = User.objects.filter(phonenumber=phonenumber,password=password)
        if len(userResult)==0:
            response.write("ERROR!")
        else:
            user = userResult[0]
            name = user.realname
            sid = user.jwxt_usr
            response.write("notopen")
# 发送邮件
    else:
        response.write("非法访问！")
    return response

@ratelimit(key='ip', rate='1000/h',block=True)
def getTeacherByID(request):
    response = myResponse(request)
    if request.method == 'POST':
        infoid = request.POST.get("id").split("order")[1]
        info = Teacher_Info.objects.filter(id=infoid)
        if len(info)>=1:
            teacher = info[0]
            result = {}
            result["name"] = teacher.name
            result["email"] = teacher.email
            response = myResponse(request,result)
    else:
        response.write("非法访问！")
    return response

@ratelimit(key='ip', rate='1000/h',block=True)
def getActivity(request):
    response = myResponse(request)
    if request.method == 'POST':
        phonenumber = request.POST.get("phonenumber")
        password = request.POST.get("password")
        userResult = User.objects.filter(phonenumber=phonenumber,password=password)
        if len(userResult)==0:
            response.write("ERROR!")
        else:
            user = userResult[0]
            funcinfo,created = FunctionUsedTimes.objects.get_or_create(user=user)
            funcinfo.open_Activity_Wall = funcinfo.open_Activity_Wall + 1
            funcinfo.save()
            result = []
            for item in Activity_Wall.objects.all():
                if item.is_show:
                    r = {}
                    r["img"] = getCompressed_ImageBase64(item.user.headImage,target=HeadImageHeight)
                    r["name"] = item.user.username
                    r["user_id"] = item.user.id
                    r["time"] = date_trans(item.pub_date)
                    r["content"] = item.content
                    r["id"] = item.id
                    r["title"] = item.title
                    r["content_img"] = []
                    r["startTime"] = dateTransForActivityTofront(item.startTime)
                    r["endTime"] = dateTransForActivityTofront(item.endTime)
                    r["num_people"] = item.num_people
                    r["location"] = item.location
                    if len(JoinActivity.objects.filter(user=user,activity=item))>=1:
                        r["is_joined"] = True
                    else:
                        r["is_joined"] = False 
                    result.append(r)
            result.reverse()
            response = myResponse(request,result)
    else:
        response.write("非法访问！")
    return response


@ratelimit(key='ip', rate='10/h',block=True)
def pubActivity(request):
    response = myResponse(request)
    if request.method == 'POST':
        phonenumber = request.POST.get("phonenumber")
        password = request.POST.get("password")
        content = request.POST.get("content")
        startTime = dateTransForActivity(request.POST.get("startTime"))
        endTime = dateTransForActivity(request.POST.get("endTime"))
        title = request.POST.get("title")
        limt_people = 0
        location = request.POST.get("location")
        userResult = User.objects.filter(phonenumber=phonenumber,password=password)
        if len(userResult)==0:
            response.write("ERROR!")
        else:
            user = userResult[0]
            # if user.is_jwxt_checked:
            #     activity = Activity_Wall.objects.create(user=user,title=title,startTime=startTime,endTime=endTime,limt_people=limt_people,content=content,location=location)
            #     JoinActivity.objects.create(user=user,activity=activity)
            #     activity.num_people = activity.num_people+1
            #     activity.save()
            #     response.write("success")
            # else:
            #     response.write(NOT_ALLOWED)
            activity = Activity_Wall.objects.create(user=user,title=title,startTime=startTime,endTime=endTime,limt_people=limt_people,content=content,location=location)
            JoinActivity.objects.create(user=user,activity=activity)
            activity.num_people = activity.num_people+1
            activity.save()
            response.write("success")
    else:
        response.write("非法访问！")
    return response


@ratelimit(key='ip', rate='70/h',block=True)
def getEasyBusInfo(request):
    global EasyBusInfo
    response = myResponse(request)
    if request.method == 'POST':
        with open(BusTimepickle,"rb") as timefile:
            bustime = pickle.load(timefile)
            result = ""
            timedict = bustime[weekdayOrWeekend()].iteritems()
            for station,item in timedict:
                min_minites = 10000
                min_bus = None
                for index,bustime in item.iteritems():
                    minites = timeDifference(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),bustime)
                    if minites<=min_minites:
                        min_bus = index
                        min_minites = minites
                if min_minites==10000:
                    result += station+"已经没有车了  "
                else:
                    if min_minites>=60:
                        result += station+"还有约"+str(min_minites/60)+"小时发车 "
                    elif min_minites==0:
                        result += station+"即将发车 "
                    else:
                        result += station+"还有"+str(min_minites)+"分钟发车 "
        response.write(result)
    else:
        response.write("非法访问！")
    return response

@ratelimit(key='ip', rate='30/h',block=True)
def LibResign(request):
    response = myResponse(request)
    if request.method == 'POST':
        phonenumber = request.POST.get("phonenumber")
        password = request.POST.get("password")
        libpwd = request.POST.get("libpwd")
        libusr = request.POST.get("libusr")
        userResult = User.objects.filter(phonenumber=phonenumber,password=password)
        if len(userResult)==0:
            response.write("ERROR!")
        else:
            user = userResult[0]
            if LoginToLibTest(libusr,libpwd):
                UserBooksInfo.objects.get_or_create(user=user,lib_usr=libusr,lib_pwd=libpwd)
                response.write("success")        
            else:
                response.write(NOT_CHECKED)        
    else:
        response.write("非法访问！")
    return response

@ratelimit(key='ip', rate='100/h',block=True)
def isLibResigned(request):
    response = myResponse(request)
    if request.method == 'POST':
        phonenumber = request.POST.get("phonenumber")
        password = request.POST.get("password")
        userResult = User.objects.filter(phonenumber=phonenumber,password=password)
        if len(userResult)==0:
            response.write("ERROR!")
        else:
            user = userResult[0]
            if len(UserBooksInfo.objects.filter(user=user))>0:
                response.write("resigned")
            else:
                response.write(NOT_RESIGNED)
    else:
        response.write("非法访问！")
    return response


@ratelimit(key='ip', rate='100/h',block=True)
def getWeather(request):
    response = myResponse(request)
    if request.method == 'POST':
        result = []
        obj,created = TodayWeather.objects.get_or_create(id=0)    
        response.write(obj.datetimeWea + " "+obj.nighttimeWea)
    else:
        response.write("非法访问！")
    return response

@ratelimit(key='ip', rate='100/h',block=True)
def getMainPagePicture(request):
    response = myResponse(request)
    if request.method == 'POST':
        result = []
        num_samples = 20
        listInfo = list(range(MainPagePicture.objects.count()))
        sample = random.sample(listInfo,num_samples if len(listInfo) > num_samples else len(listInfo))  
        allList = [MainPagePicture.objects.all()[i] for i in sample]
        for item in allList:
            r={}
            r["id"] = item.id
            r["fSmallImg"] = item.fSmallImg
            r["fBigImg"] = item.fBigImg
            r["keyword"] = item.keyword
            result.append(r)
        response = myResponse(request,result)
    else:
        response.write("非法访问！")
    return response
   
def putPictureWords(request):
    response = myResponse(request)
    if request.method == 'POST':
        phonenumber = request.POST.get("phonenumber")
        password = request.POST.get("password")
        word = request.POST.get("word")
        userResult = User.objects.filter(phonenumber=phonenumber,password=password)
        if len(userResult)==0:
            response.write("ERROR!")
        else:
            user = userResult[0]
            UpdatePicture(word)
    else:
        response.write("非法访问！")
    return response
    
@ratelimit(key='ip', rate='100/h',block=True)
def SearchBooks(request):
    response = myResponse(request)
    if request.method == 'POST':
        phonenumber = request.POST.get("phonenumber")
        password = request.POST.get("password")
        bookname = request.POST.get("bookname")
        userResult = User.objects.filter(phonenumber=phonenumber,password=password)
        if len(userResult)==0:
            response.write("ERROR!")
        else:
            user = userResult[0]
            funcinfo,created = FunctionUsedTimes.objects.get_or_create(user=user)
            funcinfo.search_books = funcinfo.search_books + 1
            funcinfo.save()
            result = findBooks(bookname)
            response = myResponse(request,result)
    else:
        response.write("非法访问！")
    return response

@ratelimit(key='ip', rate='10/h',block=True)
def OneKeyBorrowBooks(request):
    response = myResponse(request)
    if request.method == 'POST':
        phonenumber = request.POST.get("phonenumber")
        password = request.POST.get("password")
        userResult = User.objects.filter(phonenumber=phonenumber,password=password)
        if len(userResult)==0:
            response.write("ERROR!")
        else:
            user = userResult[0]
            funcinfo,created = FunctionUsedTimes.objects.get_or_create(user=user)
            funcinfo.borrow_books = funcinfo.borrow_books + 1
            funcinfo.save()
            res = UserBooksInfo.objects.filter(user=user)
            if len(res)==0:
                response.write(NOT_RESIGNED)
            else:
                lib = res[0]
                result = loginToLibAndAutoBorrow(lib.lib_usr,lib.lib_pwd)
                if result:
                    response = myResponse(request,result)
                else:
                    response.write(NOT_RESIGNED)
    else:
        response.write("非法访问！")
    return response

@ratelimit(key='ip', rate='10/h',block=True)
def putWallContent(request):
    response = myResponse(request)
    if request.method == 'POST':
        phonenumber = request.POST.get("phonenumber")
        password = request.POST.get("password")
        kind = request.POST.get("kind")
        content = request.POST.get("content")
        label = request.POST.get("label")
        userResult = User.objects.filter(phonenumber=phonenumber,password=password)
        if len(userResult)==0:
            response.write("ERROR!")
        else:
            user = userResult[0]
            if user.is_jwxt_checked:
                if kind=="blame":
                    Blame_Wall.objects.create(user=user,content=content,label=label)
                elif kind=="activity":
                    pass
                elif kind=="confession":
                    pass
                elif kind=="makefriends":
                    pass
            else:
                response.write(NOT_ALLOWED)
            # if kind=="blame":
            #     Blame_Wall.objects.create(user=user,content=content)
            #     response.write("success")
            # elif kind=="activity":
            #     pass
            # elif kind=="confession":
            #     pass
            # elif kind=="makefriends":
            #     pass
    else:
        response.write("非法访问！")
    return response

@ratelimit(key='ip', rate='100/h',block=True)
def doComment(request):
    response = myResponse(request)
    if request.method == 'POST':
        phonenumber = request.POST.get("phonenumber")
        password = request.POST.get("password")
        infoid = request.POST.get("id")
        kind = request.POST.get("kind")
        content = request.POST.get("content")
        userResult = User.objects.filter(phonenumber=phonenumber,password=password)
        if len(userResult)==0:
            response.write("ERROR!")
        else:
            user = userResult[0]
            # if user.is_jwxt_checked:
            #     if kind=="blame":
            #         wall = Blame_Wall.objects.get(id=infoid)
            #         wall.comment = wall.comment + 1
            #         wall.save()
            #         if user!=wall.user:
            #             to = str(wall.user.phonenumber)
            #             pushinfo =  CommentActivity%user.username
            #             jpushInfo(information=pushinfo,users=to)

            #         Blame_comment.objects.create(user=user,blameID=infoid,content=content)
            #     elif kind=="activity":
            #         pass
            #     elif kind=="sell":
            #         sell = SellInfo.objects.get(id=infoid)
            #         if user!=sell.pub_user:
            #             to = str(sell.pub_user.phonenumber)
            #             pushinfo =  CommentActivity%user.username
            #             jpushInfo(information=pushinfo,users=to)
            #         Sell_comment.objects.create(user=user,sellID=infoid,content=content)
            #     elif kind=="teacher":
            #         Teacher_comment.objects.create(user=user,teacherID=infoid,content=content)
            #     response.write("success")
            # else:
            #     response.write(NOT_ALLOWED)

            if kind=="blame":
                wall = Blame_Wall.objects.get(id=infoid)
                wall.comment = wall.comment + 1
                wall.save()
                if user!=wall.user:
                    to = str(wall.user.phonenumber)
                    pushinfo =  CommentActivity%user.username
                    jpushInfo(information=pushinfo,users=to)
                Blame_comment.objects.create(user=user,blameID=infoid,content=content)
            elif kind=="activity":
                pass
            elif kind=="sell":
                sell = SellInfo.objects.get(id=infoid)
                if user!=sell.pub_user:
                    to = str(sell.pub_user.phonenumber)
                    pushinfo =  CommentActivity%user.username
                    jpushInfo(information=pushinfo,users=to)
                Sell_comment.objects.create(user=user,sellID=infoid,content=content)
            elif kind=="teacher":
                Teacher_comment.objects.create(user=user,teacherID=infoid,content=content)
            response.write("success")
            
    else:
        response.write("非法访问！")
    return response

@ratelimit(key='ip', rate='1000/h',block=True)
def getComment(request):
    response = myResponse(request)
    if request.method == 'POST':
        phonenumber = request.POST.get("phonenumber")
        password = request.POST.get("password")
        infoid = request.POST.get("id")
        kind = request.POST.get("kind")
        userResult = User.objects.filter(phonenumber=phonenumber,password=password)
        if len(userResult)==0:
            response.write("ERROR!")
        else:
            user = userResult[0]
            # if user.is_jwxt_checked:
            #     comment_info_list = []
            #     if kind=="blame":
            #         comment_info_list = Blame_comment.objects.filter(blameID=infoid)
            #     elif kind=="activity":
            #         pass
            #     elif kind=="teacher":
            #         comment_info_list = Teacher_comment.objects.filter(teacherID=infoid)
            #     elif kind=="sell":
            #         comment_info_list = Sell_comment.objects.filter(sellID=infoid)
            #     result = []
            #     for item in comment_info_list:
            #         r = {}
            #         r["id"] = item.id
            #         r["userheadimage"] = getCompressed_ImageBase64(item.user.headImage)
            #         r["username"] = item.user.username
            #         r["time"] = date_trans(item.pub_date)
            #         r["content"] = item.content
            #         result.append(r)
            #     response = myResponse(request,result)
            # else:
            #     response.write(NOT_ALLOWED)

            comment_info_list = []
            if kind=="blame":
                comment_info_list = Blame_comment.objects.filter(blameID=infoid)
            elif kind=="activity":
                pass
            elif kind=="teacher":
                comment_info_list = Teacher_comment.objects.filter(teacherID=infoid)
            elif kind=="sell":
                comment_info_list = Sell_comment.objects.filter(sellID=infoid)
            result = []
            for item in comment_info_list:
                r = {}
                r["id"] = item.id
                r["userheadimage"] = getCompressed_ImageBase64(item.user.headImage,target=HeadImageHeight)
                r["username"] = item.user.username
                r["time"] = date_trans(item.pub_date)
                r["content"] = item.content
                r["user_id"] = item.user.id
                result.append(r)
            result.reverse()
            response = myResponse(request,result)
            
    else:
        response.write("非法访问！")
    return response


def getWhoStarBlameWall(request):
    response = myResponse(request)
    if request.method == 'POST':
        phonenumber = request.POST.get("phonenumber")
        password = request.POST.get("password")
        idinfo = request.POST.get("id")
        userResult = User.objects.filter(phonenumber=phonenumber,password=password)
        if len(userResult)==0:
            response.write("ERROR!")
        else:
            user = userResult[0]
            # if user.is_jwxt_checked:
            #     starBlameWall_info_list = Blame_star.objects.filter(blameID=idinfo)
            #     result = []
            #     for item in starBlameWall_info_list:
            #         r = {}
            #         r["img"] = getCompressed_ImageBase64(item.user.headImage)
            #         r["name"] = item.user.username
            #         r["time"] = date_trans(item.pub_date)
            #         result.append(r)
            #     response = myResponse(request,result)
            # else:
            #     response.write(NOT_ALLOWED)

            starBlameWall_info_list = Blame_star.objects.filter(blameID=idinfo)
            result = []
            for item in starBlameWall_info_list:
                r = {}
                r["img"] = getCompressed_ImageBase64(item.user.headImage,target=HeadImageHeight)
                r["name"] = item.user.username
                r["time"] = date_trans(item.pub_date)
                result.append(r)
            response = myResponse(request,result)
            
    else:
        response.write("非法访问！")
    return response

@ratelimit(key='ip', rate='20/h',block=True)
def starBlameWall(request):
    response = myResponse(request)
    if request.method == 'POST':
        phonenumber = request.POST.get("phonenumber")
        password = request.POST.get("password")
        infoid = request.POST.get("id")
        userResult = User.objects.filter(phonenumber=phonenumber,password=password)
        if len(userResult)==0:
            response.write("ERROR!")
        else:
            user = userResult[0]
            # if user.is_jwxt_checked:
            #     starobj,created = Blame_star.objects.get_or_create(user=user,blameID=int(infoid))
            #     if created:
            #         wall = Blame_Wall.objects.get(id=infoid)
                    
            #         if user!=wall.user:
            #             to = str(wall.user.phonenumber)
            #             pushinfo =  StarActivity%user.username
            #             jpushInfo(information=pushinfo,users=to)
                        
            
            #         wall.star = wall.star + 1
            #         wall.save()
            # else:
            #     response.write(NOT_ALLOWED)

            starobj,created = Blame_star.objects.get_or_create(user=user,blameID=int(infoid))
            if created:
                wall = Blame_Wall.objects.get(id=infoid)
                
                if user!=wall.user:
                    to = str(wall.user.phonenumber)
                    pushinfo =  StarActivity%user.username
                    jpushInfo(information=pushinfo,users=to)
                    
        
                wall.star = wall.star + 1
                wall.save()
            
    else:
        response.write("非法访问！")
    return response

def unstarBlameWall(request):
    response = myResponse(request)
    if request.method == 'POST':
        phonenumber = request.POST.get("phonenumber")
        password = request.POST.get("password")
        infoid = request.POST.get("id")
        userResult = User.objects.filter(phonenumber=phonenumber,password=password)
        if len(userResult)==0:
            response.write("ERROR!")
        else:
            user = userResult[0]
            # if user.is_jwxt_checked:
            #     wall = Blame_Wall.objects.get(id=infoid)
            #     wall.star = wall.star - 1
            #     wall.save()
            #     Blame_star.objects.get(user=user,blameID=infoid).delete()
            # else:
            #     response.write(NOT_ALLOWED)
            
            wall = Blame_Wall.objects.get(id=infoid)
            wall.star = wall.star - 1
            wall.save()
            Blame_star.objects.get(user=user,blameID=infoid).delete()
        
    else:
        response.write("非法访问！")
    return response

@ratelimit(key='ip', rate='100/h',block=True)
def getBlameWallInfo(request):
    """
    # 需要改的字段:BlameWall,open_Blame_Wall,Blame_Wall,blame_wall_info
    
    """
    response = myResponse(request)
    if request.method == 'POST':
        phonenumber = request.POST.get("phonenumber")
        password = request.POST.get("password")
        userResult = User.objects.filter(phonenumber=phonenumber,password=password)
        if len(userResult)==0:
            response.write("ERROR!")
        else:
            user = userResult[0]
            funcinfo,created = FunctionUsedTimes.objects.get_or_create(user=user)
            funcinfo.open_Blame_Wall = funcinfo.open_Blame_Wall + 1
            funcinfo.save()

            
            result = []
            blame_wall_info = Blame_Wall.objects.all()
            for item in blame_wall_info:
                r = {}
                r["img"] = getCompressed_ImageBase64(item.user.headImage,target=HeadImageHeight)
                r["name"] = item.user.username
                r["user_id"] = item.user.id
                r["time"] = date_trans(item.pub_date)
                r["content"] = item.content
                r["id"] = item.id
                r["thumbs_num"] = item.star
                r["comments_num"] = item.comment
                if len(Blame_star.objects.filter(user=user,blameID=item.id))>=1:
                    r["is_thumbs"] = True
                else:
                    r["is_thumbs"] = False 
                result.append(r)
            result.reverse()
            response = myResponse(request,result)
    else:
        response.write("非法访问！")
    return response


@ratelimit(key='ip', rate='100/h')
def getBusTime(request):
    response = myResponse(request)
    if request.method == 'POST':
        phonenumber = request.POST.get("phonenumber")
        password = request.POST.get("password")
        longitude = request.POST.get("longitude")
        latitude = request.POST.get("latitude")
        location = request.POST.get("location")
        time = request.POST.get("time")
        try:
            userResult = User.objects.filter(phonenumber=phonenumber,password=password)
            if len(userResult)==0:
                response.write("notregiste")
            else:
                user = userResult[0]
                funcinfo,created = FunctionUsedTimes.objects.get_or_create(user=user)
                funcinfo.getBusTime = funcinfo.getBusTime + 1
                funcinfo.save()

                with open(bustimeEngpickle,"rb") as timefile:
                    bustime = pickle.load(timefile)
                if longitude and latitude:
                    with open(BusTimepickle,"rb") as timefile:
                        bustime = pickle.load(timefile)
                    station = getLocationnameFromGPS(longitude=longitude,latitude=latitude,limit="bus")
                else:
                    station = location
                timedict = bustime[weekdayOrWeekend(time)][station]
                min_minites = 10000
                min_bus = None
                for index,bustime in timedict.iteritems():
                    minites = timeDifference(time,bustime)
                    if minites<=min_minites:
                        min_bus = index
                        min_minites = minites
                result = {}
                result["min_minites"] = min_minites
                if station=="ly":
                    station = "欣园"
                if station=="tsg":
                    station = "科研楼"
                result["station"] = station
                timelist = []
                if min_bus>1 and min_bus<len(timedict):
                    BusTimeInfoList = [timedict[min_bus-1 if min_bus>1 else 1],timedict[min_bus],timedict[min_bus+1 if min_bus<len(timedict) else len(timedict)]]
                elif min_bus==1:
                    BusTimeInfoList = [timedict[min_bus],timedict[min_bus+1]]
                elif min_bus==len(timedict):
                    BusTimeInfoList = [timedict[min_bus-1],timedict[min_bus]]
                for i,bustimeinfo in enumerate(BusTimeInfoList):
                    r = {}
                    i+=min_bus-1 if min_bus>1 else 1
                    r["index"] = "第"+str(i)+"班车"
                    r["time"] = bustimeinfo
                    timelist.append(r)
                result["otherinfo"] = timelist
                response = myResponse(request,result)
                # else:
                #     response.write("err")
        except Exception as e:
            response.write("err")
    else:
        response.write("非法访问！")
    return response



    
def addForumToCalendar(request):
    response = myResponse(request)
    if request.method == 'POST':
        phonenumber = request.POST.get("phonenumber")
        password = request.POST.get("password")
        forumid = request.POST.get("forumid")
        userResult = User.objects.filter(phonenumber=phonenumber,password=password)
        if len(userResult)==0:
            response.write("ERROR!")
        else:
            user = userResult[0]
            chosenforum = None
            print forumid
            for foruminfo in AcademicForumInfo.objects.all():
                if str(foruminfo.id) == forumid[-1]:
                    chosenforum = foruminfo
                    break
            UserJoinForumInfo.objects.create(user=user,Title=chosenforum.Title,Apartment=chosenforum.Apartment,Detail_url=chosenforum.Detail_url)
            result = {}
            result["start"] = str(getLectureDatetime(chosenforum.Time))
            result["end"] = str(getEndTime(result["start"],defaultForumTime))
            result["title"] = chosenforum.Apartment + "讲座"
            result["location"] = chosenforum.Location
            result["notes"] = chosenforum.Title
            result["calendarName"] = "讲座日程"
            response = myResponse(request,result)
    else:
        response.write("非法访问！")
    return response        

def getTeacherInfo(request):
    response = myResponse(request)
    if request.method == 'POST':
        result = []
        for teacher_info in Teacher_Info.objects.all():
            r = {}
            r["id"] = teacher_info.id
            r["position"] = teacher_info.position
            r["apartment"] = teacher_info.Apartment
            r["email"] = teacher_info.email
            r["telephone"] = teacher_info.telephone
            r["name"] = teacher_info.name
            r["detail_url"] = teacher_info.detail_url
            r["img_url"] = teacher_info.img_url
            result.append(r)
        response = myResponse(request,result)
    else:
        response.write("非法访问！")
    return response        

@Check_If_Available(NEED_PWD=True,NEED_JWXT=True,RETURN_VALUE=True)
@ratelimit(key='ip', rate='100/h',block=True)
def getGPAdetail(request,user):
    with open(GPApickle,"rb") as file:
        gpaInfo = pickle.load(file)
    AllTermInfo = gpaInfo[user.jwxt_usr]["FullGPAInfo"]["data"]["ed"]
    return AllTermInfo

@ratelimit(key='ip', rate='100/h',block=True)
def getGPAinfo(request):
    # global conf
    response = myResponse(request)
    if request.method == 'POST':
        phonenumber = request.POST.get("phonenumber")
        password = request.POST.get("password")
        # try:
        userResult = User.objects.filter(phonenumber=phonenumber,password=password)
        if len(userResult)==0:
            response.write("ERROR!")
        else:
            user = userResult[0]
            if user.is_jwxt_checked:
                userinfo = UserInfo.objects.get(user=user)
                result = {}
                result["TotalScore"] = userinfo.TotalScore
                result["TotalGPA"] = userinfo.TotalGPA
                ScoreBeated = 0
                GPAbeated = 0
                term = userinfo.SUSTech_Class[0:2]
                sameTermInfo = [item for item in UserInfo.objects.all() if item.SUSTech_Class.startswith(term)]
                count = len(sameTermInfo)
                result["compareNum"] = count
                for Alluserinfo in sameTermInfo:
                    if Alluserinfo.TotalGPA <= userinfo.TotalGPA:
                        GPAbeated += 1
                    if Alluserinfo.TotalScore <= userinfo.TotalScore:
                        ScoreBeated += 1
                result["GPAbeated"] = 1.0*GPAbeated/count*100
                result["ScoreBeated"] = 1.0*ScoreBeated/count*100
                
                
                with open(GPApickle,"rb") as file:
                    gpaInfo = pickle.load(file)
                #     print gpaInfo
                # file = open(GPApickle,"rb")
                # print pickle.load(file)
                # file.close()
                    # print conf.get("Directory","GPAPickleInfoFile")
                    # totalGPA,totalScores,GPA_List,compareList,TotalInfodict = getClassScores(user.jwxt_usr,user.jwxt_pwd)
                    info = gpaInfo[str(user.jwxt_usr)]
                    compareList = info.get("BestWorst")
                    # ClassName   GPA
                    r1 = []
                    try:
                        for (gpa,name) in compareList[0:len(compareList)/2]:
                            res = {}
                            res["ClassName"] = name
                            res["GPA"] = gpa
                            r1.append(res)
                        r2 = []
                        for (gpa,name) in compareList[len(compareList)/2:]:
                            res = {}
                            res["ClassName"] = name
                            res["GPA"] = gpa
                            r2.append(res)
                        result["WorstClass"] = r1
                        result["BestClass"] = r2
                    except:
                        result["WorstClass"] = []
                        result["BestClass"] = []
                response = myResponse(request,result)
            else:
                response.write(NOT_CHECKED)    
                # totalGPA,totalScores,GPA_List = getClassScores('11612110','123321')
        # except Exception as e:
        #     raise e
        
    else:
        response.write("非法访问！")
    return response
@ratelimit(key='ip', rate='10/h',block=True)
def getSustcMainNews(request):
    response = myResponse(request)
    if request.method == 'POST':
        result = []
        for news_info in SustcNewsInfo.objects.all():
            r = {}
            r["show_id"] = news_info.id
            r["title"] = news_info.title
            r["img_url"] = news_info.img_url
            r["news_url"] = news_info.newsUrl
            if r["title"]=="" or r["img_url"]=="" or r["news_url"]=="":
                pass
            else:
                result.append(r)
        response = myResponse(request,result)
    else:
        response.write("非法访问！")
    return response
        
def getSustcForumInfo(request):
    response = myResponse(request)
    if request.method == 'POST':
        phonenumber = request.POST.get("phonenumber")
        password = request.POST.get("password")
        try:
            userResult = User.objects.filter(phonenumber=phonenumber,password=password)
            if len(userResult)==0:
                pass
            else:
                user = userResult[0]
                funcinfo,created = FunctionUsedTimes.objects.get_or_create(user=user)
                funcinfo.getForumInfo = funcinfo.getForumInfo + 1
                funcinfo.save()
            result = []
            for forum_info in AcademicForumInfo.objects.all():
                item = {}
                item["id"] = forum_info.id
                item["Apartment"] = forum_info.Apartment 
                item["Title"] = forum_info.Title
                item["Lecturer"] = forum_info.Lecturer
                item["Time"] = forum_info.Time 
                item["Location"] = forum_info.Location
                item["Detail_url"] = forum_info.Detail_url
                # item["day"] = forum_info.day
                result.append(item)
            response = myResponse(request,result)
        except Exception as e:
            pass
    else:
        response.write("非法访问！")
    return response
        
def sell_deal(request):
    response = myResponse(request)
    if request.method == 'POST':
        phonenumber = request.POST.get("phonenumber")
        password = request.POST.get("password")
        dealed_id = request.POST.get("id")
        try:
            userResult = User.objects.filter(phonenumber=phonenumber,password=password)
            if len(userResult)==0:
                response.write("ERROR!")
            else:
                user = userResult[0]
                sendinfo = SellInfo.objects.all()
                for i in sendinfo:
                    if i.pub_user==user:
                        if str(i.id)==dealed_id:
                            i.is_dealed=True
                            i.save()
                            response.write("success")
                            return response
                response.write("err")
        except Exception as e:
            raise e
            response.write("err")
    else:
        response.write("非法访问！")

    return response

def getDealing(request):
    response = myResponse(request)
    if request.method == 'POST':
        phonenumber = request.POST.get("phonenumber")
        password = request.POST.get("password")
        try:
            userResult = User.objects.filter(phonenumber=phonenumber,password=password)
            if len(userResult)==0:
                response.write("ERROR!")
            else:
                user = userResult[0]
                sendinfo = SellInfo.objects.all()
                result = []
                count = 0
                for i in sendinfo:
                    if i.pub_user==user:
                        if i.is_dealed==False:
                            r = {}
                            r["goodsname"] = i.goodsname
                            r["price"] = i.price
                            r["detail"] = i.description
                            r["picture"] = getCompressed_ImageBase64(i.picture)
                            r["id"] = i.id
                            r["xid"] = count
                            count+=1
                            result.append(r)
                response = myResponse(request,result)
        except Exception as e:
            raise e
            response.write("err")
    else:
        response.write("非法访问！")

    return response

def getDealed(request):
    response = myResponse(request)
    if request.method == 'POST':
        phonenumber = request.POST.get("phonenumber")
        password = request.POST.get("password")
        try:
            userResult = User.objects.filter(phonenumber=phonenumber,password=password)
            if len(userResult)==0:
                response.write("ERROR!")
            else:
                user = userResult[0]
                sendinfo = SellInfo.objects.all()
                result = []
                # count = 0
                for i in sendinfo:
                    if i.pub_user==user:
                        if i.is_dealed==True:
                            r = {}
                            r["goodsname"] = i.goodsname
                            r["price"] = i.price
                            r["detail"] = i.description
                            r["picture"] = getCompressed_ImageBase64(i.picture)
                            r["id"] = i.id
                            # count+=1
                            result.append(r)

                response = myResponse(request,result)
        except Exception as e:
            raise e
            response.write("err")
    else:
        response.write("非法访问！")

    return response

def getUserQQ(request):
    response = myResponse(request)
    if request.method == 'POST':
        username = request.POST.get("username")
        try:
            userResult = User.objects.filter(username=username)
            if len(userResult)==0:
                response.write("ERROR!")
            else:
                user = userResult[0]
                response.write(user.QQnumber)
        except Exception as e:
            raise e
    else:
        response.write("非法访问！")
    return response

def getUserDetail(request):
    response = myResponse(request)
    if request.method == 'POST':
        userid = request.POST.get("userid")
        try:
            userResult = User.objects.filter(id=userid)
            if len(userResult)==0:
                response.write("ERROR!")
            else:
                user = userResult[0]
                result = {}
                result["QQ"] = user.QQnumber
                result["mail"] = user.email
                result["img"] = getCompressed_ImageBase64(user.headImage,target=HeadImageHeight)
                result["username"] = user.username
                result["joinedactivity"] = len(JoinActivity.objects.filter(user=user))
                result["pubedactivity"] = len(Activity_Wall.objects.filter(user=user))
                sendinfo = SellInfo.objects.all()
                dealed = 0
                dealing = 0
                for i in sendinfo:
                    if i.pub_user==user:
                        if i.is_dealed==True:
                            dealed+=1
                        else:
                            dealing+=1
                result["dealed"] = dealed
                result["dealing"] = dealing

                response = myResponse(request,result)

        except Exception as e:
            raise e
    else:
        response.write("非法访问！")
    return response

@ratelimit(key='ip', rate='10/h')
def uploadheadimage(request):
    # {data:base64,phonenumber:justep.Shell.phoneNumber.get()
    # ,password:justep.Shell.password.get()},

    response = myResponse(request)
    if request.method == 'POST':
        phonenumber = request.POST.get("phonenumber")
        password = request.POST.get("password")
        data = request.POST.get("data")
        try:
            userResult = User.objects.filter(phonenumber=phonenumber,password=password)
            if len(userResult)==0:
                response.write("ERROR!")
            else:
                user = userResult[0]
                picdata = data.split('base64,')[1].decode('base64')
                picname = phonenumber+"_"+"headimage.jpg"
                user.headImage = ContentFile(content=picdata,name=picname)
                user.save()
                response.write("success")
        except Exception as e:
            raise e
            response.write("err")
    else:
        response.write("非法访问！")

    return response

@ratelimit(key='ip', rate='4/h',block=True)
def sell_pub(request):
    response = myResponse(request)
    
    if request.method == 'POST':
        phonenumber = request.POST.get("phonenumber")
        password = request.POST.get("password")
        name = request.POST.get("name")
        price = request.POST.get("price")
        detail = request.POST.get("detail")
        image = request.POST.get("image")
        flag = request.POST.get("flag")
        try:
            userResult = User.objects.filter(phonenumber=phonenumber,password=password)
            if len(userResult)==0:
                # username is phonenumber when registing
                response.write("nouser")
            else:
                user = userResult[0]
                if len(SellInfo.objects.filter(pub_user=user,is_dealed=False))>4:
                    response.write("overnum")
                    return response
                if user.isInfoFilled==False:
                    response.write("notallowed")
                else:
                    obj = SellInfo.objects.create(goodsname=name,description=detail,price=price,pub_user=user,flag=flag)
                    if image!="null":
                        picdata = image.split('base64,')[1].decode('base64')
                        picname = phonenumber+"_"+str(uuid.uuid4())
                        obj.picture=ContentFile(content=picdata,name=picname)
                        obj.save()
                    response.write("success")
                
                # obj = SellInfo.objects.create(goodsname=name,description=detail,price=price,pub_user=user,flag=flag)
                # if image!="null":
                #     picdata = image.split('base64,')[1].decode('base64')
                #     picname = phonenumber+"_"+str(uuid.uuid4())
                #     obj.picture=ContentFile(content=picdata,name=picname)
                #     obj.save()
                # response.write("success")
        except Exception as e:
            raise e
            response.write("err")
    else:
        response.write("非法访问！")
    return response

@ratelimit(key='ip', rate='100/h',block=True)
def sell_get(request):
    response = myResponse(request)
    if request.method == 'POST':
        loaded_num = int(request.POST.get("getselldata"))
        if loaded_num=="":
            response.write("非法访问！")
        else:
            try:
                # allsellinfo = SellInfo.objects.all()
                sendinfo = SellInfo.objects.all()
                if loaded_num==0:
                    pass
                elif loaded_num==1:
                    result = []
                    for i in sendinfo:
                        if i.flag==0:
                            result.append(i)
                    sendinfo = result

                elif loaded_num==2:
                    result = []
                    for i in sendinfo:
                        if i.flag==1:
                            result.append(i)
                    sendinfo = result

                elif loaded_num==3:  
                    result = []
                    for i in sendinfo:
                        if i.flag==2:
                            result.append(i)
                    sendinfo = result  
                # total_data_len = len(allsellinfo)
                # if loaded_num < total_data_len:
                #     sendinfo = allsellinfo[loaded_num:loaded_num+5]
                # else:
                #     response.write("loaded")
                #     return response

                result = []
                count = 0
                for info in sendinfo:
                    if info.is_dealed==False:
                        try:
                            r = {}
                            r["goodsname"] = info.goodsname
                            r["description"] = info.description
                            r["price"] = info.price
                            r["username"] = info.pub_user.username
                            r["id"] = info.id
                            r["sellid"] = info.id
                            r["flag"] = info.flag
                            count += 1
                            r["picture"] = getCompressed_ImageBase64(info.picture)
                            r["userheadimage"] = getCompressed_ImageBase64(info.pub_user.headImage,target=HeadImageHeight)
                            r["userid"] = info.pub_user.id
                            r["time"] = date_trans(info.pub_change_date)
                            result.append(r)
                        except Exception as e:
                            continue
                result.reverse()
                response = myResponse(request,result)
            except Exception as e:
                raise e
                response.write("err")
    else:
        response.write("非法访问！")
    return response



@ratelimit(key='ip', rate='30/h',block=True)
def isPhoneRegisted(request):
    response = myResponse(request)
    if request.method == 'POST':
        phonenumber = request.POST.get("phonenumber")
        userResult = User.objects.filter(phonenumber=phonenumber)
        if len(userResult)==0:
            response.write("notregiste")
        else:
            response.write("registed")
    else:
        response.write("非法访问！")
    return response

@ratelimit(key='ip', rate='10/h',block=True)
def registe(request):
    response = myResponse(request)
    if request.method == 'POST':
        phonenumber = request.POST.get("phonenumber")
        password = request.POST.get("password")
        try:
            userResult = User.objects.filter(phonenumber=phonenumber)
            if len(userResult)==0:
                # username is phonenumber when registing
                user = User.objects.create(username=phonenumber,password=password,phonenumber=phonenumber)
                user.is_active = True
                user.save()
                response.write("success")
            else:
                response.write("errregisted")
        except Exception as e:
            raise e
            response.write("err")
    else:
        response.write("非法访问！")

    return response

@ratelimit(key='ip', rate='5/h',block=True)
def login(request):
    response = myResponse(request)
    if request.method == 'POST':
        phonenumber = request.POST.get("phonenumber")
        password = request.POST.get("password")
        try:
            userResult = User.objects.filter(phonenumber=phonenumber)
            if len(userResult)==0:
                # username is phonenumber when registing
                response.write("notregiste")
            else:
                userResult = User.objects.filter(phonenumber=phonenumber,password=password)
                if len(userResult)==0:
                    response.write("wrongpwd")
                else:
                    user = userResult[0]
                    ls_f = getCompressed_ImageBase64(user.headImage,target=HeadImageHeight)
                    # try:
                    #     with open(str(user.headImage),'rb') as f:
                    #         ls_f=base64.b64encode(f.read())
                    #         ls_f = "data:image/jpeg;base64,"+ls_f
                    # except Exception as e:
                    #     ls_f = ""
                    if user.is_jwxt_checked:
                        r = "checked"
                    else:
                        r = "notyet"
                    response = myResponse(request,{'username':user.username,"data":ls_f,"ischecked":r})
        except Exception as e:
            raise e
            response.write("err")
    else:
        response.write("非法访问！")
    return response

@ratelimit(key='ip', rate='60/h')
def getInfo(request):
    response = myResponse(request)
    if request.method == 'POST':
        phonenumber = request.POST.get("phonenumber")
        password = request.POST.get("password")
        try:
            userResult = User.objects.filter(phonenumber=phonenumber,password=password)
            if len(userResult)==0:
                # username is phonenumber when registing
                response.write("notregiste")
            else:
                user = userResult[0]
                qqnumber = user.QQnumber
                username = user.username
                # jwxt_usr = user.jwxt_usr
                # email = user.email
                response = myResponse(request,{'success':True,'qqnumber':qqnumber,'username':username})
                # response = myResponse(request,{'success':True,'qqnumber':qqnumber,'username':username,'jwxt_usr':jwxt_usr,'email':email})
        except Exception as e:
            raise e
            response.write("err")
    else:
        response.write("非法访问！")
    return response

@ratelimit(key='ip', rate='60/h',block=True)
def saveInfo(request):
    response = myResponse(request)
    if request.method == 'POST':
        phonenumber = request.POST.get("phonenumber")
        username = request.POST.get("username")
        password = request.POST.get("password")
        qqnumber = request.POST.get("qqnumber")
        try:
            userResult = User.objects.filter(phonenumber=phonenumber,password=password)
            if len(userResult)==0:
                # username is phonenumber when registing
                response.write("notregiste")
            else:
                usernameResult = User.objects.filter(username=username)
                if len(usernameResult)>0 and usernameResult[0]!=userResult[0]:
                    response.write("username_used")
                else:
                    user = userResult[0]
                    user.username = username
                    user.QQnumber = qqnumber
                    # if user.email != email:
                    #     user.email = email
                    #     token = token_confirm.generate_validate_token(phonenumber)
                    #     url = '/'.join(["http://sustechapp.com:4000",'user','activate',token])
                    #     url = u"<a href=\"%s\">点击链接</a>"%url
                    #     message = "\n".join([u'{0},欢迎注册使用SUSTechAPP'.format(username), u'请访问该链接，完成邮箱验证:', 
                    #         url])
                    #     res = sendmail(subject="SUSTech邮箱验证",text=message,receivers=[email])
                    # else:
                    #     res = True
                    user.save()
                    response.write("success")
        except Exception as e:
            raise e
            response.write("err")
    else:
        response.write("非法访问！")
    return response

def active_user(request,token):
    response = myResponse(request)
    try:
        phonenumber = token_confirm.confirm_validate_token(token)
    except:
        response.write('对不起，验证链接已经过期，请重新验证')
        return response
    try:
        user = User.objects.get(phonenumber=phonenumber)
    except User.DoesNotExist:
        response.write('对不起，您所验证的用户不存在，请重新注册')
        return response
    user.is_email_checked = True
    user.save()
    response.write('验证成功!')
    return response

# data:{location:input,username:justep.Shell.userName.get(),
# phonenumber:justep.Shell.phoneNumber.get(),longitude:me.xl,latitude:me.yl},
def putlocation(request):
    response = myResponse(request)
    if request.method == 'POST':
        phonenumber = request.POST.get("phonenumber")
        username = request.POST.get("username")

        location = request.POST.get("location")
        longitude = request.POST.get("longitude")
        latitude = request.POST.get("latitude")

        try:
            userResult = User.objects.filter(phonenumber=phonenumber)
            if len(userResult)==0:
                # username is phonenumber when registing
                response.write("notregiste")
            else:
                date = time.strftime('%m-%d|%H:%M',time.localtime())
                local = Location.objects.create(longitude=longitude,latitude=latitude,locationName=location,user=userResult[0],date=date)
                local.save()
                response.write("success")
        except Exception as e:
            raise e
            response.write("err")
    else:
        response.write("非法访问！")
    return response

# data:{username:justep.Shell.userName.get(),
# phonenumber:justep.Shell.phoneNumber.get(),password:justep.Shell.password.get()},
def getlocation(request):
    response = myResponse(request)
    if request.method == 'POST':
        phonenumber = request.POST.get("phonenumber")
        password = request.POST.get("password")
        longitude = request.POST.get("longitude")
        latitude = request.POST.get("latitude")
        try:
            userResult = User.objects.filter(phonenumber=phonenumber,password=password)
            if len(userResult)==0:
                # username is phonenumber when registing
                response.write("notregiste")
            else:
                user = userResult[0]
                info = UserInfo_updateEveryTenMin.objects.create(user=user)
                info.longitude = longitude
                info.latitude = latitude
                info.save()
        except Exception as e:
            response.write("err")
    else:
        response.write("非法访问！")
    return response


def test(request):
    res = {"sucess": False, "error": "  "}
    # response = HttpResponse()
    # response["Access-Control-Allow-Origin"] = request.META.get("HTTP_ORIGIN")
    # response["Access-Control-Allow-Credentials"] = "true"
    # if request.method == 'POST':
    #     print request.POST
    response = HttpResponse()
    response["Access-Control-Allow-Origin"] = request.META.get("HTTP_ORIGIN")
    response["Access-Control-Allow-Credentials"] = "true"
    response.write(json.dumps(res))
    return response
