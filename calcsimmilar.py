#!/usr/bin/env python
#-*- coding:utf-8 -*-

__author__ = "Yiu"

import cv2
import numpy
import logging
import sys
import os,os.path

sys.path.append("./")

try:
    import chacracter
except ImportError:
    logging.exception("no chacracter module")


__author__="Ubinch"
    

#-------------*******************--------------------

#第一个参数是待检测图片，第二个参数是符合相似加权值范围的图片列表
#返回图片的灰度相似度，是一个列表
def __calc_histogram_similar(checkedImage,dataImageList):
    calc_histogram_rel = []
    checkedImage = chacracter.greyvalue(checkedImage)
    checkedImage = [x for y in checkedImage for x in y]   
   
    if dataImageList.__len__()==1:
        checkingImage = chacracter.greyvalue(dataImageList[0])
        checkingImage = [x for y in checkingImage for x in y]
        assert len(checkedImage) == len(checkingImage)
        tmp = sum(1-(0 if ci==dil else float(abs(ci-dil))/max(ci,dil)) for ci,dil in zip(checkedImage,checkingImage))/len(checkedImage)
        calc_histogram_rel.append(tmp)
        return calc_histogram_rel
    
    else:
        for checkingImage in dataImageList:
            checkingImage = chacracter.greyvalue(checkingImage)
            checkingImage = [x for y in checkingImage for x in y]
            assert len(checkedImage) == len(checkingImage)
            tmp = sum(1-(0 if ci==dil else float(abs(ci-dil))/max(ci,dil)) for ci,dil in zip(checkedImage,checkingImage))/len(checkedImage)
            calc_histogram_rel.append(tmp)
            tmp = None
        return calc_histogram_rel
        

#轮廓相似度比较
def __calc_contours_similiar(checkedImage,dataImageList):
    checkedImage = chacracter.getContours(checkedImage)
    calc_contours_rel = []
    
    if len(dataImageList) == 1:
        dataImage = chacracter.getContours(dataImageList[0])
        tmp = cv2.matchShapes(checkedImage,dataImage,3,1.0)
        calc_contours_rel.append(tmp)
        return calc_contours_rel
    else:
        for checkingImage in dataImageList:
            checkingImage = chacracter.getContours(checkingImage)
            tmp = cv2.matchShapes(checkedImage,checkingImage,3,1.0)
            calc_contours_rel.append(tmp)
            tmp = None
        return calc_contours_rel
    
#LBP二值相似度对比    
def __calc_LBP_similiar(checkedImage,dataImageList):
    calc_lbp_rel = []
    checkedImage = chacracter.getLBP(checkedImage)
    
    if len(dataImageList) == 1:
        checkingImage = chacracter.getLBP(dataImageList[0])
        tmplen = [x for x,y in zip(checkedImage,checkingImage) if x==y]
        tmp = float(tmplen.__len__()/len(checkedImage))
        calc_lbp_rel.append(tmp)
        return calc_lbp_rel
    else:
        for checkingImage in dataImageList:
            checkingImage = chacracter.getLBP(checkingImage)
            tmplen = [x for x,y in zip(checkedImage,checkingImage) if x==y]
            tmp = 1 - float(tmplen.__len__()/len(checkedImage))  #越小相似度越高
            calc_lbp_rel.append(tmp)
            tmplen = []
            tmp = None
        return calc_lbp_rel
        
            
#汉明距离计算感应哈希算法的指纹码的相似性
#小于6则判断相似
def __calc_hanming_similiar(checkedImage,dataImageList):
    calc_hanming_rel = []
    checkedImage = chacracter.pHash(checkedImage)
    
    if len(dataImageList) == 1:
        checkingImage = chacracter.pHash(dataImageList[0])
        diff = 0
        assert len(checkedImage) == len(checkingImage)
        for x in range(len(checkedImage)):
            if checkedImage[x] != checkingImage[x]:
                diff += 1
        calc_hanming_rel.append(diff)
        return calc_hanming_rel
    else:
        diff = 0
        for checkingImage in dataImageList:
            checkingImage = chacracter.pHash(checkingImage)
            assert len(checkedImage) == len(checkingImage)
            for x in range(len(checkedImage)):
                if checkedImage[x] != checkingImage[x]:
                    diff += 1
            calc_hanming_rel.append(diff)
            diff = 0
        return calc_hanming_rel
        
#权重百分比
def __percents(x):
    if x<1.0 and x>0.8:
        return 0.2
    elif x<0.8 and x>0.6:
        return 0.4
    elif x<0.6 and x>0.4:
        return 0.6
    elif x<0.4 and x>0.2:
        return 0.8
    elif x<0.2 and x>0.1:
        return 0.92
    else:
        return 1
    
def calc_similiar(checkedImage,dataImageList):
    histogram = []
    contours = []
    LBP = []
    hanming = []
    rellist = {}
    if len(dataImageList) == 1:
        histogram = __calc_histogram_similar(checkedImage,dataImageList)
        contours = __calc_contours_similiar(checkedImage,dataImageList)
        LBP = __calc_LBP_similiar(checkedImage,dataImageList)
        hanming = __calc_hanming_similiar(checkedImage,dataImageList)
        # 3 3 3 1 权重
        if len(histogram)==len(contours)==len(LBP)==len(hanming)==1:
            rel = __percents(histogram[0])*3+__percents(contours[0])*4+__percents(LBP[0])*2+(1 if hanming[0]<6 else 0)*1
            if rel>5.4:
                rellist[0] = dataImageList[0]
        return rellist
    else:
        histogram = __calc_histogram_similar(checkedImage,dataImageList)
        contours = __calc_contours_similiar(checkedImage,dataImageList)
        LBP = __calc_LBP_similiar(checkedImage,dataImageList)
        hanming = __calc_hanming_similiar(checkedImage,dataImageList)
        if len(histogram)==len(contours)==len(LBP)==len(hanming)==len(dataImageList):
            for x in range(len(dataImageList)):
                rel = __percents(histogram[x])*3+__percents(contours[x])*3+__percents(LBP[x])*3+(1 if hanming[x]<6 else 0)*1
                if rel>7.5:
                    rellist[rel] = os.path.split(dataImageList[x])[1]
        return rellist
        
if __name__ == '__main__':
    pass