# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.db import models
import json
from Useful_function import getCompressed_ImageBase64, date_trans
from datetime import datetime, timedelta, date
# Create your models here.



def convertToJson(obj,imageQuality=75,dateHumanRead=True):
    result = {}
    field_names_list = obj._meta.fields
    for fieldName in field_names_list:
        try:
            fieldValue = getattr(obj, fieldName.name)  # 获取属性值
            if type(fieldValue) is date or type(fieldValue) is datetime:
                if dateHumanRead:
                    fieldValue = date_trans(fieldValue)
                else:
                    fieldValue = fieldValue.strftime('%Y-%m-%d %H:%M:%S')
            if type(fieldValue) == models.fields.files.ImageFieldFile:
                fieldValue = getCompressed_ImageBase64(fieldValue,target=imageQuality)
            result[fieldName.name] = str(fieldValue)
        except Exception, ex:
            print ex
    return result

class User(AbstractUser):
    phonenumber = models.CharField(max_length=20,default="")  
    QQnumber = models.CharField(max_length=20,default="")  
    description = models.TextField(max_length=256, default="",blank=True)  
    headImage = models.ImageField(upload_to='./media/image/users/headimage',default='media/image/users/defaultheadimage.jpg',null=True, blank=True)  
    score = models.IntegerField(default=0)
    realname = models.CharField(max_length=20,default="")  
    pushID = models.CharField(max_length=50,default="")  

    isInfoFilled = models.BooleanField(default=False)

    jwxt_usr = models.CharField(max_length=10,default="",blank=True)
    jwxt_pwd = models.CharField(max_length=20,default="",blank=True)
    is_email_checked = models.BooleanField(default=False)
    is_jwxt_checked = models.BooleanField(default=False)
    def __unicode__(self):
        return self.username
    def toJson(self,imageQuality=75,dateHumanRead=True):
        return convertToJson(self,imageQuality=200,dateHumanRead=True)
class UserInfo(models.Model):
    user = models.ForeignKey(User)
    TotalGPA = models.CharField(max_length=20,default="")  
    TotalScore = models.CharField(max_length=20,default="") 
    gpaInfo = models.CharField(max_length=100,default="") 

    Apartment = models.CharField(max_length=20,default="") 
    SUSTech_Class = models.CharField(max_length=20,default="") 
    def __unicode__(self):
        return self.user.realname
    def toJson(self,imageQuality=75,dateHumanRead=True):
        return convertToJson(self,imageQuality=200,dateHumanRead=True)
class UserInfo_updateEveryTenMin(models.Model):
    user = models.ForeignKey(User)
    longitude = models.CharField(max_length=20,default="")  
    latitude = models.CharField(max_length=20,default="")  
    pub_date = models.DateTimeField(auto_now=True)

class UserBooksInfo(models.Model):
    user = models.ForeignKey(User)
    lib_usr = models.CharField(max_length=20,default="")  
    lib_pwd = models.CharField(max_length=20,default="")  



class AcademicForumInfo(models.Model):
    Apartment = models.CharField(max_length=20,default="") 
    Title = models.CharField(max_length=20,default="") 
    Lecturer = models.CharField(max_length=20,default="") 
    Time = models.CharField(max_length=20,default="") 
    Location = models.CharField(max_length=20,default="") 
    day = models.CharField(max_length=20,default="") 
    Detail_url = models.CharField(max_length=50,default="") 
    def __unicode__(self):
        return self.Title
    def toJson(self,imageQuality=75,dateHumanRead=True):
        return convertToJson(self,imageQuality=200,dateHumanRead=True)
class UserJoinForumInfo(models.Model):
    user = models.ForeignKey(User)
    Title = models.CharField(max_length=20,default="") 
    Apartment = models.CharField(max_length=20,default="") 
    Detail_url = models.CharField(max_length=50,default="") 

class FunctionUsedTimes(models.Model):
    user = models.ForeignKey(User)
    getBusTime = models.IntegerField(default=0)
    getTeacherInfo = models.IntegerField(default=0)
    getForumInfo = models.IntegerField(default=0)
    open_Confession_Wall = models.IntegerField(default=0)
    open_Activity_Wall = models.IntegerField(default=0)
    open_Blame_Wall = models.IntegerField(default=0)
    open_MakeFriends_Wall = models.IntegerField(default=0)
    search_books = models.IntegerField(default=0)
    borrow_books = models.IntegerField(default=0)
    def getInfoList(self):
        return [self.getBusTime,self.getTeacherInfo,self.getForumInfo,self.open_Activity_Wall,self.open_Blame_Wall,self.search_books,self.borrow_books]

class Blame_star(models.Model):
    user = models.ForeignKey(User)
    blameID = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now=True)

class Blame_comment(models.Model):
    user = models.ForeignKey(User)
    blameID = models.IntegerField(default=0)
    content = models.CharField(max_length=100,default="") 
    pub_date = models.DateTimeField(auto_now=True)
    
class Blame_Wall(models.Model):
    user = models.ForeignKey(User)
    content = models.CharField(max_length=100,default="") 
    star = models.IntegerField(default=0)
    comment = models.IntegerField(default=0)
    label = models.CharField(max_length=20,default="") 
    pub_date = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.user.username
    def toJson(self,imageQuality=75,dateHumanRead=True):
        return convertToJson(self,imageQuality=200,dateHumanRead=True)
class Confession_Wall(models.Model):
    Con_user = models.ForeignKey(User)
    content = models.CharField(max_length=100,default="") 
    star = models.IntegerField(default=0)
    
