# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import urllib2,sys
sys.path.append("../..")
from Market.models import Teacher_Info
# import urllib,urllib2,re,json
from bs4 import BeautifulSoup
def update_TeacherInfo():
    soup = BeautifulSoup(urllib2.urlopen("http://sustc.edu.cn/faculty_all").read(),"html.parser")
    for i,item in enumerate(soup.find_all(class_="block")):
        teacher_info,created = Teacher_Info.objects.get_or_create(id=i)
        info1 = [i for i in item.find(class_="typ").text.replace("\t","").replace("\r","").split("\n") if i!=""]   #第一个是职位 第二个是系
        teacher_info.position = info1[0]
        try:
            teacher_info.Apartment = info1[1]
        except Exception as e:
            teacher_info.Apartment = "无信息"
        info2 = [i for i in item.find(class_="oth").text.replace("\t","").replace("\r","").split("\n") if i!=""]   #电话  邮箱   长度为1且@ in 是邮箱
        if len(info2)==1:
            teacher_info.email = info2[0]
            teacher_info.telephone = "无信息"
        elif len(info2) == 2 and "@" in info2[1]:
            teacher_info.telephone = info2[0]
            teacher_info.email = info2[1]
        teacher_info.name = item.find(class_="img").a["title"]
        teacher_info.detail_url = "http://sustc.edu.cn" + item.find(class_="img").a["href"]
        teacher_info.img_url = "http://sustc.edu.cn" + item.find(class_="img").a.img["src"]
        teacher_info.save()
