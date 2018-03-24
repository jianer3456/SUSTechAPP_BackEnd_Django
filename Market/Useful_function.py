# coding=utf-8
import smtplib
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header
from django.conf import settings as django_settings
from itsdangerous import URLSafeTimedSerializer as utsr
from datetime import timedelta
import base64
import cPickle as pickle
import os
import xlrd
from datetime import datetime
import time
from Config import *
from cStringIO import StringIO
from PIL import Image
import jpush
import urllib
import re
import json
try:
    import urllib2
except ImportError:
    pass
import requests
import json
from bs4 import BeautifulSoup
import plotly
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
plotly.tools.set_credentials_file(
    username=Plotly_username, api_key=Plotly_APIKey)


def dateTransForActivity(time_str):
    # 把yyyy年MM月dd日hh时mm分ss秒
    # 转换成  %Y-%m-%d %H:%M:%S
    format = time_str.replace("年", "-").replace("月", "-").replace(
        "日", " ").replace("时", ":").replace("分", ":").replace("秒", "")
    return format


def dateTransForActivityTofront(time_str):
    time_format = time.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    return date_trans(datetime.fromtimestamp(time.mktime(time_format)))


def getTodayWeather(citycode="101280601"):
    url = "http://www.weather.com.cn/weather1d/%s.shtml" % citycode
    req = urllib2.Request(url)
    req.add_header(
        'User-Agent', 'Mozilla/5.0 (Android 5.1.1; Mobile; rv:42.0) Gecko/42.0 Firefox/42.0')
    text = urllib2.urlopen(req).read()
    soup = BeautifulSoup(text, "html.parser")
    result_list = soup.find_all("div", class_="t")[0]
    result = []
    for i in range(2):
        head = result_list.find_all("h1")[i].get_text()
        wea = result_list.find_all("p", class_="wea")[i]["title"]
        tem = result_list.find_all("p", class_="tem")[i].get_text().strip()
        r = " ".join([head, wea, tem])
        result.append(r)
    return result


def getPictureFromPexels(keyword=" "):
    def doJob(word):
        searchurl = 'https://www.pexels.com/search/' + str(word) + '/'
        text = requests.get(searchurl).text.encode('utf-8')
        soup = BeautifulSoup(text, "html.parser")
        result_list = soup.find_all("img")
        result = []
        for i in result_list:
            try:
                if "images.pexels.com" in i["src"]:
                    result.append(i["src"])
            except Exception as e:
                pass
        return result

    if type(keyword) == type(str()):
        return doJob(keyword)
    else:
        result = []
        for word in keyword:
            result += doJob(word)
        return result


def findBooks(bookname, num=20):
    """
    搜索图书
    @搜索的图书名称
    """
    base_url = "http://110.65.147.72/NTRdrBookRetr.aspx?"
    data = {"strType": "text", "strKeyValue": bookname,
            "strSortType": "", "strpageNum": num, "strSort": "desc"}
    params = urllib.urlencode(data)
    text = urllib2.urlopen(base_url + params).read()
    soup = BeautifulSoup(text, "html.parser")

    result = []

    info1 = soup.find_all("div", class_="into")
    info2 = soup.find_all("div", class_="titbar")
    num = num if num < len(info1) else len(info1)
    for i in xrange(num):
        r = {}
        titleInfo = info1[i].find_all("h3")[0].find_all("a")[0]
        r["detail_url"] = base_url + titleInfo["href"]
        r["title"] = titleInfo.get_text().strip()

        bodyInfo = info2[i]
        r["author"] = bodyInfo.find_all("span", class_="author")[
            0].get_text().split("：")[1]
        num = bodyInfo.find_all("span", class_="dates")[
            2].get_text().split("：")[1]
        if "online" in num:
            r["getbookNum"] = "No Resource"
        else:
            r["getbookNum"] = num
        result.append(r)
    return result


def LoginToLibTest(username, pwd):
    url = "http://lib.sustc.edu.cn/loginto.html"
    data = {"type": 2, "username": username, "pwd": pwd}
    headers = {"X-Requested-With": "XMLHttpRequest"}
    libSession = requests.Session()
    result = json.loads(libSession.post(url=url, data=data,
                                        headers=headers).content.decode())
    if result["error"] == 0:
        return True
    else:
        return False


