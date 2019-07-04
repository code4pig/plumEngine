# -*- coding: utf-8 -*-
"""
@author: bbz
"""
import game
import sys
import os


def insert_script_path():
    if game.isdebug:
        AddPath("../3rd/libs/python27_d/DLLs")
    else:
        AddPath("../3rd/libs/python27/DLLs")
    AddPath("../3rd/libs/python27/Tools")

    print sys.path


def AddPath(path):
    if not os.path.exists(path):
        raise Exception("AddPath failed! not exist path:%s" % path)
    sys.path.append(path)
    print "add sys path:%s" % path
