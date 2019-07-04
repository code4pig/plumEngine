# -*- coding: utf-8 -*-

# Author : Yoray
# Created: 2018-07-09 15:42

from script.object_factory import SetGlobalApp


def CreateApp():
    import script.scene.scene as mod_scene
    return SetGlobalApp(mod_scene.CScene())
