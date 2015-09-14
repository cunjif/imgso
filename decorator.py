#/usr/bin/env python
#-*- coding:utf-8 -*-

__author__="Yiu"

import chacracter
import calcsimmilar
import featureIndex
import threading
import os
import app


def __decorator(ImageName,ImageSavePath):
    ftrindex = chacracter.getImageIndex(ImageSavePath)
    if not isinstance(ftrindex,float) and not isinstance(ftrindex,int):
        raise Exception("ftrindex is not a number")
    dataImageList = featureIndex.selectFeatureIndex(ftrindex)
    if isinstance(dataImageList,int) or len(dataImageList) == 0:
        return -1
    res = calcsimmilar.calc_similiar(ImageSavePath,dataImageList)
    return res

def __run(ImageName,ImageSavePath):
    resImage = {}   
    global t
         
    resImage = __decorator(ImageName,ImageSavePath)
    t = threading.Thread(target=featureIndex.insertFetures,args=(ImageName,ImageSavePath))
    return resImage
    
def main_(ImgName,ImageSavPath):
    resImage = __run(ImgName,ImageSavPath)
    if not t==None:
        t.start()
        t.join()
    if isinstance(resImage,int) or len(resImage)==0:
        return None
    else:
        return resImage
    os.chdir(app.ROOTDIR)

if __name__=='__main__':
    main_('1 (2).jpg','./1 (2).jpg')