class MakeFriends_Wall(models.Model):
    user = models.ForeignKey(User)
    content = models.CharField(max_length=100,default="") 
    star = models.IntegerField(default=0)

class Activity_Wall(models.Model):
    user = models.ForeignKey(User)
    # 2014-07-10 10:21:12
    title = models.CharField(max_length=50,default="") 
    startTime = models.CharField(max_length=100,default="") 
    endTime = models.CharField(max_length=100,default="") 
    limt_people = models.IntegerField(default=0)
    num_people = models.IntegerField(default=0)
    location = models.CharField(max_length=100,default="") 
    # 10:21
    duration  = models.CharField(max_length=100,default="") 
    content = models.CharField(max_length=100,default="") 
    star = models.IntegerField(default=0)
    is_show = models.BooleanField(default=True)
    pub_date = models.DateTimeField(auto_now=True)

class JoinActivity(models.Model):
    user = models.ForeignKey(User)
    activity = models.ForeignKey(Activity_Wall)
    pub_date = models.DateTimeField(auto_now=True)


class Teacher_Info(models.Model):
    name = models.CharField(max_length=10,default="")
    email = models.CharField(max_length=30,default="")
    phonenumber = models.CharField(max_length=30,default="")
    Apartment = models.CharField(max_length=20,default="") 
    description = models.CharField(max_length=100,default="") 
    achievement = models.CharField(max_length=100,default="") 
    num_achievement = models.IntegerField(default=0)
    star = models.IntegerField(default=0)
    detail_url = models.CharField(max_length=100,default="") 
    img_url = models.CharField(max_length=100,default="") 
    position = models.CharField(max_length=20,default="") 
    telephone = models.CharField(max_length=20,default="") 

class Teacher_comment(models.Model):
    user = models.ForeignKey(User)
    teacherID = models.IntegerField(default=0)
    content = models.CharField(max_length=100,default="") 
    pub_date = models.DateTimeField(auto_now=True)

class SustcNewsInfo(models.Model):
    # show_id = models.IntegerField(default=0)
    title = models.CharField(max_length=40,default="")  
    newsImage = models.ImageField(upload_to='./media/image/news/sustcimage',null=True, blank=True)
    img_url = models.CharField(max_length=100,default="")  
    newsUrl = models.CharField(max_length=100,default="")  


class Location(models.Model):
    longitude = models.CharField(max_length=20,default="")  
    latitude = models.CharField(max_length=20,default="")  
    locationName = models.CharField(max_length=20,default="")  
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now=True)
    app_location = models.CharField(max_length=20,default="")  
class SellInfo(models.Model):
    picture = models.ImageField(upload_to='./media/image/goods/sell',default='media/image/goods/defaultgoodsimage.jpg',null=True, blank=True)  
    goodsname = models.CharField(max_length=20,default="")  
    description = models.CharField(max_length=200,default="")  
    price = models.CharField(max_length=20,default="")  
    # is_adjustable = models.BooleanField(default=False)
    pub_user = models.ForeignKey(User)
    flag = models.IntegerField(default=0)
    
    is_dealed = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)
# datetime.datetime
#change to time we use: datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S")
    pub_change_date = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.goodsname
    def toJson(self,imageQuality=75,dateHumanRead=True):
        return convertToJson(self,imageQuality=200,dateHumanRead=True)

class Sell_comment(models.Model):
    user = models.ForeignKey(User)
    sellID = models.IntegerField(default=0)
    content = models.CharField(max_length=100,default="") 
    pub_date = models.DateTimeField(auto_now=True)


class MainPagePicture(models.Model):
    keyword = models.CharField(max_length=20,default="")  
    fSmallImg = models.CharField(max_length=200,default="")  
    fBigImg = models.CharField(max_length=200,default="")  
    pub_change_date = models.DateTimeField(auto_now=True)

class TodayWeather(models.Model):
    datetimeWea = models.CharField(max_length=200,default="")  
    nighttimeWea = models.CharField(max_length=200,default="")  
    pub_change_date = models.DateTimeField(auto_now=True)

class ClubActivity(models.Model):
    title = models.CharField(max_length=100,default="")  
    location = models.CharField(max_length=20,default="")  
    time = models.CharField(max_length=20,default="")  
    content = models.CharField(max_length=200,default="")  
    host = models.CharField(max_length=200,default="")  

class OfficialActivity(models.Model):
    title = models.CharField(max_length=100,default="")  
    location = models.CharField(max_length=20,default="")  
    time = models.CharField(max_length=20,default="")  
    content = models.CharField(max_length=200,default="")  
    host = models.CharField(max_length=200,default="")  
    def __unicode__(self):
        return self.title
    def toJson(self,imageQuality=75,dateHumanRead=True):
        return convertToJson(self,imageQuality=200,dateHumanRead=True)

class MainPageInfo(models.Model):
    name = models.CharField(max_length=100,default="")  
    url = models.CharField(max_length=1000,default="")  
    intro = models.CharField(max_length=100,default="")  
    color = models.CharField(max_length=100,default="")  
    pageurl = models.CharField(max_length=1000,default="")  
    pictureurl = models.CharField(max_length=1000,default="")  
    videourl = models.CharField(max_length=1000,default="")  
    changeDate = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.name
    def toJson(self,imageQuality=75,dateHumanRead=True):
        return convertToJson(self,imageQuality=200,dateHumanRead=True)
