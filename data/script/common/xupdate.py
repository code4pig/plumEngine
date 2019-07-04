# -*- coding: utf8 -*-
# $Id: xupdate.py 62830 2010-05-18 06:48:13Z akara $
# 
# 热更新的目标：
#   支持：
#   (1)更新代码定义(function/method/static_method/class_method)
#   (2)不更新数据(除了代码定义外的类型都当作是数据)；
#   (3)第一次import，调用模块的__first_import__函数;
#      执行更新前，调用模块的__before_update__函数；
#      执行更新后，调用模块的__after_update__函数
#   (4)本模块自身也支持同样规则的热更新；但需要慎重更改本模块
#   不支持：
#   (1)不支持命名空间的命名删除；reload本身决定了修改文件来删除命名是不生效的。
#   (2)不支持中途新添的代码定义的[重定向]后再热更新。
#   (3)不支持类的继承关系的修改
#
# TODO:
# (1) 是否可以通过一些模块命名约定来实现模块级的 dict / list / set 更新？
# (2) 如果(1)可以实现，怎么实现 tuple frozenset 之类的固态容器更新呢？
# (3) 检查两次update之间是否存在对象泄漏？
#
# by AKara 2010.05.14
#
import sys
import types


# 取得一个对象的字符串描述
def _S(obj):
    return str(obj)[:50]


# 支持缩进打印的log函数
def _log(msg, depth=0):
    return


# print "%s %s"%("--" * depth, msg)


def update_data(oldobj, newobj, depth=1):
    handlers = get_valid_handlers(True)
    v_type = type(oldobj)
    handler = handlers.get(v_type)
    if handler:
        handler(oldobj, newobj, depth + 1)


def _update_list(oldobj, newobj, depth):
    handlers = get_valid_handlers(True)
    dislen = len(newobj) - len(oldobj)
    if dislen < 0:
        for i in xrange(-dislen):
            oldobj.pop()
    # newobj.extend([None] * -dislen)

    oldLen = len(oldobj)
    for i, newdata in enumerate(newobj):
        if i >= oldLen:
            oldobj.append(newdata)
            continue

        olddata = oldobj[i]
        v_type = type(newdata)
        handle = handlers.get(v_type)
        if handle:
            handle(olddata, newdata, depth + 1)
        else:
            oldobj[i] = newdata


def _update_dict(old_dict, new_dict, depth):
    handlers = get_valid_handlers(True)
    for newkey, newvalue in new_dict.iteritems():
        if newkey not in old_dict:
            old_dict[newkey] = newvalue

        oldv = old_dict[newkey]

        # 如果key对象类型在新旧class间不同，那留用旧class的对象
        if type(oldv) != type(newvalue):
            _log("[RD] %s : %s" % (newkey, _S(oldv)), depth)
            continue

        # 更新当前支持更新的对象
        v_type = type(newvalue)
        handler = handlers.get(v_type)
        if handler:
            handler(oldv, newvalue, depth + 1)
        else:
            old_dict[newkey] = newvalue

        # 由于是直接改oldv的内容，所以不用再setattr了。


old_list = []


def clear_old_funcs():
    global old_list
    del old_list[:]


# 用新的函数对象内容更新旧的函数对象中的内容，保持函数对象本身地址不变
def _update_function(oldobj, newobj, depth):
    global old_list
    old_list.append(getattr(oldobj, "func_code"))
    old_list.append(getattr(oldobj, "func_defaults"))
    old_list.append(getattr(oldobj, "func_doc"))

    setattr(oldobj, "func_code", newobj.func_code)
    setattr(oldobj, "func_defaults", newobj.func_defaults)
    setattr(oldobj, "func_doc", newobj.func_doc)

    _log("[U] func_code", depth)
    _log("[U] func_defaults", depth)
    _log("[U] func_doc", depth)


# 更改旧的方法对象，保持地址不变
def _update_method(oldobj, newobj, depth):
    _update_function(oldobj.im_func, newobj.im_func, depth)


