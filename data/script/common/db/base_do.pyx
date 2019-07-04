# coding=utf8

from __future__ import unicode_literals

import abc

from script.common import exception_def as excp
from script.common.db.instant_box import instant_box

# class StrategyMakeDocumentKey(object):
#     def make_key(self, *args):
#         return '_'.join(unicode(elem) for elem in args)
#
#
# class StrategyMakeServerDependantDocumentKey(object):
#     def make_key(self, *args):
#         return '_'.join(unicode(elem) for elem in ([unicode(instant_box.server_selected)] + list(args)))


class BaseDo(object):
    __metaclass__ = abc.ABCMeta

    writer = True
    try_period = 0

    @classmethod
    def Reader(cls):
        class DoReader(cls):
            writer = False

            def __init__(self, *args, **kwargs):
                cls.__init__(self, *args, **kwargs)

            def must_lock(self):
                return False

            def update(self):
                raise excp.ExceptionReaderCannotWrite(repr(cls))

        return DoReader

    @classmethod
    def TryLock(cls, try_period_):
        """
        도큐먼트를 lock 할 때 실패하면, try_period 만큼 기다리면서 계속 lock 을 시도한다
        :param try_period: lock 잡길 기다리는 최대 시간. in milliseconds
        :return: cls
        """
        class TryLocker(cls):
            try_period = try_period_

            def __init__(self, *args, **kwargs):
                cls.__init__(self, *args, **kwargs)

        return TryLocker

    def __init__(self, context, *args):
        self._key = self.get_document_key(self.get_prefix(), *args)
        self._doc_cache_key = (True, self._key)  # (self.__class__.writer, self._key)
        self._doc = context.get_doc(self._doc_cache_key, self.cls(), self.get_db(), self._key, self.get_default_doc(),
                                    self.__class__.get_prefix(), self.__class__.get_ttl(), self.must_lock(),
                                    self.__class__.is_server_dependant(), self.__class__.writer,
                                    self.__class__.is_server_group_do(), self.get_server_dependant_id(),
                                    try_period=self.__class__.try_period)
        self.context = context

    @classmethod
    @abc.abstractmethod
    def cls(cls):
        """

        :rtype : type
        """
        pass

    @classmethod
    def get_prefix(cls):
        pass

    @classmethod
    @abc.abstractmethod
    def get_db(cls):
        pass

    def get_default_doc(self):
        return self.cls()()

    @classmethod
    def get_ttl(cls):
        return 0

    def set_ttl(self, ttl):
        self._doc.set_ttl(ttl)

    # @classmethod
    # def get_strategy_make_document_key(cls):
    #     return StrategyMakeServerDependantDocumentKey()

    # @classmethod
    # def _get_server_dependant_document_key(cls, *args):
    #     return '_'.join(unicode(elem) for elem in ([unicode(instant_box.server_selected)] + list(args)))
    #
    # @classmethod
    # def _get_server_independant_document_key(cls, *args):
    #     return '_'.join(unicode(elem) for elem in args)

    @classmethod
    def is_server_dependant(cls):
        return True

    @classmethod
    def is_server_group_do(cls):
        return False

    def get_server_dependant_id(self):
        return None

    def get_document_key(self, *args):
        if self.is_server_dependant():
            if self.is_server_group_do():
                return '_'.join(unicode(elem) for elem in ([unicode(instant_box.server_group)] + list(args)))
            else:
                server_id = self.get_server_dependant_id()
                return '_'.join(unicode(elem) for elem in
                                ([unicode(server_id if server_id else instant_box.server_selected)
                                  ] + list(args)))
        else:
            return '_'.join(unicode(elem) for elem in args)

    # get_document_key = _get_server_dependant_document_key

    # @staticmethod
    # def make_key(*args):
    #     return '_'.join(unicode(elem) for elem in args)
    #
    # def _make_key(*args):
    #     return '_'.join(unicode(elem) for elem in ([repr(instant_box.server_selected)] + args))

    def get_key(self):
        return self._key

    @property
    def is_new(self):
        return self._doc.is_new

    @property
    def doc(self):
        return self._doc.doc

    @doc.setter
    def doc(self, new):
        self._doc.doc = new
        self.update()

    def update(self):
        self._doc.update = True

    @property
    def updated(self):
        return self._doc.update

    def delete(self):
        self._doc.delete = True

    def save(self, ttl=None, force_reload=False):
        self._doc.save(ttl)
        if force_reload:
            self._doc.load(force_reload)

    def must_lock(self):
        return True

    @classmethod
    def get_schema_doc(cls, indent=0):
        """
        schema 문서를 자동 생성함

        :rtype : string
        """

        try:
            if cls.get_db():
                tab = '\t' * indent

                doc = '{0}bucket: {1}, {2} document: {3}\n'.format(tab, cls.get_db().bucket, tab, cls.get_prefix())

                if cls.cls():
                    doc += cls.cls().get_protocol_doc(indent=indent + 1)

                return doc + '\n'
            else:
                return ''
        except Exception as e:
            print e, cls.get_prefix()
            raise

    def get_doc_cache_key(self):
        return self._doc_cache_key


class ServerIndependantLockDoBase(BaseDo):
    __metaclass__ = abc.ABCMeta

    def __init__(self, context, *args):
        super(ServerIndependantLockDoBase, self).__init__(context, *args)

    def must_lock(self):
        return True

    @classmethod
    def is_server_dependant(cls):
        return False


class ServerIndependantUnlockDoBase(BaseDo):
    __metaclass__ = abc.ABCMeta

    def __init__(self, context, *args):
        super(ServerIndependantUnlockDoBase, self).__init__(context, *args)

    def must_lock(self):
        return False

    @classmethod
    def is_server_dependant(cls):
        return False


class MasterDoBase(BaseDo):
    __metaclass__ = abc.ABCMeta

    def __init__(self, context, *args):
        super(MasterDoBase, self).__init__(context, *args)

    def must_lock(self):
        return False

    @classmethod
    def is_server_dependant(cls):
        return False

        # get_document_key = BaseDo._get_server_independant_document_key


class UnlockedDoBase(BaseDo):
    __metaclass__ = abc.ABCMeta

    def __init__(self, context, *args):
        super(UnlockedDoBase, self).__init__(context, *args)

    def must_lock(self):
        return False

# class MasterDoBase(BaseDo):
#     __metaclass__ = abc.ABCMeta
#
#     def __init__(self, context, *args):
#         super(MasterDoBase, self).__init__(context, *args)
#
#     def must_lock(self):
#         return False
#
#     @classmethod
#     def get_strategy_make_document_key(cls):
#         return StrategyMakeDocumentKey()


# class ServerIndependantBase(BaseDo):
#     __metaclass__ = abc.ABCMeta
#
#     def __init__(self, context, *args):
#         super(ServerIndependantBase, self).__init__(context, *args)
#
#     def must_lock(self):
#         return True
