# -*- coding: utf8 -*-
from script.object_factory import SetGlobalApp

def CreateApp():
    import script.chatproxy.chatproxy as ModCp
    return SetGlobalApp(ModCp.CChatProxy())
