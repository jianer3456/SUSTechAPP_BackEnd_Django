# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import cPickle as pickle
from threading import Timer, Thread
from Market.Useful_function import *
from django.http import HttpResponse
import time
from Market.models import *
from Config import *
from UpdateTeacherInfo import *
import sys
import functools
reload(sys)
sys.setdefaultencoding("utf-8")
from functools import wraps
from threading import Thread
import arrow

def getDeltaDays():
    initDay = arrow.Arrow(2017,9,8)
    now = arrow.now()
    delta = now-initDay
    return delta.days/7

def isToday(Date):
    """
    @传入日期对象 返回是否是今天
    """
    return Date.strftime("%Y%m%d") == datetime.now().strftime("%Y%m%d")


def async(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        Thread(target=f, args=args, kwargs=kwargs).start()
    return wrapper

# 传入字典  和 request


def myResponse(request, dictcontent=None):
    if dictcontent == None:
        response = HttpResponse()
    else:
        response = HttpResponse(json.dumps(dictcontent))
    response["Access-Control-Allow-Origin"] = request.META.get("HTTP_ORIGIN")
    response["Access-Control-Allow-Credentials"] = "true"
    return response


def Check_If_Available(*types, **kwtypes):
    """
    @NEED_PWD           是否需要验证用户
    @NEED_JWXT          是否需要验证教务系统
    @RETURN_VALUE       是否返回一个JSON串
    Tips:
            若不返回JSON,则需要返回操作是否成功
    """
    def _outer(func):
        @functools.wraps(func)
        def _inner(*args, **kwargs):
            request = args[0]
            response = myResponse(request)
            if request.method == 'POST':
                if kwtypes["NEED_PWD"]:
                    phonenumber = request.POST.get("phonenumber")
                    password = request.POST.get("password")
                    userResult = User.objects.filter(
                        phonenumber=phonenumber, password=password)
                    if len(userResult) == 0:
                        response.write(NO_USER)
                    else:
                        user = userResult[0]
                        if kwtypes["NEED_JWXT"]:
                            if user.is_jwxt_checked:
                                if kwtypes.get("AUTH_ADMIN"):
                                    if user.jwxt_usr not in ADMIN_JWXT:
                                        response.write(NOT_ALLOWED)
                                        return response
                                if kwtypes["RETURN_VALUE"]:
                                    result = func(request, user)
                                    if type(result) == type({}) or type(result) == type([]):
                                        response = myResponse(request, result)
                                    else:
                                        response.write(result)
                                else:
                                    func(request, user)
                                    response.write(OPERATION_SUCCESS)
                            else:
                                response.write(NOT_ALLOWED)
                        else:
                            if kwtypes["RETURN_VALUE"]:
                                result = func(request, user)
                                response = myResponse(request, result)
                            else:
                                if func(request, user):
                                    response.write(OPERATION_SUCCESS)
                                else:
                                    response.write(OPERATION_FAIL)
                else:
                    if kwtypes["RETURN_VALUE"]:
                        result = func(request)
                        response = myResponse(request, result)
                    else:
                        if func(request):
                            response.write(OPERATION_SUCCESS)
                        else:
                            response.write(OPERATION_FAIL)
            elif request.method == 'GET':
                # For Debug
                response.write(func(request, None))
            else:
                response.write("非法访问")
            return response
        return _inner
    return _outer


@async
def UpdatePicture(keyword):
    # 词语加入pickle
    # with open(EnglishWordspickle,"rb") as file:
    #     keywords = pickle.load(file)
    #     if not keyword in keywords:
    #         keywords.append(keyword)
    #         with open(EnglishWordspickle,"wb") as file:
    #             pickle.dump(dict(),file)
    #             pickle.dump(keywords,file)

    url_list = getPictureFromPexels(keyword)
    for item in url_list:
        MainPagePicture.objects.create(
            keyword=keyword, fSmallImg=item, fBigImg="")


# 每隔半天运行一次数据更新
def upDateInfo():
    time_str = str(datetime.strftime(datetime.now(), "%m月%d日 %H:%M"))
    # 主页新闻更新
    # global conf
    for item in SustcNewsInfo.objects.all():
        item.delete()

    news_Title = []
    for i, r in get_Sustc_Main_News().iteritems():
        try:
            news_info, created = SustcNewsInfo.objects.get_or_create(id=i)
            news_info.title = r["title"]
            # news_info.img_url =  r["img_url"]
            aaa = urllib.urlretrieve(r["img_url"], "cached_img.jpg")
            news_info.img_url = getCompressed_ImageBase64(
                aaa[0], target=QualityOfMainPic)
            news_info.newsUrl = r["news_url"]

            news_Title.append(r["title"])
            news_Title.append("=" * 10)
            if r["title"] == "" or r["img_url"] == "" or r["news_url"] == "":
                pass
            else:
                news_info.save()
        except Exception as e:
            pass

    text1 = "更新主页新闻信息成功" + "\n==========\n".join(news_Title)
    # AcademicForumInfo
    forum_title = []
    for i, item in enumerate(get_Sustc_Academic_Info()):
        forum_info, created = AcademicForumInfo.objects.get_or_create(id=i)
        forum_info.Apartment = item["Apartment"]
        forum_info.Detail_url = item["Detail_url"]
        forum_info.Title = item["Title"]
        forum_title.append(item["Title"])
        forum_info.Lecturer = item["Lecturer"]
        forum_info.Time = item["Time"]
        forum_info.Location = item["Location"]
        # 格式 07-31  找个地方PUSH一下
        forum_info.day = item["day"]
        forum_info.save()
    text2 = "更新讲座信息成功" + "\n==========\n".join(forum_title)

    # 数据统计操作
    # label = ["获取巴士时间", "获取教师信息", "获取讲座信息", "打开活动墙", "打开动态", "搜索图书", "借入图书"]
    # value = np.zeros(len(label))
    # for item in FunctionUsedTimes.objects.all():
    #     value += np.array(item.getInfoList(), dtype=int)
    # getStatisticsChart(chartType="bar", label=label,
    #    value=value, filename="%s-功能使用次数统计" % time_str)

    weaList = getTodayWeather()
    obj, created = TodayWeather.objects.get_or_create(id=0)
    obj.datetimeWea = weaList[0]
    obj.nighttimeWea = weaList[1]
    obj.save()
    TodayWeather.objects.create(
        datetimeWea=weaList[0], nighttimeWea=weaList[1])
    # 发送邮件

    result = {}
    users = User.objects.all()
    result["user_total_num"] = len(users)
    newUsers = [item for item in users if isToday(item.date_joined)]
    jwxt_users = [item for item in users if item.is_jwxt_checked]
    today_jwxt_users = [
        item for item in users if item.is_jwxt_checked and isToday(item.date_joined)]
    result["jwxt_total_num"] = len(jwxt_users)
    result["jwxt_today_num"] = len(today_jwxt_users)
    result["new_user_today"] = len(newUsers)

    Maininfo = "总用户:%d 今日新增数:%d 教务系统认证总数:%d 教务系统今日新增:%d" % (
        result["user_total_num"], result["new_user_today"], result["jwxt_total_num"], result["jwxt_today_num"])

    text = weaList[0] + "\n" + weaList[1] + "\n" + \
        text1 + text2 + "\n%s\n" % time_str + Maininfo
    res = sendmail(subject="服务器信息", text=text,
                   receivers=adminmail, kind="plain")

    time.sleep(43200)
    Thread(target=upDateInfo).start()


# 用户注册后异步执行数据更新
@async
def InitUser_AfterChecked(user):
    totalGPA, totalScores, GPA_List, compareList, TotalInfodict = getClassScores(
        user.jwxt_usr, user.jwxt_pwd)
    userinfo = UserInfo.objects.get_or_create(user=user)
    userinfo = userinfo[0]
    userinfo.TotalGPA = str(totalGPA)
    userinfo.TotalScore = str(totalScores)
    userinfo.SUSTech_Class = user.jwxt_usr[1:3] + user.jwxt_usr[4:6]
    userinfo.save()
    with open(GPApickle, "rb") as file:
        # with open('PickleInfo/GPAinfo/gpa.pickle',"r+b") as file:
        gpaInfo = pickle.load(file)
        if not gpaInfo.get(user.jwxt_usr):
            Info = {"EveryTermGPAandScore": GPA_List,
                    "BestWorst": compareList, "FullGPAInfo": TotalInfodict}
            gpaInfo[user.jwxt_usr] = Info
            with open(GPApickle, "wb") as f:
                pickle.dump(gpaInfo, f)
    namepickle = ClassTablePickle + user.jwxt_usr
    with open(namepickle, "wb") as f:
        i = {}
        pickle.dump(i, f)
    a = InitClassTable(user.jwxt_usr, user.jwxt_pwd, ClassTablePickle)
    a.run()
    # text = "\n".join(news_Title)
    # res = sendmail(subject="新用户获取-%s"%user.username,text=text,receivers=conf.get("AdminInfo",adminMail))
import arrow

# classnum convert
classnumConvert = {1:8,2:10,3:14,4:16,5:19,6:21,7:23}

def gogetNextClassInfo(user):
    if user.is_jwxt_checked:
        filename = ClassTablePickle+str(user.jwxt_usr)
        if os.path.exists(filename):
            with open(filename,"rb") as file:
                result = pickle.load(file)
                if result:
                    date = result["date"][0]
                    r = result["classtable"][date]
                    todayClass = False
                    for index,item in enumerate(r):
                        item["id"] = index
                        todayWeekday = arrow.now().weekday()
                        if todayWeekday==item['weekday']:
                            if classnumConvert[item["classnum"]]>=arrow.now().hour:
                                todayClass=item
                                hour = classnumConvert[item["classnum"]]
                                break
#  and getDeltaDays()%2
                    if "单" in item["weekinfo"] and getDeltaDays()%2!=1:
                        return "今天没有课"
                    if "双" in item["weekinfo"] and getDeltaDays()%2==1:
                        return "今天没有课"
                    if todayClass:
                        return item["classname"]+" "+item["location"]+" "+ str(hour)+"点"
                    else:
                        return "今天没有课"
                else:
                    return NEED_TIME
        else:
            # InitUser_AfterChecked(user)
            return NEED_TIME    
    else:
        return NOT_ALLOWED

from random import choice
def gogetAppMsg(user):
    max_len = 6

    joinedlist = JoinActivity.objects.filter(user=user)
    sellinfo = SellInfo.objects.filter(pub_user=user)
    activityInfo = Activity_Wall.objects.filter(user=user)
    pubblame = Blame_Wall.objects.filter(user=user)
    msgList = []
    l = len(joinedlist)
    if l>0:
        if l==1:
            msgList.append("参加活动\"%s...\""%joinedlist[0].activity.title[0:max_len])
        else:
            msgList.append("共参加了%i个活动"%l)
    l = len(sellinfo)
    if l>0:
        if l==1:
            msgList.append("发布\"%s\..."%sellinfo[0].goodsname[0:max_len])
        else:
            msgList.append("共发布了%i个售卖信息"%l)
    l = len(activityInfo)
    if l>0:
        if l==1:
            msgList.append("发布活动\"%s...\""%activityInfo[0].title[0:max_len])
        else:
            msgList.append("共发布了%i个活动"%l)
    l = len(pubblame)
    if l>0:
        if l==1:
            msgList.append("发表动态\"%s...\""%pubblame[0].content[0:max_len])
        else:
            msgList.append("共发表了%i个动态"%l)                 
    return choice(msgList)