# 用新类内容更新旧类内容，保持旧类本身地址不变
def _update_new_style_class(oldobj, newobj, depth):
    handlers = get_valid_handlers()
    for k, v in newobj.__dict__.iteritems():
        # 如果新的key不在旧的class中，添加之
        if k not in oldobj.__dict__:
            setattr(oldobj, k, v)
            _log("[A] %s : %s" % (k, _S(v)), depth)
            continue
        oldv = oldobj.__dict__[k]

        # 如果key对象类型在新旧class间不同，那留用旧class的对象
        if type(oldv) != type(v):
            _log("[RD] %s : %s" % (k, _S(oldv)), depth)
            continue

        # 更新当前支持更新的对象
        v_type = type(v)
        handler = handlers.get(v_type)
        if handler:
            _log("[U] %s : %s" % (k, _S(v)), depth)
            handler(oldv, v, depth + 1)
        # 由于是直接改oldv的内容，所以不用再setattr了。
        else:
            _log("[RC] %s : %s : %s" % (k, type(oldv), _S(oldv)), depth)


# 用新类内容更新旧类内容，旧类本身地址不变
def _update_old_style_class(oldobj, newobj, depth):
    _update_new_style_class(oldobj, newobj, depth)


def _update_staticmethod(oldobj, newobj, depth):
    # TODO: 这方法好hack，不知还有其他办法不?
    # 一个staticmethod对象，它的 sm.__get__(object)便是那个function对象
    oldfunc = oldobj.__get__(object)
    newfunc = newobj.__get__(object)
    _update_function(oldfunc, newfunc, depth)


def _update_classmethod(oldobj, newobj, depth):
    # 继续很hack的做法-_-
    oldfunc = oldobj.__get__(object).im_func
    newfunc = newobj.__get__(object).im_func
    _update_function(oldfunc, newfunc, depth)


# 因为types模块中没有
# (1)StaticMethodType
# (2)ClassMethodType
# 所以又要自己动手了
class CFoobar(object):
    @staticmethod
    def i_am_static_method(): pass

    @classmethod
    def i_am_class_method(cls): pass  # classmethod必须定义至少一个隐式cls参数


# 既然暂时不能更新dict类型的对象，
# 为了使得这个模块本身成为完全可以update的整体，
# 这个映射性质的dict就通过函数来返回吧
def get_valid_handlers(is_update_data=False):
    _StaticMethodType = type(CFoobar.__dict__["i_am_static_method"])
    _ClassMethodType = type(CFoobar.__dict__["i_am_class_method"])
    adict = {
        types.FunctionType: _update_function,
        types.MethodType: _update_method,
        types.TypeType: _update_new_style_class,
        _StaticMethodType: _update_staticmethod,
        _ClassMethodType: _update_classmethod,
        types.ClassType: _update_old_style_class,
        #	types.DictType : _update_dict,
        #	types.ListType : _update_list,
    }

    if is_update_data:
        adict[types.ListType] = _update_list
        adict[types.DictType] = _update_dict

    return adict


#
# 热更新模块
# 日志标志说明：
# F: First import
# U: Update
# S: Saving old key
# A: Adding new key
# RD: Restore old key because Different object type between old & new
# RC: Restore old key because Can't handle the object type
#
def _call_module_func(module, func_name, *args):
    func = module.__dict__.get(func_name, None)
    if type(func) != types.FunctionType:
        _log(">>>[%s] have no %s function, skip call<<<" % (str(module), func_name))
        return

    _log(">>>[%s] call %s function ok<<<" % (str(module), func_name))
    func(*args)


