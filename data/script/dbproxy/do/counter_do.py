# coding=utf8

from __future__ import unicode_literals

import abc
import time

from couchbase.exceptions import NotFoundError
from script.common.db.instant_box import instant_box, RollbackCounterInfo


class Counter(object):
    __metaclass__ = abc.ABCMeta

    prefix = 'COUNTER'

    def __init__(self, *args):
        self._key = self.make_key(self.__class__.prefix, *args)

    def increase(self, amount=1, initial=0, ttl_period=None):
        """
        주의 사항
        1. ttl 이 기존 document 에 세팅된 그것 보다 짧을 경우. 무시됨
        2. amount == 0 인 경우. ttl 이 무시됨
        """
        ttl = self.__class__.get_ttl_time_t(ttl_period)

        if self.rollback_counter():
            instant_box.rollback_counter.append(RollbackCounterInfo(self.db(), self._key, True, amount, ttl_period))

        return self.db().incr(self._key, amount, initial=max(0, initial + amount), ttl=ttl).value

    def set(self, counter, ttl_period=None):
        delta = counter - self.get()
        self.increase(delta, ttl_period=ttl_period)

    @classmethod
    def rollback_counter(cls):
        return False

    @classmethod
    def get_ttl_time_t(cls, ttl_period):
        if ttl_period is None:
            if cls.get_ttl() == 0:
                return 0
            else:
                return int(time.time()) + cls.get_ttl()
        elif ttl_period == 0:
            return 0
        else:
            return int(time.time()) + ttl_period

    def get(self):
        try:
            return self.db().get(self._key).value
        except NotFoundError:
            return 0

    @abc.abstractmethod
    def db(self):
        pass

    @classmethod
    def get_ttl(cls):
        return 0

    def make_key(self, *args):
        return '_'.join(unicode(elem) for elem in args)


class ServerCounter(Counter):
    @abc.abstractmethod
    def db(self):
        pass

    def get_server_dependant_id(self):
        return None

    @classmethod
    def is_server_group_do(cls):
        return True

    def make_key(self, *args):
        server_id = self.get_server_dependant_id()
        if server_id:
            return '_'.join(unicode(elem) for elem in ([unicode(server_id)] + list(args)))
        else:
            if self.is_server_group_do():
                return '_'.join(unicode(elem) for elem in ([unicode(instant_box.server_group)] + list(args)))
            else:
                return '_'.join(unicode(elem) for elem in ([unicode(instant_box.server_selected)] + list(args)))
