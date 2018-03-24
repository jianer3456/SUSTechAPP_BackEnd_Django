# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from Market.models import *
from django.contrib import admin

# Register your models here.
class Blame_starAdmin(admin.ModelAdmin):
    list_display = ('user', "blameID")


class Blame_WallAdmin(admin.ModelAdmin):
    list_display = ('user', "content", "star", "comment")


class Blame_CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'blameID', 'content', 'pub_date')

class Activity_WallAdmin(admin.ModelAdmin):
    list_display = ('user', 'startTime', 'duration', 'content', 'star')


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'jwxt_usr', 'QQnumber',
                    'phonenumber', 'email', 'score')


class LocalAdmin(admin.ModelAdmin):
    list_display = ('locationName', 'user', 'date','longitude','latitude')


class SellInfoAdmin(admin.ModelAdmin):
    list_display = ('goodsname', 'price', 'description',
                    'pub_user', 'is_dealed', 'pub_change_date')


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'TotalGPA', 'TotalScore', 'SUSTech_Class')


class LibInfoUser(admin.ModelAdmin):
    list_display = ('user', 'lib_usr', 'lib_pwd')


class ForumInfoAdmin(admin.ModelAdmin):
    list_display = ('Apartment', 'Title', 'Lecturer',
                    'Time', 'Location', 'day', 'Detail_url')


class FunctionTimesAdmin(admin.ModelAdmin):
    list_display = ('user', 'getBusTime', 'getTeacherInfo', 'getForumInfo', 'open_Confession_Wall',
                    'open_Activity_Wall', 'open_Blame_Wall', 'open_MakeFriends_Wall', 'search_books', 'borrow_books')


class Teacher_InfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'Apartment', 'img_url')


class SustcNewsInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'newsUrl')

class ClubActivityAdmin(admin.ModelAdmin):
    list_display = ('title','location','content','time','host')

class OfficialActivityAdmin(admin.ModelAdmin):
    list_display = ('title','location','content','time','host')

class MainPageFunctionInfoAdmin(admin.ModelAdmin):
    list_display = ('name','url','intro','color','pageurl','pictureurl','videourl')


class SustcNewsInfoAdmin(admin.ModelAdmin):
    list_display = ('title','newsImage','img_url')


admin.site.register(SustcNewsInfo,SustcNewsInfoAdmin)
admin.site.register(MainPageInfo,MainPageFunctionInfoAdmin)
admin.site.register(OfficialActivity,OfficialActivityAdmin)
admin.site.register(ClubActivity,ClubActivityAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Location, LocalAdmin)
admin.site.register(SellInfo, SellInfoAdmin)
admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(Blame_star, Blame_starAdmin)
admin.site.register(Blame_Wall, Blame_WallAdmin)
admin.site.register(UserBooksInfo, LibInfoUser)
admin.site.register(AcademicForumInfo, ForumInfoAdmin)
admin.site.register(FunctionUsedTimes, FunctionTimesAdmin)
admin.site.register(Blame_comment, Blame_CommentAdmin)
admin.site.register(Activity_Wall, Activity_WallAdmin)
admin.site.register(Teacher_Info, Teacher_InfoAdmin)
