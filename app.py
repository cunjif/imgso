#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import sys,os,re
rootpath = os.getcwd()
rootpath = re.findall(r'.+imgso', rootpath, flags=0)[0]
sys.path.insert(0, rootpath)

try:
    from __init__ import app
except ImportError:
    print("import __init__ module error")
    exit(-1)

if __name__ == "__main__":
    app.config.from_pyfile('conf.py')
    app.run(debug=app.config['DEBUG'],host=app.config['HOST'],port=app.config['PORT'])
