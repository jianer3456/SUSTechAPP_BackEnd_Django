# -*- coding: UTF-8 -*-

from jwxt_ClassProcess import *
user = raw_input("输入学号：")
pwd = raw_input("输入密码：")

if user!="" and pwd!="":
    cp = Class_Process(user,pwd)
else:
    exit(0)
# listaa = cp.GetAllPossibleClassList(["即兴创编","电子创意设计I","托福听说"])
Classname = cp.showAllClassName()

name = "00"
classNamelist = []
while name!="":
    name = raw_input("输入课程名称:")
    for i in Classname:
        if name=="":
            break
        if name in i:
            classNamelist.append(i)
            print i+"添加成功"


print "获取了所有课程名称，排列课表如下"
tablelist = cp.GetAllPossibleClassList(classNamelist)

print "共有课表"+str(len(tablelist))
showNum = raw_input("显示前多少张课程表(默认显示前5张):")

if showNum=="":
    showNum = 5

isshowTeacher = raw_input("显示老师？默认不显示（y or n）")
if isshowTeacher=="n" or isshowTeacher=="":
    isshowTeacher = False
else:
    isshowTeacher = True


count = 1
for i in tablelist:
    print "课表"+str(count)
    print "学分："+str(countScore(i))

    cp.showClassTable(i,showTeacher=isshowTeacher)
    if count>=int(showNum):
        print "共有课表"+str(len(tablelist))+"显示了"+str(count)
        break
    count += 1

chosenTable = raw_input("选择哪个课表？（默认选第一张）输入课表序号：")
if chosenTable=="":
    chosenTable = 1

# cp.ChooseByClassList(tablelist[count-1])
time = raw_input("选课时间（例：201705222200）：")
if time=="":
    time = 0
cp.chooseAtTime(str(time),tablelist[int(chosenTable)-1])
# cp.Choosetttt(tablelist[count-1])


