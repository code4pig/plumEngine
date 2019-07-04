# -*- coding: utf8 -*-
import types


class Const:
    class ConstError(TypeError): pass

    def __setattr__(self, name, value):
        if self.__dict__.has_key(name):
            raise self.ConstError, "Can't rebind const(%s)" % name
        self.__dict__[name] = value

    def has_value(self, value):
        return value in self.__dict__.values()


# 枚举接口
class IEnum(object):
    def __init__(self):
        self._finish = False
        self._enumvks = {}  # value->key
        self._enumkvs = {}  # key->value
        self._defaultv = None  # 默认枚举值
        self._enum_value_list = []

    def GetValueList(self):
        return self._enum_value_list

    def End(self):
        self._finish = True

    def GetEnumCount(self):
        return len(self._enumkvs)

    def IterEnumValues(self):
        return self._enumkvs.itervalues()

    def EnumValues(self):
        return self._enumkvs.values()

    def GetValueKeys(self):
        return self._enumvks.items()

    def GetEnumKey(self, value):
        return self._enumvks.get(value)

    def IsValidValue(self, v):
        return self._enumvks.has_key(v)

    def GetEnumValue(self, key):
        return self._enumkvs.get(key)

    def SetDefaultValue(self, v):
        if self.GetEnumKey(v) is None:
            print "设置默认枚举值错误！无效的枚举值.", v
            raise Exception("设置默认枚举值错误！无效的枚举值.")
            return
        self._defaultv = v

        # 传入一个枚举值， 如果没有对应的key，则给予默认值值

    def CorrectEnumValue(self, v):
        if self.GetEnumKey(v) is None:
            if self._defaultv is None:
                raise Exception("获取校对枚举值错误！未设定默认值!")
                return
            return self._defaultv
        return v

    def _DoEnum(self, name, value):
        # 避免key重复
        if self.__dict__.has_key(name):
            raise Exception("Can't redefine enum key(%s)" % name)
            return

            # 避免值重复
        if self._enumvks.has_key(value):
            raise Exception("Can't redefine enum value(%s)" % value)
            return

        self.__dict__[name] = value
        self._enumkvs[name] = value
        self._enumvks[value] = name
        self._enum_value_list.append(value)

    def __getattr__(self, name):
        if self._finish or name[0:1] == "_":
            raise Exception("enum obj has no key:%s" % name)
            return None

        self._DoEnum(name)

        if self.__dict__.has_key(name):
            return self.__dict__[name]
        else:
            # 反序列化的
            raise AttributeError("%s instance has no attribute:%s" % (self.__class__, name))
            return None

    def __setattr__(self, name, value):
        if name[0:1] == "_":
            object.__setattr__(self, name, value)
            return

        if self._finish == True:
            raise Exception("Can't define enum key(%s).  status is ended" % name)
            return

        self._DoEnum(name, value)


# 自定义枚举类型
class Enum(IEnum):
    """
    用法举例：
    codes = Enum()
    codes.SUCC  #0
    codes.FAIL  #1
    codes.ERROR #2
    codes.OK = 100  #100
    codes.OTHER	  #101
    ....
    codes.End()#结束. 防止继续非法枚举。 不调用这个一般问题也不大。
    """

    def __init__(self):
        IEnum.__init__(self)
        self._id = 0

    def _DoEnum(self, name, value=None):
        if value is None:
            value = self._id

            # 必须是int类型
        if not isinstance(value, types.IntType):
            raise Exception("enum value should be int. got invalid type: ", type(value))
            return

        super(Enum, self)._DoEnum(name, value)

        self._id = value + 1


# 字符串枚举。
"""
	用法举例：
	codes = StrEnum()
	codes.SUCC  #"SUCC"
	codes.FAIL  #"FAIL"
	codes.ERROR #"ERROR"
	codes.OK = "okok" #"okok"
"""


class StrEnum(IEnum):
    def __init__(self):
        IEnum.__init__(self)

    def _DoEnum(self, name, value=None):
        if value is None:
            value = name

            # 必须是string类型
        if not isinstance(value, types.StringType):
            raise Exception("strenum value should be string. got invalid type: ", type(value))
            return

        super(StrEnum, self)._DoEnum(name, value)
