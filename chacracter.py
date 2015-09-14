#!/usr/bin/env python
#-*- coding:utf-8 -*-

__author__ = "Yiu"

from  PIL import Image
import math
import logging
import cv2
from functools import reduce
import numpy as np
from hashlib import md5

"""用于图像特征的提取"""

#图像裁剪，统一规格ima
def convertimage(image,x=256,y=256):
    """
    使用resize,convert方法对传进来的图像进行裁剪，默认统一成256x256像素RGB模式的规格
    """
    return Image.open(image).resize((x,y)).convert("RGB")
    
#额外方法定义
def mapmethod(methodname):
    def LBP(image):
        """
        二值化处理函数
        """
        x,y = image.size
        l=[]
        for i in range(x):
            for j in range(y):
                if image.getpixel((i,j)) > image.getpixel((1,1)):
                    l.append(1)
                elif image.getpixel((i,j)) < image.getpixel((1,1)):
                    l.append(0)
                else:
                    l.append(1)
        return l
        
    def cannythreshold(img,gray,ratio,core_size,lowthreshold):
        """canny算子"""
        edge = cv2.GaussianBlur(gray,(3,3),0)
        edge = cv2.Canny(edge,lowthreshold,lowthreshold*ratio,apertureSize = core_size)
        aim = cv2.bitwise_and(img,img,mask=edge)
        return aim
    
    if methodname == "LBP":
        return LBP
    elif methodname == "cannythreshold":
        return cannythreshold
    else:
        pass

#对灰度值的提取
def greyvalue(image):
    image=convertimage(image)
    W,H=image.size
    w,h=64,64
    assert W % w == H % h == 0
    image = [image.crop((i,j,i+w,j+h)).copy().histogram() for i in range(0,W,w) for j in range(0,H,h)]
    return image
    
#对纹理特征的提取
#使用LBP算法
def getLBP(image):
    image = convertimage(image)
    width,height=image.size
    w,h=(3,3)
    greyImage=[]
    imgcroplist = [image.crop((x,y,x+w,y+h)).copy() for x in range(0,width,w) for y in range(0,height,h)]   #将图片切割成3*3的小区域块
    
    LBP = mapmethod("LBP")
    binarymap = map(LBP,imgcroplist)  
    binTexture = []
    try:
        for x in binarymap:
            binTexture.extend(x)
        return binTexture
    except TypeError:
        logging.exception("binarymap can't not for")
        return 0

#pHash算法
def pHash(image):
    image = Image.open(image).resize((8,8)).convert("L")
    colordatalist = list(image.getdata())
    avr = sum(colordatalist)/64
    plist = [0 if x<avr else 1 for x in colordatalist]
    ps = reduce(lambda x,y:str(x)+str(y),plist)
    return md5(ps.encode("ascii")).hexdigest()
    
    
#轮廓特征提取
def getContours(image):
    image = cv2.imread(image)
    image = cv2.resize(image,(512,512))
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    ret,dst = cv2.threshold(gray,128,255,cv2.THRESH_BINARY)
    image,contour,hierarchy = cv2.findContours(dst,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)     
    return image

#图像的表示数获取        
def getImageIndex(image):
    contindex = 0
    lbpindex = 0
    greyindex = 0
        
    cont = getContours(image)
    for cons in cont:
        contindex = sum(cons)
    
    lbp = getLBP(image)
    lbpindex = sum(lbp)
        
    his = greyvalue(image)
    for x in his:
        greyindex += sum(x)
        
    return contindex*0.6 + lbpindex*0.2 + greyindex*0.2
    
if __name__=='__main__':
    try:
        pass
    except :
        logging.exception("File is not found!")
    
    