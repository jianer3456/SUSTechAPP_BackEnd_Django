# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import sys
import re
import json
import cookielib
import urllib2
import urllib
import requests


class Login(object):
    """docstring for Login"""
    sucess = False
    user_name = ""
    jxzid = ""
    user_sid = ""
    usr = ""
    psw = ""
    XK_success_result = []
    XK_fail_result = []
    url_base = 'http://jwxt.sustc.edu.cn'
    login_url = u'https://cas.sustc.edu.cn/cas/login?service=http%3A%2F%2Fjwxt.sustc.edu.cn%2Fjsxsd%2F'

    def __init__(self, usr, psw):
        self.usr = usr
        self.pwd = psw
        self.Session = requests.Session()
        # self.cookies = cookielib.CookieJar()
        # self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))
        self._login()

    def getHtml(self, url):
        try:
            return self.Session.get(url).content
        except Exception as e:
            print "NetWork error!"

    def getCode(self):
        html = self.getHtml(self.login_url)
        soup = BeautifulSoup(html, 'html.parser')
        html_flit = soup.find_all('section')
        soup_flit = BeautifulSoup(str(html_flit), 'html.parser')
        lt = soup_flit.find_all('input')[2]['value']
        code = soup_flit.find_all('input')[3]['value']
        return lt, code

    def _login(self):
        url = "https://cas.sustc.edu.cn/cas/login?service=http%3A%2F%2Fjwxt.sustc.edu.cn%2Fjsxsd%2F"
        html = requests.get(url).content
        soup = BeautifulSoup(html, 'html.parser')
        html_flit = soup.find_all('section')
        soup_flit = BeautifulSoup(str(html_flit), 'html.parser')
        term = soup_flit.find_all('input')
        lt = term[2]['value']
        code = term[3]['value']
        postdata = {'username': self.usr, 'password': self.pwd, 'lt': lt,
                    'execution': lt, '_eventId': 'submit', 'submit': 'LOGIN'}
        headers = {"X-Requested-With": "XMLHttpRequest"}
        result = self.Session.post(
            url=url, data=postdata, headers=headers).content

        if "errors" not in result:
            nameInfo = self.getName(result)[0]
            self.user_name = nameInfo[0]
            self.user_sid = nameInfo[1]
            self.jxzid = self.getJxzid()
            self.sucess = True
        else:
            self.sucess = False

    def login(self):
        lt, code = self.getCode()
        postdata = {'username': self.usr, 'password': self.psw, 'lt': lt,
                    'execution': lt, '_eventId': 'submit', 'submit': 'LOGIN'}
        postdata = urllib.urlencode(postdata)
        request = urllib2.Request(url=self.login_url, data=postdata)
        i = 1
        while i <= 3:
            result = self.opener.open(request).read()
            if "errors" not in result:
                nameInfo = self.getName(result)[0]
                self.user_name = nameInfo[0]
                self.user_sid = nameInfo[1]
                self.jxzid = self.getJxzid()
                self.sucess = True
                return
            i += 1
        self.sucess = False

    def getJxzid(self):
        text = self.Session.get(
            "http://jwxt.sustc.edu.cn/jsxsd/xsxk/xklc_list?Ves632DSdyV=NEW_XSD_PYGL").content
        pattern = r"<a href=\".*jx0502zbid=(.*)\">进入选课</a>\s*</td>"

        try:
            return self.reToinfo(pattern, text)[0]
        except Exception as e:
            return "2A018810EA3C4DCFAD5A971752AD1A0D"

    def reToinfo(self, pattern, text):
        pattern = re.compile(pattern)
        item = re.findall(pattern, text)
        return item

    def getName(self, LoginHtml):
        pattern = r"<div class=\"block1text\">\s*(.*)\s*<br/>\s*(.*)\s*<br/>"
        return self.reToinfo(pattern, LoginHtml)

    def getRawClass_Info(self, xkURL):
        # url = "http://jwxt.sustc.edu.cn/jsxsd/xsxk/xsxk_index?jx0502zbid="+self.jxzid
        url = "http://jwxt.sustc.edu.cn/jsxsd/xsxk/xsxk_index?jx0502zbid=" + self.jxzid
        self.Session.get(url)
        # displayLength为传输多少课程数据。这里设置为1000，够大就行
        dataT = "sEcho=1&iColumns=10&sColumns=&iDisplayStart=0&iDisplayLength=1000&mDataProp_0=kch&mDataProp_1=kcmc&mDataProp_2=xf&mDataProp_3=skls&mDataProp_4=sksj&mDataProp_5=skdd&mDataProp_6=xkrs&mDataProp_7=syrs&mDataProp_8=ctsm&mDataProp_9=czOper"
        request = urllib2.Request(url=xkURL, data=dataT)
        result = self.Session.get(request).read()
        return json.loads(result)

    def get_ClassTableFile(self, name=None, date="2016-2017-2"):
        if name == None:
            name = self.user_name
        print_url = self.url_base + '/jsxsd/xskb/xskb_print.do?xnxq01id=%s&zc=' % date
        data = self.getHtml(print_url)
        if data == None:
            print "获取课程表文件时发生错误"
            return
        name = "课程表|" + name
        with open('%s.xls' % name, 'wb') as file:
            file.write(data)
            file.close()

    def chooseCla(self, CO):

        id = CO.xkID
        url1 = "http://jwxt.sustc.edu.cn/jsxsd/xsxkkc/knjxkOper?jx0404id=%s&xkzy=&trjf=" % id
        url2 = "http://jwxt.sustc.edu.cn/jsxsd/xsxkkc/fawxkOper?jx0404id=%s&xkzy=&trjf=" % id
        url3 = "http://jwxt.sustc.edu.cn/jsxsd/xsxkkc/ggxxkxkOper?jx0404id=%s&xkzy=&trjf=" % id
        url4 = "http://jwxt.sustc.edu.cn/jsxsd/xsxkkc/xxxkOper?jx0404id=%s" % id
        url = "http://jwxt.sustc.edu.cn/jsxsd/xsxk/xsxk_index?jx0502zbid=" + self.jxzid
        self.Session.get(url)
        urllist = []
        urllist.append(url1)
        urllist.append(url2)
        urllist.append(url3)
        urllist.append(url4)
        result = []
        for i in urllist:
            result.append(self.getHtml(i))
        print "返回信息："
        for i in result:
            print i

    def chooseByClassObject(self, ClassObject):
        if not self.sucess:
            # print "未登录不能选课！"
            return "未登录不能选课！"
        id = ClassObject.xkID
        url1 = "http://jwxt.sustc.edu.cn/jsxsd/xsxkkc/knjxkOper?jx0404id=%s&xkzy=&trjf=" % id
        url2 = "http://jwxt.sustc.edu.cn/jsxsd/xsxkkc/fawxkOper?jx0404id=%s&xkzy=&trjf=" % id
        url3 = "http://jwxt.sustc.edu.cn/jsxsd/xsxkkc/ggxxkxkOper?jx0404id=%s&xkzy=&trjf=" % id
        url4 = "http://jwxt.sustc.edu.cn/jsxsd/xsxkkc/xxxkOper?jx0404id=%s" % id
        url = "http://jwxt.sustc.edu.cn/jsxsd/xsxk/xsxk_index?jx0502zbid=" + self.jxzid
        self.Session.get(url)
        CLasstype = ClassObject.Class_Type
        if CLasstype == None or CLasstype == "MR":
            urllist = []
            urllist.append(url1)
            urllist.append(url2)
            urllist.append(url3)
            urllist.append(url4)
            result = []
            for i in urllist:
                result.append(self.getHtml(i))
            return
            # result2= self.getHtml(old_str)
        Type_UrlDict = {}
        Type_UrlDict["JHXK"] = url4
        Type_UrlDict["KZYXK"] = url2
        Type_UrlDict["KNJXK"] = url1
        Type_UrlDict["GXK"] = url3
        for i, j in Type_UrlDict.iteritems():
            if CLasstype == i:
                result = self.getHtml(j)
                try:
                    result = json.loads(result)
                    if result.get("success") == True:
                        self.XK_success_result.append(
                            ClassObject.Class_name + ":" + result.get("message"))
                    else:
                        self.XK_fail_result.append(
                            ClassObject.Class_name + ":" + result.get("message"))
                except Exception as e:
                    raise e
        # if CLasstype=="JHXK":
        #     self.getHtml(url4)
        #     return
        # if CLasstype=="KZYXK":
        #     self.getHtml(url2)
        #     return
        # if CLasstype=="KNJXK":
        #     self.getHtml(url1)
        #     return
        # if CLasstype=="GXK":
        #     self.getHtml(url3)
        #     return

    def getXKlinkByClassObject(self, ClassObject):
        if not self.sucess:
            # print "未登录不能选课！"
            return None
        id = ClassObject.xkID
        CLasstype = ClassObject.Class_Type
        if CLasstype == "JHXK":
            url4 = "http://jwxt.sustc.edu.cn/jsxsd/xsxkkc/xxxkOper?jx0404id=%s" % id
            return url4
        if CLasstype == "KZYXK":
            url2 = "http://jwxt.sustc.edu.cn/jsxsd/xsxkkc/fawxkOper?jx0404id=%s&xkzy=&trjf=" % id
            return url2
        if CLasstype == "KNJXK":
            url1 = "http://jwxt.sustc.edu.cn/jsxsd/xsxkkc/knjxkOper?jx0404id=%s&xkzy=&trjf=" % id
            return url1
        if CLasstype == "GXK":
            url3 = "http://jwxt.sustc.edu.cn/jsxsd/xsxkkc/ggxxkxkOper?jx0404id=%s&xkzy=&trjf=" % id
            return url3

    def choose_class(self, id, name="该课程"):
        if not self.sucess:
            # print "未登录不能选课！"
            return "未登录不能选课！"
        # self.getHtml('http://jwxt.sustc.edu.cn/jsxsd/xsxk/xsxk_index?jx0502zbid="+self.jxzid
        url1 = "http://jwxt.sustc.edu.cn/jsxsd/xsxkkc/knjxkOper?jx0404id=%s&xkzy=&trjf=" % id
        url2 = "http://jwxt.sustc.edu.cn/jsxsd/xsxkkc/fawxkOper?jx0404id=%s&xkzy=&trjf=" % id
        url3 = "http://jwxt.sustc.edu.cn/jsxsd/xsxkkc/ggxxkxkOper?jx0404id=%s&xkzy=&trjf=" % id
        url4 = "http://jwxt.sustc.edu.cn/jsxsd/xsxkkc/xxxkOper?jx0404id=%s" % id
        url = "http://jwxt.sustc.edu.cn/jsxsd/xsxk/xsxk_index?jx0502zbid=" + self.jxzid
        self.Session.get(url)
        urllist = []
        urllist.append(url1)
        urllist.append(url2)
        urllist.append(url3)
        urllist.append(url4)
        result = []
        for i in urllist:
            result.append(self.getHtml(i))
        print name + "返回信息："
        for i in result:
            print i
        # result2= self.getHtml(old_str)
