# -*- coding: utf-8 -*-

# Author : Yoray
# Created: 2018-07-09 15:45

from script.object_factory import SetGlobalApp


def CreateApp():
    import script.sceneproxy.sceneproxy as mod_scene_proxy
    return SetGlobalApp(mod_scene_proxy.CSceneProxy())