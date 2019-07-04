# -*- coding: utf8 -*-
from script.object_factory import SetGlobalApp

def CreateApp():
    import script.fight.fight as ModFt
    return SetGlobalApp(ModFt.CFight())
