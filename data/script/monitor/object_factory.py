# -*- coding: utf-8 -*-
# __author__ = 'Yoray'
from script.object_factory import SetGlobalApp

def CreateApp():
    import script.monitor.monitor as ModMonitor
    return SetGlobalApp(ModMonitor.CMonitor())
