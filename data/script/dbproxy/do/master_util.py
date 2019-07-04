# coding=utf8

from __future__ import unicode_literals

import bisect

from script.common import exceptions as excp
from script.common.db.class_obj import ClassObject, String, Dict, Class
from script.common.db.database import db_game
from script.common.db.base_do import MasterDoBase


def new_master_do_class(
        row_type, prefix, db=db_game(),
        index_meta_func=lambda x: x.get_index_meta() if hasattr(x, 'get_index_meta') else None):
    """
    마스터 do 클래스를 생성한다

    :param row_type: 마스터의 row class.
    :param prefix: 시트 이름. MST_xxx
    :param db: 마스터가 존재하는 db 커넥션 오브젝트
    :param index_meta_func: index meta 를 조회하는 함수. None 일 경우 index 를 만들지 않는다.
    :return: 마스터 do 클래스
    """

    class DocType(ClassObject):
        version = String(desc='마스터 버전')
        items = Dict(Class(row_type), desc='마스터. row')

    class NewMasterDo(MasterDoBase):
        def __init__(self, context, sort_by=None):
            super(NewMasterDo, self).__init__(context)

            self.index = {}
            if index_meta_func:
                for v in self.doc.items.itervalues():
                    index_meta = index_meta_func(v)
                    if index_meta:
                        for index_name, index_columns in index_meta.iteritems():
                            # box_level: (COMMON, 10)
                            # box: (HIGH,)
                            if index_name not in self.index:
                                self.index[index_name] = {}
                            if index_columns not in self.index[index_name]:
                                self.index[index_name][index_columns] = []
                            self.index[index_name][index_columns].append(v)

            if sort_by:
                for sort_key in sort_by:
                    key = sort_by[sort_key]['key']
                    is_number = sort_by[sort_key].get('is_number', False)
                    is_reverse = sort_by[sort_key].get('is_reverse', False)

                    for index_columns in self.index[sort_key]:
                        self.index[sort_key][index_columns] = sorted(self.index[sort_key][index_columns],
                                         key=lambda x: self.__convert_getattr__(x, key, is_number), reverse=is_reverse)

            """
            {
                box:
                    {
                        COMMON: [row1, row2, row3, row4],
                        HIGH: [row1, row2]
                    },

                box_level:
                    {
                        COMMON, 10: [row1, row2],
                        COMMON, 20: [row3, row4],
                        HIGH, 10: [row5, row6]
                    },

                box_level_item:
                    {
                        COMMON, 10, Adena: [row1],
                        COMMON, 10, Bone: [row2],
                        COMMON, 20, Adena: [row3],
                        HIGH, 10, Adena: [row4]
                    }
            }
            """

            # self.index = {}
            # if pk_func:
            #     for k, v in self.doc.items.iteritems():
            #         pk = pk_func(v)
            #         if pk not in self.index:
            #             self.index[pk] = []
            #
            #         self.index[pk].append(v)

        def __convert_getattr__(self, object, name, is_number):
            value = getattr(object, name)
            return int(value) if is_number else value

        @classmethod
        def cls(cls):
            return DocType

        @classmethod
        def get_prefix(cls):
            return prefix

        @classmethod
        def get_db(cls):
            return db

        def get_item(self, key, raise_exception=False):
            result = self.doc.items.get(key)

            if result is None and raise_exception:
                raise excp.ExceptionMasterRowNotExist(key)

            return result

        def get_by_index(self, name, *index_columns):
            """
            지정된 이름의 인덱스로부터 지정한 키의(index_columns) row list 를 얻어온다
            :param name: 인덱스 이름
            :param index_columns: 키. (컬럼 리스트)
            :return: list(DocType): master row 의 리스트
            """
            try:
                return self.index[name][index_columns]
            except KeyError:
                raise excp.ExceptionIndexNotExist(name, *index_columns)

        def search_upper(self, left, index_name, *index_columns):
            """
            지정된 이름의 인덱스로부터 지정한 키(index columns)에 가까운 row 를 찾는다. index_columns 보다 크거나 같으면서 가장 작은 row.
            [2,5,7,10] 에서 6을 찾으면 7이 나온다.
            [2,5,7,7,10] 에서 7을 찾으면. if left 왼쪽 7 else 오른쪽 7 이 나온다
            [2,5,7,10] 에서 1을 찾으면 2가 나온다.
            [2,3,7,10] 에서 12를 찾으면 예외 발생
            :param left: 동일키가 존재할 경우, 해당 키의 left / right 선택
            :param index_name: 사용할 인덱스의 이름
            :param index_columns: 검색할 인덱스 키
            :return: 찾은 master row
            """
            if index_name not in self.index:
                raise excp.ExceptionIndexNotExist('search_uppder', index_name, *index_columns)

            key_table = sorted(self.index[index_name].keys())
            if not key_table:
                raise excp.ExceptionIndexNotExist('search_uppder', index_name, *index_columns)

            # if left:
            #     f = bisect.bisect_left
            # else:
            #     f = bisect.bisect_right

            pos = bisect.bisect_left(key_table, index_columns)
            if pos >= len(key_table):
                raise excp.ExceptionIndexNotExist('search_upper', index_name, *index_columns)
            else:
                rows = self.index[index_name][key_table[pos]]
                return rows[0] if left else rows[-1]

        def search_near(self, left, index_name, *index_columns):
            """
            지정된 이름의 인덱스로부터 지정한 키(index columns)에 가까운 row 를 찾는다.
            [2,5,7,10] 에서 6을 찾으면: 5 if left else 7
            [2,5,7,10] 에서 7을 찾으면. 7 이 나온다.
            [2,5,7,10] 에서 1을 찾으면 None 이 나온다
            :param left: 동일키가 존재할 경우, 해당 키의 left / right 선택
            :param index_name: 사용할 인덱스의 이름
            :param index_columns: 검색할 인덱스 키
            :return: 찾은 master row or None if 키가 제일 작은 값일 경우
            """
            if index_name not in self.index:
                raise excp.ExceptionIndexNotExist('search_lower', index_name, *index_columns)

            key_table = sorted(self.index[index_name].keys(), reverse=left)
            if not key_table:
                raise excp.ExceptionIndexNotExist('search_lower', index_name, *index_columns)

            # prev_row = None
            for key in key_table:
                if key <= index_columns:
                    return self.index[index_name][key]
            #     if key < index_columns:
            #         # right 검색인데 마지막 동일키가 있으면 해당 row 반환
            #         if not left and prev_row:
            #             return prev_row
            #         # left 이거나, right 여도 동일키가 없으면 현재 값 반환
            #         else:
            #             return self.index[index_name][key]
            #     elif key == index_columns:
            #         # left 검색이고 동일키일 경우 반환
            #         if left:
            #             return self.index[index_name][key]
            #         # right 검색이고 동일키일 경우, 다음 키도 동일키인지 살펴보도록 하고 현재 값은 저장해 둔다
            #         else:
            #             prev_row = self.index[index_name][key]
            #
            # # right 검색인데, 동일키가 index 의 마지막 엘리먼트일 경우 해당 row 반환
            # if prev_row:
            #     return prev_row

            # 키가 index 의 가장 작은 값보다 작을 경우
            return None

        def has_index(self, name, *index_columns):
            if index_columns in self.index[name]:
                return True

            return False

        def get_first_by_index(self, name, *index_columns):
            """
            지정된 이름의 인덱스로부터 지정한 키의(index_columns) 첫번째 row 를 얻어온다. 주로 unique index 일 경우 사용.
            :param name: 인덱스 이름
            :param index_columns: 키. (컬럼 리스트)
            :return: DocType: master row obj
            """
            return self.get_by_index(name, *index_columns)[0]

    return NewMasterDo
