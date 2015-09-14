#! /usr/bin/env python3
#-*- coding:utf-8 -*-

__author__ = "Yiu"
__date__ = 'Aug 2015'

from flask import *
import os,os.path
import re
import logging
import decorator

#*********************************#
ROOTDIR = os.path.abspath("./")
IMAGESDIR = 'static/dbimages'
SECRET = os.urandom(30)
#*********************************#
app  = Flask(__name__)

if app.secret_key  == None:
    app.secret_key = SECRET

@app.route('/',methods = ['GET','POST'])
def index():
    msg = None
    if request.method == 'POST':
        image = request.files['realImage']
        if image is None:
            return render_template("index.html")
        if not os.path.exists('%s/%s' % (ROOTDIR,IMAGESDIR)):
            os.mkdir('%s/%s' % (ROOTDIR,IMAGESDIR))
        if not re.match(r'.(jpg|jpeg|bmp|png)',os.path.splitext(image.filename)[1]):
            return render_template('ImgFormatError.html')
        if not os.path.exists(os.path.join(ROOTDIR,IMAGESDIR,image.filename)):
            image.save(os.path.join(ROOTDIR,IMAGESDIR,image.filename))
        rel = doSearch(image.filename,os.path.join(ROOTDIR,IMAGESDIR,image.filename))
        return redirect('/result')
    else:
        return render_template('index.html')


@app.route("/result",methods = ['POST','GET'])
def result():
    if not app.resultImage is None:
        result = {}
        for k,v in app.resultImage.items():
            result[k] = os.path.split(v)[1]
        return render_template("result.html",resultImage = result)
    else:
        return render_template("result.html",resultImage = None)

def doSearch(ImageName,ImageSavePath):
    resImage = decorator.main_(ImageName,ImageSavePath)
    if not resImage is None:
        app.resultImage = resImage
        return True
    else:
        app.resultImage = None
        return False


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0",port=3000)