def loginToLibAndAutoBorrow(username, pwd):
    """
    自动登录到图书馆系统
    获取借书信息  并自动续借返回续借结果
    """
    url = "http://lib.sustc.edu.cn/loginto.html"
    data = {"type": 2, "username": username, "pwd": pwd}
    headers = {"X-Requested-With": "XMLHttpRequest"}
    libSession = requests.Session()
    result = json.loads(libSession.post(url=url, data=data,
                                        headers=headers).content.decode())
    if result["error"] == 0:
        text = libSession.get(
            "http://lib.sustc.edu.cn/member/borrow.html").content
        soup = BeautifulSoup(text, "html.parser")
        # soup.find_all("td",class_="Desktop")
        main_text_list = soup.find_all("tbody")[0].find_all("tr")
        result = []
        borrow_url = "http://lib.sustc.edu.cn/member/renewBook.html"
        for item in main_text_list:
            r = {}
            if len(item.find("td", class_="desktop")) == 0:
                continue
            r["barcode"] = item.find("td", class_="desktop").get_text()
            r["bookname"] = item.find("td", class_="left").get_text()
            r["dateborrow"] = item.find("td", class_="desktop ws").get_text()
            r["dategiveback"] = item.find_all("td", class_="ws")[1].get_text()
            r["serialNumber"] = item.find("td", class_="desktop").get_text()
            r["automsg"] = json.loads(libSession.post(url=borrow_url, data={
                                      "barno": r["barcode"]}, headers=headers).content)["msg"]
            result.append(r)
        return result
    elif result["error"] == 6:
        return False
    else:
        return False


def getStatisticsChart(label, value, filename="默认图表", chartType="bar"):
    """
    chartType can be 'pie',饼状图 'bar',柱状图 'line',折线图 'scatter' 点状图
    filename文件名称，存在plotly上
    """
    if(len(label) != len(value)):
        return False
    if chartType == 'bar':
        trace = go.Bar(x=label, y=value)
    elif chartType == 'pie':
        trace = go.Pie(labels=label, values=value,
                       hoverinfo='label+percent', textinfo='label+value',
                       hole='.4',
                       textfont={'family': "Arial", 'size': 16})
    elif chartType == 'line':
        trace = go.Scatter(x=label, y=value, mode="lines+markers")
    elif chartType == 'scatter':
        trace = go.Scatter(x=label, y=value, mode='markers',
                           marker={'size': 10})
    else:
        return False
    data = [trace]
    py.plot(data, filename=filename)
    return True


# 判断是否是工作日
def weekdayOrWeekend(strtime=None):

    if strtime is None:
        info = datetime.now().weekday()
        if info == 6 or info == 5:
            return 'weekend'
        else:
            return 'weekday'
    else:
        today = datetime.strptime(strtime, '%Y-%m-%d %H:%M:%S')
        if today.isoweekday() == 6 or today.isoweekday() == 7:
            return 'weekend'
        else:
            return 'weekday'


def timeDifference(now, bustime):
    """
    标准时间,巴士时间 8:10
    返回相差时间的分钟数
    """
    now = datetime.strptime(now.split(" ")[1], '%H:%M:%S')
    bustime = datetime.strptime(bustime, '%H:%M')
    if(now < bustime):
        return ((bustime - now).seconds / 60)
    else:
        # 这是与上一班车相差的时间
        return 10000


def getLocationnameFromGPS(longitude, latitude, limit=None):
    """
    @经度  纬度
    返回地点名称 --- lyhill荔园车站  library图书馆车站
    """
    if limit == "bus":
        info = stationLocationpickle
    else:
        info = Locationpickle
    with open(info, "rb") as file:
        info = pickle.load(file)
        mindist = 0.0
        minloc = ""
        lastdist = 1000000.0
        for locationname, gpslist in info.iteritems():
            mindist = pow(pow(gpslist[0] - float(longitude), 2) +
                          pow(gpslist[1] - float(latitude), 2), 0.5)
            if mindist < lastdist:
                lastdist = mindist
                minloc = locationname
    return minloc


# 传入 标准格式的时间字符串  和delta时间
# 传出 结束时间
def getEndTime(str, last_time='1:00'):  # 默认1小时
    hour = int(last_time.split(":")[0])
    minute = int(last_time.split(":")[1])
    last = timedelta(hours=hour, minutes=minute)  # 持续时间
    startTime = datetime.strptime(str, '%Y-%m-%d %H:%M:%S')  # 开始时间
    endTime = startTime + last  # 结束时间
    return endTime

