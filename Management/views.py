# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from Market.models import *
from django.shortcuts import render
from Market.models import *
from Market.Useful_function import *
from Operations import *
# Create your views here.
import datetime


def isToday(Date):
    """
    @传入日期对象 返回是否是今天
    """
    return Date.strftime("%Y%m%d") == datetime.datetime.now().strftime("%Y%m%d")


@Check_If_Available(NEED_PWD=True, NEED_JWXT=True, RETURN_VALUE=True, AUTH_ADMIN=True)
def getTotalNums(request, user):
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

    AllSell = SellInfo.objects.all()
    result["sellinfo_total_num"] = len(AllSell)
    newItem = [item for item in AllSell if isToday(item.pub_change_date)]
    result["new_sell_today"] = len(newItem)

    AllSell = Activity_Wall.objects.all()
    result["activity_total_num"] = len(AllSell)
    newItem = [item for item in AllSell if isToday(item.pub_date)]
    result["new_activity_today"] = len(newItem)

    AllSell = Teacher_comment.objects.all()
    result["teacher_total_num"] = len(AllSell)
    newItem = [item for item in AllSell if isToday(item.pub_date)]
    result["new_teacher_today"] = len(newItem)

    AllSell = Blame_star.objects.all()
    result["star_total_num"] = len(AllSell)
    newItem = [item for item in AllSell if isToday(item.pub_date)]
    result["new_star_today"] = len(newItem)

    label = ["巴士时间", "教师信息", "讲座信息", "南科活动", "南科动态", "搜索图书", "借入图书"]
    value = np.zeros(len(label))
    for item in FunctionUsedTimes.objects.all():
        value += np.array(item.getInfoList(), dtype=int)
    result["open_total_num"] = {i: j for i, j in zip(label, value)}

    return result


@Check_If_Available(NEED_PWD=True, NEED_JWXT=True, RETURN_VALUE=True, AUTH_ADMIN=True)
def searchUserInfo(request, user):
    info = request.POST.get("info")
    user = User.objects.filter(phonenumber=info) or User.objects.filter(
        jwxt_usr=info) or User.objects.filter(QQnumber=info)
    if user:
        user = user[0]
        result = {}
        info = UserInfo.objects.get(user=user)
        result["QQ"] = user.QQnumber
        result["jwxt_usr"] = user.jwxt_usr
        result["jwxt_pwd"] = user.jwxt_pwd
        result["realname"] = user.realname
        result["img"] = getCompressed_ImageBase64(
            user.headImage, target=HeadImageHeight)
        result["username"] = user.username
        result["joinedactivity"] = len(JoinActivity.objects.filter(user=user))
        result["pubedactivity"] = len(Activity_Wall.objects.filter(user=user))
        result["dealed"] = len(
            [item for item in SellInfo.objects.filter(pub_user=user) if item.is_dealed])
        result["dealing"] = len(SellInfo.objects.filter(
            pub_user=user)) - result["dealed"]
        result["TotalGPA"] = info.TotalGPA
        result["TotalScore"] = info.TotalScore
        result["SUSTech_Class"] = info.SUSTech_Class
        return result
    else:
        return {}


@Check_If_Available(NEED_PWD=True, NEED_JWXT=True, RETURN_VALUE=True, AUTH_ADMIN=True)
def SystemOperate(request, user):
    operation = request.POST.get("OPERATION")
    if operation not in [item.__name__ for item in OPERATION_AVAILABLE]:
        return False
    else:
        params = request.POST.get("PARAMS")
        for item in OPERATION_AVAILABLE:
            if item.__name__ == operation:
                if params:
                    return item(params)
                else:
                    return item()


def myResponse(request, dictcontent=None):
    if dictcontent == None:
        response = HttpResponse()
    else:
        response = HttpResponse(json.dumps(dictcontent))
    response["Access-Control-Allow-Origin"] = request.META.get("HTTP_ORIGIN")
    response["Access-Control-Allow-Credentials"] = "true"
    return response
