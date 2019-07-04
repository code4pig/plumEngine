# coding=utf8

from __future__ import unicode_literals

import copy

import script.common.exception_def as excp


class DataObject(object):
    pass


class ParserObject(object):
    @classmethod
    def default_value(cls):
        return None

    def __init__(self, required=False, default=None, desc=None):
        self.required = required
        self.default = default
        self.desc = desc

    def get_protocol_doc(self, indent=0, continue_line=False):
        tab = '\n' + '\t' * indent
        return '{0}{1}, required={2}, default={3}, {4}'.format(
            '' if continue_line else tab, self.get_protocol_name(), self.required, self.default, self.desc)

    def get_protocol_name(self):
        return self.__class__.__name__


class ComplexParserObject(ParserObject):
    def __init__(self, parser_type, required=False, default=None, desc=None):
        super(ComplexParserObject, self).__init__(required=required, default=default, desc=desc)

        self.parser_type = parser_type

    def get_protocol_doc(self, indent=0, continue_line=False):
        tab = '\n' + '\t' * indent

        doc = ''
        if continue_line:
            doc = '{0}{1} - {2}, required={3}, default={4}, {5}'.format(
                '' if continue_line else tab, self.__class__.__name__,
                self.parser_type.get_protocol_name() if self.parser_type else '', self.required, self.default,
                self.desc)
        if issubclass(self.parser_type.__class__, ComplexParserObject):
            doc += self.parser_type.get_protocol_doc(indent, False)

        return doc


class Primitive(ParserObject):
    def __init__(self, required=False, default=None, desc=None):
        super(Primitive, self).__init__(required, default, desc)

    @staticmethod
    def to_obj(data):
        return data

    @staticmethod
    def to_data(obj, exclude_null=False):
        return obj


class Number(Primitive):
    pass


class Float(Primitive):
    pass


class Integer(Primitive):
    pass


class String(Primitive):
    pass


class Boolean(Primitive):
    pass


class Dict(ComplexParserObject):
    @classmethod
    def default_value(cls):
        return {}

    def __init__(self, parser_type=None, required=False, default=None, desc=None):
        super(Dict, self).__init__(parser_type, required, default, desc)

    def to_obj(self, data):
        if data is None:
            return {}

        if self.parser_type:
            # value 의 타입이 지정되었으면, 해당 타입으로 변환 처리한다
            result = {}
            for k, v in data.iteritems():
                result[k] = self.parser_type.to_obj(v)
            return result
        else:
            # value 의 타입이 지정되지 않았으면, 변환 없이 원본 딕셔너리를 반환한다. value 의 원래 타입을 보존한다.
            return data

    def to_data(self, obj, exclude_null=False):
        # object 가 None 이면 널 딕셔너리를 반환
        if obj is None:
            return {}

        if self.parser_type:
            # value 의 타입이 지정되지 않았으면, 변환 없이 원본 딕셔너리를 반환한다.
            result = {}
            for k, v in obj.iteritems():
                if not (exclude_null and v is None):
                    result[k] = self.parser_type.to_data(v)

            return result
        else:
            # value 의 타입이 지정되지 않았으면, 변환 없이 원본 딕셔너리를 반환한다. value 의 원래 타입을 보존한다.
            return obj

    def load_from(self, data, obj):
        if data is None:
            return

        if not self.parser_type:
            obj.clear()
            obj.update(data)

        for k, v in data.iteritems():
            obj[k] = self.parser_type.to_obj(v)

    @staticmethod
    def load_from_obj(data, obj):
        obj.clear()
        obj.update(data)