# 讲座时间 转换成标准 字符串


def getLectureDatetime(str):
    # str = str.split("：")[1]
    split1 = str.split('月')
    split2 = split1[1].split('日')
    split3 = split2[1].split(':')
    year = int(time.strftime('%Y'))
    month = int(split1[0])
    day = int(split2[0])
    hour = int(split3[0])
    minute = int(split3[1])
    dt = datetime(year, month, day, hour, minute)
    return dt


def checkJWXT(username, password):
    url = "http://gpa.sustc.edu.cn/queryscorebyitem"
    data = {"username": str(username), "password": str(password)}
    data = urllib.urlencode(data)
    request = urllib2.Request(url=url, data=data)
    try:
        result = urllib2.urlopen(request).read()
    except Exception as e:
        return False
    querydict = json.loads(result)
    if querydict.get("status") == 1000:
        return True


def getClassScores(username, password):
    url = "http://gpa.sustc.edu.cn/queryscorebyitem"
    data = {"username": str(username), "password": str(password)}
    data = urllib.urlencode(data)
    request = urllib2.Request(url=url, data=data)
    try:
        result = urllib2.urlopen(request).read()
    except Exception as e:
        return False
    querydict = json.loads(result)
    if querydict.get("status") == 1000:
        # for i in querydict["data"]:
        gpalist = []
        allgpa = 0
        zxf = 0
        compareGPAlist = []
        zxq = 0
        for i in range(0, len(querydict["data"]["ed"])):
            data = querydict["data"]["ed"][i]["data"]
            result = getGPA(data, compareGPAlist)
            if(result[0] != 0):
                zxq = zxq + 1
            allgpa += result[0]
            zxf += result[1]
            gpalist.append(result)
        NewcompareList = bubble(compareGPAlist)
        GPAl = len(NewcompareList)
        try:
            return allgpa / zxq, zxf, gpalist, [NewcompareList[0], NewcompareList[1], NewcompareList[2], NewcompareList[GPAl - 1], NewcompareList[GPAl - 2], NewcompareList[GPAl - 3]], querydict
        except:
            return 0, 0, [], [0, 0, 0, 0, 0, 0], querydict


def bubble(list):
    for index in range(len(list) - 1, 0, -1):
        for two_index in range(index):
            if list[two_index][0] > list[two_index + 1][0]:
                list[two_index], list[two_index +
                                      1] = list[two_index + 1], list[two_index]
    return list


def getGPA(data, gpabjlist):
    sumgpa = 0
    sumscore = 0
    extrascore = 0
    sumxf = 0
    for i in data:
        if (i["credit"].isdigit()):
            xf = float(i["credit"])
        else:
            xf = 0
        if(i["score"].isdigit()):
            cj = float(i["score"])
        else:
            cj = 0
            extrascore += xf

        if(cj >= 60):
            sumxf += xf
            gpa = calGPAPoint(cj)
            gpabjlist.append([gpa, i["coursename"]])
            sumgpa += xf * gpa
            sumscore += xf * cj
    if (sumxf != 0):
        lastgpa = sumgpa / sumxf
        sumxf += extrascore
        return (lastgpa, sumxf)
    else:
        return (0, 0)


def calGPAPoint(score):
    score = float(score)
    if (score >= 97):
        return 4.00
    if (score >= 93):
        return 3.94
    if (score >= 90):
        return 3.85
    if (score >= 87):
        return 3.73
    if (score >= 83):
        return 3.55
    if (score >= 80):
        return 3.32
    if (score >= 77):
        return 3.09
    if (score >= 73):
        return 2.78
    if (score >= 70):
        return 2.42
    if (score >= 67):
        return 2.08
    if (score >= 63):
        return 1.63
    if (score >= 60):
        return 1.15
    if (score >= 0):
        return 0
    else:
        return 0


def jpushInfo(information, users=None, tags=None):
    """
    @ tags :student   notcheckedstudent   notresign
    """
    _jpush = jpush.JPush(app_key, master_secret)
    push = _jpush.create_push()
    if users is None and tags is None:
        push.audience = jpush.all_
    elif type(users) == type(list()):
        alias1 = {"alias": users}
        push.audience = jpush.audience(
            alias1
        )
    elif type(users) == type(str()):
        alias1 = {"alias": [users]}
        push.audience = jpush.audience(
            alias1
        )
    elif tags:
        push.audience = jpush.audience(tag(tags))
    push.notification = jpush.notification(alert=information)
    push.platform = jpush.all_
    try:
        response = push.send()
    except Exception as e:
        return False
    else:
        return True


