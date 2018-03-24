# -*- coding: utf-8 -*-
from Market.models import *
from Management.models import *
from Webfunc.models import *

def filterChar(s,addmore=True):
    if type(s) != type(unicode()) and type(s) != type(""):
        return s
    r = ""
    for i in s:
        if not (i=="\"" or i=="\'"):
            r+=i
    if addmore:
        return "\""+r+"\""
    else:
        return r
    
class OBJ_Convert:
    def __init__(self,OBJname,initInfoDict=None,ForeighKey={},OBJid=None):
        self.info = ""
        self.OBJid = OBJid
        if initInfoDict:
            for i,j in initInfoDict.iteritems():
                setattr(self,i,j.get("value"))
                if "Date" in i or "Image" in i:
                    initInfoDict[i] = None
                    continue
                temp = j.get("value")
                if i in ForeighKey.keys():
                    vv = ForeighKey.get(i)[1]
                    obj = eval(ForeighKey.get(i)[0]+'.objects.get(%s)'%str(vv+"="+"\""+temp+"\""))   
                    initInfoDict[i] = obj
                    continue
                if temp:
                    try:
                        temp = int(temp)
                    except Exception:
                        if temp=="True":
                            temp = True
                        elif temp=="False":
                            temp = False
                        else:
                            temp = "\""+temp+"\""
                    self.info+=i+"="+str(temp)+","
                    initInfoDict[i] = temp
        self.initInfoDict = initInfoDict
        self.info = self.info[0:-1]
        self.OBJname = OBJname
        self.ForeighKey = ForeighKey
    def createOBJ(self):
        if len(self.ForeighKey)==0:
            eval(self.OBJname+'.objects.create(%s)'%str(self.info))
        else:
            myobj = eval(self.OBJname+'.objects.create(%s)'%str(self.info))
            for item,fitem in self.ForeighKey.iteritems():
                value = self.initInfoDict.get(item)
                value = "\""+str(value)+"\""
                value = filterChar(value)
                obj = eval(fitem[0]+'.objects.get(%s)'%str(fitem[1]+"="+value))
                setattr(myobj,item,obj)
            fun = getattr(myobj,"save")
            fun()
    def changeOBJ(self):
        if not self.OBJid:
            print "Please Provide an id"
        myobj = eval(self.OBJname+'.objects.get(%s)'%str("id="+str(self.OBJid)))
        for key,item in self.initInfoDict.iteritems():
            if "Date" in key:
                continue
            if not item:
                continue
            item = filterChar(item,addmore=False)
            setattr(myobj,key,item)
        fun = getattr(myobj,"save")
        fun()
    def deleteOBJ(self):
        eval(self.OBJname+'.objects.get(%s).delete'%str("id="+str(self.OBJid)))
    def getOBJ(self):
        return eval(self.OBJname+'.objects.get(%s)'%str("id="+str(self.OBJid)))
