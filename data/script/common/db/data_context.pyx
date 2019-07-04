# coding=utf8

from __future__ import unicode_literals

import abc

import time
from couchbase.exceptions import NotFoundError, TemporaryFailError
from script.common import exception_def as excp
from script.common.db.class_obj import ClassObject
from script.common.db.instant_box import instant_box


class Document(object):
    """
    카우치베이스 도큐먼트 class. 단일 도큐먼트에 대응.
    load, save 등의 기능을 담당
    """

    def __init__(self, cls, db, key, default_doc, doc_type, ttl, must_lock, is_server_dependant, writer,
                 is_server_group_do, get_server_dependant_id, try_period, lock_ttl_timestamp):
        """
        :param cls: 도큐먼트를 다루는 do class
        :param db: couchbase db object
        :param key: docid
        :param default_doc: db 에 데이터가 없을 시 사용하는 기본 도큐먼트 정보
        :param doc_type: 도큐먼트 타입에 대한 prefix = table name
        :param ttl: 기본 ttl
        :param must_lock: load 시 lock 을 걸어야 하는지 여부
        """
        self.cls = cls
        self._db = db
        self.key = key
        self.update = False  # 데이터 갱신이 있었는 지 여부. save 시 실제로 db 에 저장할 지 여부를 결정
        self.default_doc = default_doc
        self.doc_type = doc_type
        self.ttl = ttl
        self.must_lock = must_lock
        self.is_server_dependant = is_server_dependant
        self.is_server_group_do = is_server_group_do
        self.get_server_dependant_id = get_server_dependant_id
        self.writer = writer
        self.delete = False  # 데이터 삭제할 지 여부. save 시 db 에서 삭제할 지 여부를 결정
        self.try_period = try_period / 1000.0  # make milliseconds
        self._lock_ttl_timestamp = lock_ttl_timestamp  # ttl timestamp for locking documents

        self.doc = None  # document obj. dict or do or str
        self.cas = None  # couchbase cas
        self._is_new = True
        self._stored = False
        # self.is_new = True  # 이 도큐먼트가 save 된 적이 있는지 여부. True 일 경우, 아직 정상 create 과정을 거치지 않은 상태임 = default doc

    def save(self, ttl=None):
        """
        도큐먼트를 저장한다. cas 가 일치하지 않을 경우 실패한다.
        self.update == True: db 에 set 한다. False 이면 변경사항이 없다고 보고 set 하지 않는다.
        self.delete == True: document 를 delete 한다.

        :param ttl: 이번에만 사용할 임시 ttl 을 지정한다.
        """
        if ttl is None:
            ttl = self.ttl

        try:
            if self.delete:
                try:

                    if self.must_lock:
                        self.unlock()

                    self._db.delete(self.key)
                    self._stored = True
                except NotFoundError as e:
                    print '[WARN] delete fail. not found.', self.key, e
            elif self.update:
                doc = self.get_doc_for_save(False)
                self._db.set(self.key, doc, cas=self.cas, ttl=ttl)
                self._stored = True
        except Exception as e:
            # print 'error key :{0}, t :{1}'.format(self.key, time.time())
            raise excp.ExceptionFailToSave(e, self.key)

        self.update = False

    def get_doc_for_save(self, is_new):
        """
        db 에 저장 가능한 문서 데이터를 구한다. str -> str, dict/ClassObject -> dict 로 변환.

        :param is_new: 새로 생성된 기본 도큐먼트 여부.
        :return: str | dict
        """
        if issubclass(self.cls, dict):
            doc = self.doc
            doc['doc_type'] = self.doc_type
            if self.must_lock:
                doc['is_new'] = is_new
            if self.get_server_dependant_id:
                doc['server_d'] = self.get_server_dependant_id
            else:
                doc['server_d'] = instant_box.server_selected
            doc['server_g'] = instant_box.server_group
        elif issubclass(self.cls, str):
            doc = self.doc
        else:
            doc = self.doc.dump(for_save=True)
            doc['doc_type'] = self.doc_type
            if self.must_lock:
                doc['is_new'] = is_new
            if self.get_server_dependant_id:
                doc['server_d'] = self.get_server_dependant_id
            else:
                doc['server_d'] = instant_box.server_selected
            doc['server_g'] = instant_box.server_group

        return doc

    def get_lock_ttl_timestamp(self):
        lock_ttl_period = 10

        if instant_box.ignore_database_timeout:
            lock_ttl_period = 30

        if not self._lock_ttl_timestamp:
            # if current time = 0:0:0.5 then ttl = 0:0:11.0  # ttl must be int
            self._lock_ttl_timestamp = int(time.time() + lock_ttl_period + 1)

        return self._lock_ttl_timestamp

    def get_lock_ttl(self):
        # if current time = 0:0:0.4 and ttl = 0:0:5.5 then ttl = 6 (5.1 => 6)
        time_current = time.time()
        lock_ttl_timestamp = self.get_lock_ttl_timestamp()
        ttl = int(lock_ttl_timestamp - time_current + 1)
        if ttl < 1 and not instant_box.ignore_database_timeout:
            raise excp.ExceptionDatabaseLockTimeout(time_current, lock_ttl_timestamp)
        return ttl

    def load(self, force=False):
        """
        도큐먼트를 읽어온다. 이미 읽어온 문서가 있을 경우, 생략한다.

        :param force: 이미 읽어온 문서가 있어도 강제로 다시 가져온다. 읽어온 후 update 한 정보가 사라지니 유의!
        """
        if force or not self.doc:
            try:
                if self.must_lock:
                    result = None
                    if self.try_period > 0:
                        start = time.time()
                        while time.time() - start < self.try_period and result is None:
                            try:
                                result = self._db.lock(self.key, ttl=self.get_lock_ttl())
                            except TemporaryFailError:
                                time.sleep(0.001)
                    if result is None:
                        result = self._db.lock(self.key, ttl=self.get_lock_ttl())
                else:
                    result = self._db.get(self.key)

                if issubclass(self.cls, ClassObject):
                    self.doc = self.cls.new_from_data(result.value)
                    self._is_new = result.value.get('is_new', False)
                else:
                    self.doc = result.value
                    self._is_new = False

                if self.must_lock:
                    self.cas = result.cas
                else:
                    self.cas = 0
            except NotFoundError:
                self.doc = self.default_doc
                self._is_new = True
                # if issubclass(self.cls, ClassObject):
                #     self.doc.is_new = True

                if self.must_lock:
                    # 데이터가 없을 경우, 신규로 add 한다. is_new 를 True 로 설정
                    self._db.add(self.key, self.get_doc_for_save(True), ttl=self.get_lock_ttl())
                    # print 'add key :{0}, t :{1}, ttl :{2}'.format(self.key, time.time(), self.get_lock_ttl())
                    result = self._db.lock(self.key, ttl=self.get_lock_ttl())
                    self.cas = result.cas
                else:
                    self.cas = 0
            except TemporaryFailError as e:
                print '[WARN] lock fail.', self.key, e
                raise excp.ExceptionLockDocumentFail(self.key, e)

    def unlock(self):
        try:
            if issubclass(self.cls, ClassObject):
                if self.must_lock and not self._stored:
                    self._db.unlock(self.key, self.cas)
                    if self._is_new:
                        self._db.delete(self.key)
        except Exception as e:
            pass
            # print '[WARN] document unlock failed.', self.cas, e

    @property
    def is_new(self):
        """
        이 도큐먼트가 새로 생성된 기본 문서인지 여부. 수정 후 저장하면 False 가 된다.
        :return:
        """
        try:
            return self._is_new
        except Exception:
            return False
            # return self.doc.is_new is True if issubclass(self.cls, ClassObject) else False

    def set_ttl(self, ttl):
        self.ttl = ttl

        self.update = True


