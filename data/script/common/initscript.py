# -*- coding: utf-8 -*-
'''
@author: bbz
'''

import game
import script
import traceback, sys

traces = None
gTipFuncInited = False
gTipTraceImpl = None
gCheckTipTraceImpl = None

HOOK_MODULES = {"json": "ujson"}


def GetTraces():
    global traces
    if traces is None:
        import collections
        print "init global traces cache"
        traces = collections.deque()  # thread-safe

    return traces


def OnException(type, value, tb):
    print "OnException"
    if (hasattr(sys, 'last_traceback')):
        msgs = traceback.format_exception(type, value, tb)
        TipTrace(msgs)

    sys.__excepthook__(type, value, tb)


def TipTrace(msgs):
    new_msgs = []
    for msg in msgs:
        new_msgs.append(msg.replace("%", "%%"))

    if game.isdebug:
        TipTrace4Dev(new_msgs)


def TipTrace4Dev(msgs):
    global gTipTraceImpl
    global gTipFuncInited

    if not gTipFuncInited:
        print "add server trace before init"
        GetTraces().append(msgs)
        return

    if not gTipTraceImpl:
        return

    if not gTipTraceImpl(msgs):
        print "add server trace"
        GetTraces().append(msgs)


def PrintSavedTrace(*args):
    global traces
    global gTipTraceImpl
    global gCheckTipTraceImpl

    if not traces:
        return

    if not gCheckTipTraceImpl():
        return

    i = 0
    while traces and i < 5:
        msgs = traces.popleft()
        print "PrintSavedTrace"
        gTipTraceImpl(msgs)
        i += 1

    if len(traces) > 0:
        gTipTraceImpl(["队列中trace消息太多，请查看日志"])


def InitServerTraceTipFunc(f, fc):
    if not game.isdebug:
        return

    print "InitServerTraceTipFunc"

    global gTipTraceImpl
    global gCheckTipTraceImpl
    global gGetTipServiceName
    gTipTraceImpl = f
    gCheckTipTraceImpl = fc

    global gTipFuncInited
    gTipFuncInited = True

    game.RegTick(PrintSavedTrace, None, 1 * 1000)


def print_exc_hook(*args):
    traceback.ori_print_exc(*args)

    msg = traceback.ori_format_exc()
    msgs = msg.split("\n")
    TipTrace(msgs)


def format_exc_hook(*args):
    msg = traceback.ori_format_exc()
    msgs = msg.split("\n")
    TipTrace(msgs)

    return msg


def hook_trace_4_serverdebug():
    print "HOOK_trace_4_serverdebug"
    sys.excepthook = OnException

    if getattr(traceback, "ori_print_exc", None) is None:
        setattr(traceback, "ori_print_exc", traceback.print_exc)

    if getattr(traceback, "ori_format_exc", None) is None:
        setattr(traceback, "ori_format_exc", traceback.format_exc)

    traceback.print_exc = print_exc_hook
    traceback.format_exc = format_exc_hook


def __my_import__(modname, *args, **kws):
    try:
        modins = __ori__import__(HOOK_MODULES.get(modname, modname), *args, **kws)
        if game.isdebug:
            script.reg_mod_idx(modins, modname, *args, **kws)
        return modins
    except ImportError, ex:
        if str(ex).find("script") >= 0:
            raise
        else:
            if modname.find("script") == 0:
                raise ImportError("加载脚本%s出错  err:%s" % (modname, ex))
            else:
                raise  # keep ori raise


script.print_python()
import pyximport

pyximport.install()
print "HOOK __import__..."
buildin = sys.modules['__builtin__']
setattr(buildin, "__import__", __my_import__)

if game.isdebug:
    hook_trace_4_serverdebug()