import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def get_Sustc_Academic_Info(num=2):

    result = []
    for i in range(num):
        i += 1
        soup = BeautifulSoup(urllib2.urlopen(
            "http://sustc.edu.cn/news_events_jiangzuo/p/%s" % i).read(), "html.parser")
        for item in soup.find_all(class_="clearfix block"):
            r = {}
            r["day"] = item.find_all(class_="day")[0].get_text()
            r["Apartment"] = item.find_all(class_="t0")[0].get_text()
            r["Title"] = item.find_all(class_="t1")[0].a["title"]
            r["Detail_url"] = "http://sustc.edu.cn" + \
                item.find_all(class_="t1")[0].a["href"]
            try:
                r["Lecturer"] = item.find_all(
                    class_="t2")[0].get_text().split("：")[1]
            except Exception as e:
                r["Lecturer"] = "神秘嘉宾"
            r["Time"] = item.find_all(class_="t3")[0].get_text().split("：")[1]
            r["Location"] = item.find_all(
                class_="t4")[0].get_text().split("：")[1]
            result.append(r)
    return result


def get_Sustc_Main_News(num=8):
    """
        urllib.urlretrieve()
        news_url
        title
        img_url
    """
    soup = BeautifulSoup(urllib2.urlopen(
        "http://sustc.edu.cn/").read(), "html.parser")
    info_list = soup.find_all(id="feature_images")[0].find_all("li")[0:num]
    result = {}
    for index, info in enumerate(info_list):
        r = {}
        r["img_url"] = "http://sustc.edu.cn" + \
            re.findall(r"/upload/.*?/.*? ", info["style"])[0][0:-2]
        r["news_url"] = info.a["href"]
        r["title"] = info.a["title"]
        result[index] = r
    return result


def pictureDeal(imgpath):
    try:
        sImg = Image.open(imgpath)
    except Exception as e:
        return ""
    w, h = sImg.size
    k = 1.0 * w / h
    targeth = 450
    if h > targeth:
        dImg = sImg.resize((int(k * targeth), targeth), Image.ANTIALIAS)
        buffer = StringIO()
        dImg.save(buffer, format="JPEG")
        ls_f = base64.b64encode(buffer.getvalue())
    else:
        with open(str(imgpath), 'rb') as f:
            ls_f = base64.b64encode(f.read())
    return "data:image/jpeg;base64," + ls_f
# 传入图片路径   传出压缩后的图片base64


def getCompressed_ImageBase64(imgpath, target=150):
    try:
        sImg = Image.open(imgpath)
    except Exception as e:
        return ""
    w, h = sImg.size
    k = 1.0 * w / h
    targeth = target
    if h > targeth:
        dImg = sImg.resize((int(k * targeth), targeth), Image.ANTIALIAS)
        buffer = StringIO()
        try:
            dImg.save(buffer, format="JPEG")
        except Exception as e:
            dImg.save(buffer, format="GIF")
        ls_f = base64.b64encode(buffer.getvalue())
    else:
        with open(str(imgpath), 'rb') as f:
            ls_f = base64.b64encode(f.read())
    return "data:image/jpeg;base64," + ls_f


class Token:
    def __init__(self, security_key):
        self.security_key = security_key
        self.salt = base64.encodestring(security_key)

    def generate_validate_token(self, username):
        serializer = utsr(self.security_key)
        return serializer.dumps(username, self.salt)

    def confirm_validate_token(self, token, expiration=3600):
        serializer = utsr(self.security_key)
        return serializer.loads(token, salt=self.salt, max_age=expiration)

    def remove_validate_token(self, token):
        serializer = utsr(self.security_key)
        return serializer.loads(token, salt=self.salt)


def sendmail(subject, text, receivers, kind="html"):
    # 第三方 SMTP 服务
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user = "mobile_app@sustechapp.com"  # 用户名
    mail_pass = "clpxxtavbmisbbdj"  # 口令
    sender = mail_user
    receivers = receivers  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