class Class(ComplexParserObject):
    def __init__(self, cls, required=False, default=None, desc=None):
        super(Class, self).__init__(None, required, default, desc)

        self.cls = cls

    def to_obj(self, data):
        # 데이터가 없으면 None 반환
        if not data:
            return None

        # ClassObject 생성
        result = self.cls()

        # ClassObject 에 데이터를 대입한다.
        _class = self.cls
        while _class is not ClassObject:
            for var_name, value in _class.__dict__.iteritems():
                if issubclass(type(value), ParserObject):
                    try:
                        if value.required and var_name not in data:
                            raise excp.ExceptionRequiredColumnNotExist(var_name)

                        setattr(result, var_name, value.to_obj(data.get(var_name, value.default)))
                    except Exception as e:
                        raise excp.ExceptionClassObjectParseError(self.__class__, self.cls, var_name, value, e)

            _class = _class.__base__

        result.on_post_load()

        return result

    def to_data(self, obj, exclude_null=False, for_save=False):
        if not obj:
            return None

        result = {}
        obj.on_pre_dump(result, for_save)
        for meta_var in dir(self.cls):
            meta_obj = getattr(self.cls, meta_var)
            if issubclass(type(meta_obj), ParserObject):
                try:
                    v = meta_obj.to_data(getattr(obj, meta_var))
                    if not (exclude_null and v is None):
                        result[meta_var] = v
                except AttributeError as e:
                    raise excp.ExceptionClassObjectParseError(self.__class__, self.cls, meta_var, meta_obj, e)
        return result

    def load_from(self, data, obj):
        if not data:
            return

        for meta_var in dir(self.cls):
            meta_obj = getattr(self.cls, meta_var)
            try:
                if issubclass(type(meta_obj), ParserObject):
                    if meta_var in data:
                        value = data[meta_var]
                    else:
                        if not meta_obj.required:
                            value = meta_obj.default
                        else:
                            raise excp.ExceptionRequiredColumnNotExist(meta_var)
                    if issubclass(type(meta_obj), ComplexParserObject):
                        meta_obj.load_from(value, getattr(obj, meta_var))
                    else:
                        setattr(obj, meta_var, value)
            except Exception as e:
                raise excp.ExceptionClassObjectParseError(self.__class__, self.cls, meta_var, meta_obj, e)

        obj.on_post_load()

    def load_from_obj(self, data, obj):
        if not data:
            return

        for meta_var in dir(self.cls):
            meta_obj = getattr(self.cls, meta_var)
            if issubclass(type(meta_obj), ParserObject):
                try:
                    setattr(obj, meta_var, getattr(data, meta_var))
                except AttributeError as e:
                    if not meta_obj.required:
                        setattr(obj, meta_var, meta_obj.default)
                    else:
                        raise excp.ExceptionRequiredColumnNotExist(self.__class__, self.cls, meta_var, meta_obj, e)

        obj.on_post_load()

    def get_protocol_doc(self, indent=0, continue_line=False):
        """

        :param indent: int
        :return: str
        """
        tab = '\n' + '\t' * indent
        doc = ''
        if continue_line:
            doc += '{0}{1} - {2}, required={3}, default={4}, {5}'.format(
                '' if continue_line else tab, self.__class__.__name__,
                self.cls.__name__, self.required, self.default, self.desc)
        doc += self.cls.get_protocol_doc(indent, False)

        return doc

    def get_protocol_name(self):
        return '{0}({1})'.format(self.__class__.__name__, self.cls.__name__)


