# -*- coding: utf-8 -*-
"""
@author: bbz
"""
import game


# class CTickCallWrapper(object):
#     def __init__(self, callback):
#         self.f = callback
#
#     def __call__(self, *args):
#         self.f(*args)


class TickObj(object):
    def __init__(self):
        self._tickList = set()

    def RegTick(self, callback, args, atime, cnt=-1):
        if callback not in self._tickList:
            self._tickList.add(callback)
        game.RegTick(callback, args, atime, cnt)

    def DelTick(self, callback):
        if callback in self._tickList:
            self._tickList.discard(callback)
        game.DelTick(callback)

    def DelAllTicks(self):
        for callback in self._tickList:
            game.DelTick(callback)
        self._tickList.clear()

    def GetTickCount(self):
        return len(self._tickList)


# class TickObjEx(TickObj):
#     def __init__(self):
#         TickObj.__init__(self)
#         self._commonTickCache = {}
#
#     def DelAllTicks(self):
#         TickObj.DelAllTicks(self)
#         self._commonTickCache.clear()
#
#     def RegCommonTick(self, callback, args, atime, cnt=-1):
#         callback_id = id(callback)
#         if callback_id in self._commonTickCache:
#             self.DelTick(self._commonTickCache[callback_id])
#             self._commonTickCache.pop(callback_id)
#
#         wrapperCall = CTickCallWrapper(callback)
#         self._commonTickCache[callback_id] = wrapperCall
#         self.RegTick(wrapperCall, args, atime, cnt)
