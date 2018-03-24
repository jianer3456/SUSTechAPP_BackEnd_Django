# -*- coding: utf-8 -*-
from Market.AttachedModule import *
from Market.Useful_function import *
from Market.models import *
from Config import *
import time


def updateUser(user):
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
        if gpaInfo.get(user.jwxt_usr):
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


@async
def reset_jwxt_info(single_jwxt_usr=None):
    if single_jwxt_usr is None:
        for user in User.objects.all():
            if user.is_jwxt_checked:
                updateUser(user)
                time.sleep(30)
    else:
        try:
            updateUser(User.objects.get(jwxt_usr=single_jwxt_usr))
        except Exception as e:
            sendmail(subject="用户信息更新", text=e, receivers=[adminmail])
    if single_jwxt_usr:
        sendmail(subject="用户%s信息更新" % single_jwxt_usr,
                 text="success", receivers=[adminmail])
    else:
        sendmail(subject="全部用户信息更新完毕", text="success", receivers=[adminmail])


def push_notification_toall(content):
    try:
        jpushInfo(information=content)
    except Exception as e:
        return False
    else:
        return True


def deleteSellInfo(sellinfoId):
    try:
        SellInfo.objects.get(id=sellinfoId).delete()
    except Exception as e:
        return False
    else:
        return True


def deleteWallInfo(wallinfoId):
    try:
        Blame_Wall.objects.get(id=wallinfoId).delete()
    except Exception as e:
        return False
    else:
        return True


def deleteActivityInfo(activityId):
    try:
        Activity_Wall.objects.get(id=activityId).delete()
    except Exception as e:
        return False
    else:
        return True


def changeVersion(version):
    global APP_VERSION
    if version:
        APP_VERSION = version
        return True


def addAdmin(jwxt_usr):
    if jwxt_usr:
        ADMIN_JWXT.append(jwxt_usr)
        return True


def addAdminMail(mail):
    if mail:
        adminmail.append(mail)
        return True
    else:
        return False


def changeWenjuan(url):
    if url:
        Wenjuan_url = url
        return True


OPERATION_AVAILABLE = []
OPERATION_AVAILABLE.append(reset_jwxt_info)
OPERATION_AVAILABLE.append(push_notification_toall)
OPERATION_AVAILABLE.append(deleteWallInfo)
OPERATION_AVAILABLE.append(deleteActivityInfo)
OPERATION_AVAILABLE.append(deleteSellInfo)
OPERATION_AVAILABLE.append(changeVersion)
OPERATION_AVAILABLE.append(addAdmin)
OPERATION_AVAILABLE.append(addAdminMail)
OPERATION_AVAILABLE.append(changeWenjuan)