class ClassObject(DataObject):
    """
    dict to class, class to dict 를 지원. 문서화 지원. 프로토콜 및 data object 의 베이스 클래스로 사용됨.
    """

    def __init__(self, **kwargs):
        # ClassObject 가 가진 멤버ParserObject)에 대해 기본 값 대입
        _class = self.__class__
        while _class is not ClassObject:
            for var_name, value in _class.__dict__.iteritems():
                # if issubclass(type(value), ParserObject):
                #     if value.default is None:
                #         setattr(self, var_name, value.__class__.default_value())
                #     else:
                #         setattr(self, var_name, value.default)
                try:
                    if value.default is None:
                        setattr(self, var_name, value.__class__.default_value())
                    else:
                        setattr(self, var_name, value.default)
                except Exception as e:
                    pass

            _class = _class.__base__

        # 파라미터로 받은 값을 대입
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    @classmethod
    def new_from_data(cls, data):
        if data:
            return Class(cls).to_obj(data)
        else:
            return cls()

    def load(self, data):
        Class(self.__class__).load_from(data, self)

        return self

    def load_from_obj(self, obj):
        Class(self.__class__).load_from_obj(obj, self)

        return self

    def dump(self, exclude_null=False, for_save=False):
        return Class(self.__class__).to_data(self, exclude_null, for_save)

    def on_post_load(self):
        """
        오브젝트가 데이터(dict)로 부터 load 한 뒤 호출 된다.
        데이터가 로드 되고 후처리 하고 싶은 일이 있을 때 override 한다.
        """
        pass

    def on_pre_dump(self, dumped, for_save):
        pass

    @classmethod
    def get_protocol_doc(cls, indent=0, continue_line=False):
        """

        :param indent: int
        :return: str
        """
        tab = '\n' + '\t' * indent
        doc = ''

        for attr_name in dir(cls):
            attr_value = getattr(cls, attr_name)
            if issubclass(type(attr_value), ParserObject):
                doc += '{0}{1}: {2}'.format(
                    '' if continue_line else tab, attr_name, attr_value.get_protocol_doc(indent + 1, True))

        return doc


class List(ComplexParserObject):
    @classmethod
    def default_value(cls):
        return []

    def __init__(self, parser_type=None, required=False, default=None, desc=None):
        super(List, self).__init__(parser_type, required, default, desc)
        self.parser_type = parser_type

    def to_obj(self, data):
        if data is None:
            return []

        if not self.parser_type:
            return data

        result = []
        for each in data:
            result.append(self.parser_type.to_obj(each))
        return result

    def load_from(self, data, obj):
        if data is None:
            return

        if not self.parser_type:
            obj[:] = data

        for each in data:
            obj.append(self.parser_type.to_obj(each))

    @staticmethod
    def load_from_obj(data, obj):
        obj[:] = data

    def to_data(self, obj, exclude_null=False):
        if not self.parser_type:
            return obj

        if obj is None:
            return []

        result = []
        for each in obj:
            result.append(self.parser_type.to_data(each))
        return result


if __name__ == '__main__':
    class B(ClassObject):
        b1 = Number()
        b2 = Number()

    class C(ClassObject):
        c1 = Number()
        c2 = Number()

    class A(ClassObject):
        a1 = Number()
        a2 = String()
        b = Class(B)
        c = List(Class(C))
        d = List(List(Class(B)))
        e = Dict(Class(B))
        f = Dict(Dict(Class(B)))
        g = Dict()
        h = List()
        i = List(Number())
        j = Dict(Number())
        k = List(Dict(Number()))
        l = Dict(List(Number()))

    class Z(ClassObject):
        a = Class(A)

    dd = {
        'a': {
            'a1': 1,
            'a2': "haha",
            'b': {
                'b1': 1,
                'b2': 2
            },
            'c': [
                {
                    'c1': 1,
                    'c2': 2
                },
                {
                    'c1': 2,
                    'c2': 3
                }
            ],
            'd': [
                [{'b1': 1, 'b2': 2}, {'b1': 4, 'b2': 5}],
                [{'b1': 3, 'b2': 4}]
            ],
            'e': {
                '123': {'b1': 3, 'b2': 5},
                '124': {'b1': 6, 'b2': 7}
            },
            'f': {
                '1234': {
                    'abcd': {'b1': 3, 'b2': 5},
                    'efgh': {'b1': 3, 'b2': 5}
                },
                '5678': {
                    'hijk': {'b1': 3, 'b2': 5},
                    'lmno': {'b1': 3, 'b2': 5}
                }
            },
            'g': {
                '345': 4,
                '567': 5
            },
            'h': [1, 'haha'],
            'i': ['a', 'b', 'c'],
            'j': {'123': 1, '456': 2},
            'k': [{'123': 1, '456': 2}, {'678': 4}],
            'l': {'123': [1, 2, 3], '456': [4, 5, 6]}
        }
    }

