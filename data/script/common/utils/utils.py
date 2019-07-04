# -*- coding: utf-8 -*-
"""
@author: bbz
"""
import sys
import script.common.xupdate as xupdate


def WriteLog(msg):
    print msg


def Reload(modname):
    mods = [modname]
    if not sys.modules.has_key(modname):
        strs = modname.split(".")
        if len(strs) > 1:
            mods = [modname]  # consider as full path, but not imported
        else:
            quick_key = modname
            mods = __quick_mod_map__.get(quick_key)

    if not mods:
        WriteLog("找不到 %s 对应的模块. Ignore Reload." % modname)
        return []

    for mod in mods:
        WriteLog("reload:%s" % mod)
        xupdate.update(mod)  # reload
    return mods


def execute_reload_files_command(gm_params_str):
    reload_file_list = [x.strip() for x in gm_params_str.split(',') if x]
    fail_file_list = []
    for reload_file in reload_file_list:
        try:
            Reload(reload_file)
        except Exception as e:
            WriteLog('reload file %s error, %s' % (reload_file, e.message))
            fail_file_list.append(reload_file)
    return fail_file_list


def byte2str(msg):
    import msgpack
    #showmsg = ''.join((r'\x%02x' % ord(c) for c in msg))
    return "%s" % (msgpack.unpackb(msg))