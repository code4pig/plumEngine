# -*- coding: utf8 -*-

globalapp = None

def CreateApp():
    global globalapp
    return globalapp

def SetGlobalApp(app):
    global globalapp
    globalapp = app
    return globalapp