# -*- coding: utf8 -*-
from script.object_factory import SetGlobalApp

def CreateApp():
    import script.testclient.testclient as ModTc
    return SetGlobalApp(ModTc.CTestClient())
