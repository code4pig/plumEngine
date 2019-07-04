# -*- coding: utf8 -*-
from script.object_factory import SetGlobalApp

def CreateApp():
    import script.chat.chat as ModCt
    return SetGlobalApp(ModCt.CChat())