def update(module_name, is_update_data=False):
    # 将一些非法的格式，换成正确的格式。
    module_name = module_name.replace("/", ".")
    if module_name.endswith(".py"):
        module_name = module_name[0:len(module_name) - 3]
        # print "xupdate::update %s" % module_name
    depth = 1
    # print "on update "
    # print is_update_data
    # print " "
    module = sys.modules.get(module_name, None)
    if not module:  # 第一次import，不存在更新问题
        # print "Hello2"
        print "first import"
        module = __import__(module_name)
        _call_module_func(module, "__first_import__")
        _log("[F] %s : %s" % (module_name, module), depth)
        return module

    # 执行before update
    _call_module_func(module, "__before_update__")

    # 不是第一次，需要更新
    _log("[U] %s : %s" % (module_name, module), depth)

    # 记录update之前的原模块全部顶层对象
    old_module = {}
    for key, obj in module.__dict__.iteritems():
        # print "Old "+str(key)
        # if(str(key) == "Hello5"):
        #	print "Old Hello"
        old_module[key] = obj
        _log("[S] %s : %s" % (key, _S(obj)), depth)

    # 调用reload重新解释模块

    try:
        new_module = reload(module)
    except:
        # 正常的xupdate逻辑是：new_module必须引用旧的func（见第288行）, 替换的只是旧func里面的funccode
        # 但这里系统reload异常后，
        # 导致一部分或全部module的func已经替换成新的了。
        # 导致后续的reload，永远无法替换到最原始func的funccode

        print "reload failed. restore module attrs..."
        for key, oldobj in old_module.iteritems():
            module.__dict__[key] = oldobj  # 还原回去
        raise

        # print module.data.get(21201)
        # print new_module.data.get(21201)
        # print id(module.data)
        # print id(new_module.data)
    assert id(module) == id(new_module)

    new_dict = {}

    handlers = get_valid_handlers(is_update_data)
    for key, newobj in new_module.__dict__.iteritems():

        new_dict[key] = newobj

        # 如果新的key不在旧模块中，不处理即可(其实相当于添加新对象)
        if key not in old_module:
            _log("[A] %s : %s" % (key, _S(newobj)), depth)
            print "[reload-tip]add newobj:[%s]%s" % (key, newobj)
            continue
        oldobj = old_module[key]

        if id(oldobj) == id(newobj):  # 同一个对象就不用执行update了. by shadow, 比如import进来的东东
            continue

        # 如果key对象类型在新旧模块间不同，那留旧对象
        # 这里会跳过new style objects
        if type(newobj) != type(oldobj):
            if isinstance(newobj, types.TypeType) and isinstance(oldobj, types.TypeType):
                # 虽然类型不同，但是都是类定义，很有可能是类和Metaclass在同一个文件定义。还是给予handler， sd
                pass
            else:
                new_module.__dict__[key] = oldobj  # 特殊地，这里需要替换，因为reload后的module对象和reload前是同一个地址
                _log("[RD] %s : %s" % (key, _S(oldobj)), depth)
                print "[reload-warning]type(newobj) != type(oldobj), so to keep use oldobj. newobj:[%s]%s " % (
                key, newobj)
                print "newobj-type", type(newobj), "id(type(newobj)):", id(type(newobj))
                print "oldobj-type", type(oldobj), "id(type(oldobj)):", id(type(oldobj))
                continue

        # 更新当前支持更新的对象
        obj_type = type(newobj)
        handler = handlers.get(obj_type)

        if handler is None:
            # 处理使用了metaclass的类型,by shadow
            if isinstance(newobj, types.TypeType):  # 比如用了__metaclass__
                handler = _update_new_style_class

        if handler:
            _log("[U] %s : %s" % (key, _S(oldobj)), depth)
            handler(oldobj, newobj, depth + 1)
            new_module.__dict__[key] = oldobj
        else:  # 未支持的对象类型更新，复用旧对象, 一般都是数据类
            new_module.__dict__[key] = oldobj
            _log("[RC] %s : %s" % (key, _S(oldobj)), depth)
    # print "[reload-tip]no handler for newobj:[%s]%s, to use oldobj. " % (key, newobj)


    _call_module_func(module, "__after_update__")

    _call_module_func(module, "__onreload__", new_dict)

    return new_module
