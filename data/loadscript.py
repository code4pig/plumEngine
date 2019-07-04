# -*- coding: utf8 -*-

"""
加载脚本的入口
"""

import re, os, sys

global gRootPath
global mods
global g_py_patt
global g_invalid_py_patt
global g_unwalk_patt
global g_unwalk_path

gRootPath = None
mods = []
# 有效的文件名
g_py_patt = re.compile(r'\.py$', re.I)
# 无效的文件名
g_invalid_py_patt = re.compile(r'__init__\.py', re.I)
# 不遍历.开头的所有文件夹和子文件夹比如.svn
g_unwalk_patt = re.compile(r'^\.', re.I)
# 第一层目录，每个app可以分别有自己不需要遍历的文件夹，默认不加载netdriver目录。
g_unwalk_path = {
    "gateway": ["netdriver", ],
}


def addmod(curpkg, filename):
    global mods
    global g_py_patt
    global g_invalid_py_patt

    if (g_py_patt.search(filename) == None):
        return
    if (g_invalid_py_patt.search(filename) != None):
        return
    modname = g_py_patt.sub('', filename)
    modname = "%s.%s" % (curpkg, modname)
    mods.append(modname)


def myimport(modname):
    __import__('%s' % (modname))


def rootwalk(curpkg, path, unwalk_pathes):
    os.chdir(path)
    for item in os.listdir("./"):
        if os.path.isdir(item):
            if unwalk_pathes and item in unwalk_pathes:
                continue
            subwalk(curpkg, item)
        else:
            addmod(curpkg, item)


def subwalk(curpkg, subdir):
    global g_unwalk_patt

    if (g_unwalk_patt.search(subdir) != None):
        return
    os.chdir(subdir)
    curpkg = "%s.%s" % (curpkg, subdir)
    for item in os.listdir("./"):
        if os.path.isdir(item):
            subwalk(curpkg, item)
        else:
            addmod(curpkg, item)
    os.chdir("..")


# LoadFrom，加载源是哪个进程模块，方便进行一些加载控制
def load(path, package, loadfrom, loadtype=0):
    global g_unwalk_path
    global mods
    global gRootPath

    sinfo = ""
    unwalk_pathes = g_unwalk_path.get(loadfrom, ["netdriver"])
    if unwalk_pathes:
        sinfo = str(unwalk_pathes)

    if loadfrom in package:
        if (sinfo != ""):
            print "%s begin to load script directory except %s" % (loadfrom, sinfo)
        else:
            print "%s begin to load script directory" % (loadfrom)

    gRootPath = os.path.realpath("./")
    rootwalk(package, path, unwalk_pathes)
    os.chdir(gRootPath)

    for modname in mods:
        myimport(modname)

    if loadfrom in package:
        print 'Total : %d script file imported.' % (len(mods))
        print 'DONE'


if (__name__ == '__main__'):
    if (len(sys.argv) != 3):
        print 'Usage: %s PATTERN PATH ' % (sys.argv[0])
        print 'such as: %s script script ' % (sys.argv[0])
    else:
        load(sys.argv[1], sys.argv[2])