# name = "NOTE.txt"
# with open(name,"rb") as file:
#     text = file.read().decode("GB2312").encode("utf-8")
# print chardet.detect(text)
# print text
    message = MIMEText(text, kind, 'utf-8')
    message['From'] = Header("SUSTechAPP", 'utf-8')
    message['To'] = Header("用户", 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = SMTP_SSL(mail_host)
        smtpObj.ehlo()
        # smtpObj.starttls()
        # smtpObj.ehlo()
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        # print "发给"+str(receivers)+"邮件发送成功"
        return True
    except Exception as e:
        # raise e
        return False


def date_trans(date):
    delta = timedelta(days=1)
    _str = ""
    if datetime.today().strftime("%Y") == date.strftime("%Y"):

        if datetime.today().strftime("%Y-%m-%d") == date.strftime("%Y-%m-%d"):
            _str = "今天"
        elif (datetime.today() - delta).strftime("%Y-%m-%d") == date.strftime("%Y-%m-%d"):
            _str = "昨天"
        else:
            _str = date.strftime("%m月%d日 ")
    else:
        _str = date.strftime("%Y年%m月%d日 ")
    return _str + date.strftime("%H:%M")


class InitClassTable():
    def __init__(self, usr, pwd, pickle_base_path):
        self.usr = str(usr)
        self.pwd = str(pwd)
        self.pickle_path = pickle_base_path + usr
        self.Session = requests.Session()
        self.file_name = "cached_ClassTable_%s.xls" % self.usr
        self.raw_datelist = []
        self.table = None
        self.result = {}
        self._login()
        self._getDate()

    def run(self):
        self._analysis()
        with open(self.pickle_path, "wb") as file:
            pickle.dump(self.result, file)
        os.remove(self.file_name)

    def _login(self):
        url = "https://cas.sustc.edu.cn/cas/login?service=http%3A%2F%2Fjwxt.sustc.edu.cn%2Fjsxsd%2F"
        html = requests.get(url).content
        soup = BeautifulSoup(html, 'html.parser')
        html_flit = soup.find_all('section')
        soup_flit = BeautifulSoup(str(html_flit), 'html.parser')
        term = soup_flit.find_all('input')
        lt = term[2]['value']
        # code = term[3]['value']
        postdata = {'username': self.usr, 'password': self.pwd, 'lt': lt,
                    'execution': lt, '_eventId': 'submit', 'submit': 'LOGIN'}
        headers = {"X-Requested-With": "XMLHttpRequest"}
        self.Session.post(url=url, data=postdata, headers=headers)

    def _getClassTableFileByDate(self, date):
        print_url = 'http://jwxt.sustc.edu.cn/jsxsd/xskb/xskb_print.do?xnxq01id=%s&zc=' % date
        data = self.Session.get(print_url).content
        with open(self.file_name, 'wb') as file:
            file.write(data)

    def _getDate(self):
        date_url = "http://jwxt.sustc.edu.cn/jsxsd/xskb/xskb_list.do"
        soup = BeautifulSoup(self.Session.get(date_url).content, 'html.parser')
        a = soup.find_all('select', id="xnxq01id")[0].find_all("option")
        for i in a:
            self.raw_datelist.append(i.get_text())

    def _isValidTable(self):
        wb = xlrd.open_workbook(self.file_name)
        self.table = wb.sheets()[0]
        try:
            self.table.cell(4, 1).value
        except Exception as e:
            return False
        else:
            return True

    def _analysis(self):
        valid_datelist = []
        classtable = {}
        for date in self.raw_datelist:
            self._getClassTableFileByDate(date)
            if self._isValidTable() and self.table:
                classtable[date] = []
                for i in xrange(1, 8):
                    for j in xrange(3, 9):
                        classinfo = {}
                        info = self.table.cell(j, i).value
                        if info != " " and info != "":
                            infolist = info.split("\n")
                            # 星期几 与arrow一直  arrow.now().weekday()
                            classinfo["weekday"] = i - 1
                            # 第几大节
                            classinfo["classnum"] = j - 2
                            classinfo['classname'] = infolist[1]
                            classinfo["teacher"] = infolist[2].split("(")[0]
                            classinfo["weekinfo"] = infolist[3]
                            classinfo["location"] = infolist[4]
                            classtable[date].append(classinfo)
                if len(classtable[date]) > 0:
                    valid_datelist.append(date)
        self.result["date"] = valid_datelist
        self.result["classtable"] = classtable