class DataContext(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self._document = {}  # data objects, {doc_key: document, doc_key: document, ...}

        self._lock_ttl_timestamp = 0  # ttl timestamp for locking documents

    def save(self):
        """
        데이터가 변경된 모든 도큐먼트를 db 에 실제 저장한다.
        """
        time_current = time.time()
        if self._lock_ttl_timestamp > 0 and time_current > self._lock_ttl_timestamp - 1.5 and\
                not instant_box.ignore_database_timeout:
            raise excp.ExceptionDatabaseLockTimeout(time_current, self._lock_ttl_timestamp)

        for doc_cache_key, doc in self._document.iteritems():
            if doc_cache_key[0]:  # writer 인 경우에만 save
                doc.save()
                doc.unlock()

        self._lock_ttl_timestamp = 0

    def unlock(self):
        for doc_cache_key, doc in self._document.iteritems():
            if doc_cache_key[0]:  # writer 인 경우에만 unlock
                doc.unlock()

    def load(self, force=False):
        """

        :param force:
        """
        for doc in self._document.itervalues():
            doc.load(force)

    # modify by Yoray, JoyGames, ALPHA GROUP CO.,LTD, at 2017-12-02
    # detail: 新增reload接口
    # >>>>>>>>>>>>>
    def reload(self, doc_key=None):
        if doc_key is None:
            self.load(True)
        else:
            if doc_key in self._document:
                document = self._document[doc_key]
                document.load(True)
    # <<<<<<<<<<<<<

    def get_doc(self, doc_cache_key, cls, db, key, default_doc, doc_type, ttl, must_lock, is_server_dependant,
                writer, is_server_group_do=False, get_server_dependant_id=None, try_period=0):
        if doc_cache_key not in self._document:
            new_doc = Document(cls, db, key, default_doc, doc_type, ttl, must_lock, is_server_dependant, writer,
                               is_server_group_do, get_server_dependant_id, try_period, self._lock_ttl_timestamp)
            new_doc.load()
            self._lock_ttl_timestamp = new_doc.get_lock_ttl_timestamp()
            self._document[doc_cache_key] = new_doc
            return new_doc
        else:
            document = self._document[doc_cache_key]
            if not document.must_lock and must_lock:
                document.must_lock = must_lock
                document.writer = writer
                document.load(True)
                self._lock_ttl_timestamp = document.get_lock_ttl_timestamp()

            return document
