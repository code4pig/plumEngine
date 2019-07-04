# -*- coding: utf8 -*-
print "import script..."

import __builtin__
import sys, types

if not hasattr(__builtin__, "__ori__import__"):
    setattr(__builtin__, "__ori__import__", __builtin__.__import__)

if not hasattr(__builtin__, "__quick_mod_map__"):
    setattr(__builtin__, "__quick_mod_map__", {})


def print_python():
    print "python-version:", sys.version
    print "python-path:", sys.path


def reg_mod_idx(modins, modname, globals=None, locals=None, fromlist=None, level=None):
    fullmodnames = []

    mods = []
    if fromlist:
        for f in fromlist:
            obj = getattr(modins, f, None)
            if type(obj) is types.ModuleType:
                # fullmodnames.append(modname+"."+f)
                mods.append(obj)
            else:
                # fullmodnames.append(modname)
                mods.append(modins)
                break
    else:
        # fullmodnames.append(modname)
        mod = modins
        components = modname.split('.')
        for comp in components[1:]:
            mod = getattr(mod, comp, None)
            if mod is None:
                # print "not loaded mod, mybe in recusive import...", modname
                break
        if mod:
            mods.append(mod)

    for mod in mods:
        fullmodnames.append(mod.__name__)

    filemodnames = []
    for fullname in fullmodnames:
        # if fullname == "script.globalcommon.item.citem.item":
        #	print modname, fromlist
        mod = sys.modules.get(fullname)
        if not mod:
            continue
        modfile = getattr(mod, "__file__", None)
        if modfile and modfile.find("__init__.") < 0:
            filemodnames.append(fullname)

    if not filemodnames:
        return

    for filemodname in filemodnames:
        quick_key = filemodname.split(".")[-1]

        modnames = __quick_mod_map__.get(quick_key)
        if modnames is None:
            modnames = __quick_mod_map__[quick_key] = set()
        modnames.add(filemodname)
        # if filemodname == "script.globalcommon.item.citem.item":
    #	print "quick_key", quick_key
    #	print  "quick_mods", __quick_mod_map__[quick_key]
    #	print "fullmodnames", fullmodnames
