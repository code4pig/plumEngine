# -*- coding: utf8 -*-
from script.object_factory import SetGlobalApp

def CreateApp():
    import script.dbproxy.dbproxy as ModDb
    return SetGlobalApp(ModDb.CDbProxy())
