# -*- coding: utf8 -*-
from script.object_factory import SetGlobalApp

def CreateApp():
    import script.fightproxy.fightproxy as ModFt
    return SetGlobalApp(ModFt.CFightProxy())
