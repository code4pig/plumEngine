# -*- coding: utf8 -*-
# 单件的元类

"""
    用法:
        class MyClass(object):
            __metaclass__ = Singleton		# 子类也将是单件

            ...

    测试:
        t1 = MyClass()
        t2 = MyClass()

        print t1 is t2 	# True
"""


class Singleton(type):

    def __init__(self, name, bases, dic):
        """类被创建的时候调用"""
        super(Singleton, self).__init__(name, bases, dic)
        self.instance = None

    def __call__(self, *args, **kwargs):
        """类创建实例的时候调用"""
        if self.instance is None:
            if getattr(self, "__is_creating__", None):
                raise Exception("创建单键的过程中，循环调用回自己。 请查看traceback. 杜绝此类操作！")

            setattr(self, "__is_creating__", True)
            ins = super(Singleton, self).__call__(*args, **kwargs)
            self.instance = ins
            delattr(self, "__is_creating__")

        return self.instance
