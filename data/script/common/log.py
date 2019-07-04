# -*- coding: utf-8 -*-
"""
@author: bbz
"""
import game


class CLogger(object):
    def __init__(self, mod):
        self.mod = mod

    def debug(self, msg):
        game.Log(game.LOG_LV_DEBUG, msg, self.mod)

    def info(self, msg):
        game.Log(game.LOG_LV_INFO, msg, self.mod)

    def warn(self, msg):
        game.Log(game.LOG_LV_WARNING, msg, self.mod)

    def error(self, msg):
        game.Log(game.LOG_LV_ERROR, msg, self.mod)


g_LoggerMap = {}


def GetLog(mod="script"):
    global g_LoggerMap
    if mod not in g_LoggerMap:
        g_LoggerMap[mod] = CLogger(mod)
    return g_LoggerMap[mod]
