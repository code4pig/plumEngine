# -*- coding: utf8 -*-
from script.object_factory import SetGlobalApp


def CreateApp():
    import script.gateway.gateway as ModGw
    return SetGlobalApp(ModGw.CGateWay())
