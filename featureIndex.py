#/usr/bin/env python
#-*- coding:utf-8 -*-

__author__ = "Yiu"

from functools import reduce
import sqlite3 as sql
import os,os.path
import logging
import random
import string
import glob
import time
import app

try:
    import chacracter
except ImportError:
    raise Exception("no this module")

#sql
createTable = "create table if not exists ImageIndex(id Integer primary key autoincrement,ImageName varchar(50) not null unique,FeatureIndex float not null,ImageSavePath varchar(300) not null);"

savCurImageFeatures = "insert into ImageIndex(ImageName,FeatureIndex,ImageSavePath) values(?,?,?);"


#----------------***************----------------------
ROOTDIR = None
try:
    ROOTDIR = app.ROOTDIR
except:
    ROOTDIR = os.path.abspath('./')
DBDIR = "indexdbfiles"
DBFILEPATH = ROOTDIR + "/" + DBDIR

#----------------***************----------------------

def __checkdbfilename():
    dbfilename = "index{}.db".format(reduce(lambda x,y:x+y,random.sample(string.digits,5)))
    if os.path.exists("%s/%s" % (DBFILEPATH,dbfilename)):
        __checkdbfilename()
    else:
        return dbfilename
        
def __createNewTable(dbfilename):
    try:
        os.chdir(DBFILEPATH)
        conn = sql.connect("".join(dbfilename),timeout=30)
        os.chdir(ROOTDIR)
        cur = conn.cursor()
        cur.execute(createTable)
        conn.commit()
        return (cur,conn)
    except sql.OperationalError:
        print ("failed to create new database")
        exit(1)

def __initdb():
    tmpdb=[]
    usedb=[]
    conn = None
    if not os.path.exists("".join(DBFILEPATH)):
        os.mkdir("%s/%s" % (ROOTDIR,DBDIR))
    dbfilename = __checkdbfilename()
    #遍历已存在的数据库，并判断是否需要创建新的数据库
    tmpdb = glob.glob("%s/*.db" % DBFILEPATH)
    if tmpdb.__len__() == 0:
        (cur,conn) = __createNewTable(dbfilename)
        return (cur,conn)
    else:
        try:
            tmpdb = [os.path.split(x) for x in tmpdb]
            usedb = [x for p,x in tmpdb if os.path.isfile("%s/%s" % (p,x)) and ((os.path.getsize("%s/%s" % (p,x))/1024**2)<2)]
        except:
            os.chdir(DBFILEPATH)
            tmpdb = glob.glob("*.db")
            os.chdir(ROOTDIR)
            usedb = [x for x in tmpdb if os.path.isfile("%s/%s" % (p,x)) and ((os.path.getsize("%s/%s" % (p,x))/1024**2)<2)]
        if usedb.__len__() == 0:
            (cur,conn) = __createNewTable(dbfilename)
            return (cur,conn)
        else:
            try:
                os.chdir(DBFILEPATH)
                conn = sql.connect(usedb[0],timeout=30)
                os.chdir(ROOTDIR)
                cur = conn.cursor()
                return (cur,conn)
            except sql.OperationalError:
                return None,None


def __insertImageFeatures(ImageName,FeatureIndex,ImageSavePath):
    cur,conn = __initdb()
    if not cur and not conn:
        return -1
    try:
        cur.execute(savCurImageFeatures,(ImageName,FeatureIndex,ImageSavePath))
        conn.commit()
    except sql.OperationalError:
        return -1
    if cur and conn:
        cur.close()
        conn.close()
    return 1

def insertFetures(ImageName,ImageSavePath):
    FeatureIndex = chacracter.getImageIndex(ImageSavePath)
    check = 0
    try:
        check = __insertImageFeatures(ImageName,FeatureIndex,ImageSavePath)
    except:
        check = 0
    if check==1:
        os.chdir(ROOTDIR)
        with open("log","a") as f:
            f.write("Save recieved image:%s file okay at %s\n" % (ImageName,time.ctime()))
    else:
        os.chdir(ROOTDIR)
        with open("log","a") as f:
            f.write("Save recieved image:%s file failed at %s\n" % (ImageName,time.ctime()))
        
def selectFeatureIndex(FeatureIndex):
    SELECTFEATUREINDEX = "select ImageSavePath from ImageIndex where FeatureIndex>? and FeatureIndex<?;"
    tmprel = []
    dataImageList = []
    
    tmpdb = glob.glob("%s/*.db" % DBFILEPATH)
    if len(tmpdb) == 0:
        return 0
    try:
        tmpdb = [os.path.split(x) for x in tmpdb]
        tmpdb = [f for p,f in tmpdb]
    except:
        os.chdir(DBFILEPATH)
        tmpdb = glob.glob("*.db")
        os.chdir(ROOTDIR)
    for dbname in tmpdb:
        os.chdir(DBFILEPATH)
        conn = sql.connect("".join(dbname),timeout=30)
        os.chdir(ROOTDIR)
        cur = conn.cursor()
        cur.execute(SELECTFEATUREINDEX,(FeatureIndex*0.985,FeatureIndex*1.015))
        conn.commit()
        rs = cur.fetchall()
        tmprel.append(rs)
        cur.close()
        conn.close()
    if tmprel.__len__() == 0:
        return 0
    for rs in tmprel:
        for rss in rs:
            dataImageList.append(rss[0])
    return dataImageList
        
        
        
    
    
if __name__=="__main__":
    insertFetures("1.png","./1.png")
    

    

    

            