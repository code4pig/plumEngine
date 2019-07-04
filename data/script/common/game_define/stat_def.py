# coding=utf8

from __future__ import unicode_literals

from script.common.db.class_obj import ClassObject, Integer, Primitive


class Stat(ClassObject):
    str = Integer(default=0, desc='힘')
    dex = Integer(default=0, desc='민첩')
    int = Integer(default=0, desc='지능')
    con = Integer(default=0, desc='체력')

    atk_speed = Integer(default=0, desc='공격속도')
    p_atk = Integer(default=0, desc='물리 공격력')
    m_atk = Integer(default=0, desc='마법 공격력')
    p_def = Integer(default=0, desc='물리 방어')
    res = Integer(default=0, desc='마법 저항')
    pen = Integer(default=0, desc='물리 관통')
    hp = Integer(default=0, desc='생명력')

    # 저항 관련 스텟은 전투력 계산에서 사용되지 않으니 일단 관리 목록에서는 제외하자.
    # attr_res = Dict(Integer(), desc='속성 저항. 지수화풍흑무.(e_res, w_res, f_res, a_res, d_res, n_res)')
    # cond_res = Dict(Integer(), desc='상태이상 저항(sstun_res 스턴 저항,sleep_res 수면 저항,petrify_res 석화 저항,...)')

    cri = Integer(default=0, desc='치명타')
    eva = Integer(default=0, desc='물리 회피')

    def iterkeys(self):
        for k, v in self.__class__.__dict__.iteritems():
            if issubclass(type(v), Primitive):
                yield k

    def iteritems(self):
        for k in self.iterkeys():
            yield k, getattr(self, k)

    def get(self, stat):
        if stat is not None:
            return getattr(self, stat)
        return None

    def add(self, stat, val):
        if stat is not None and val is not None:
            if hasattr(self, stat):
                setattr(self, stat, getattr(self, stat) + val)

    def add_all(self, stats):
        if stats is not None:
            self.atk_speed += stats.atk_speed if stats.atk_speed is not None else 0
            self.p_atk += stats.p_atk if stats.p_atk is not None else 0
            self.m_atk += stats.m_atk if stats.m_atk is not None else 0
            self.p_def += stats.p_def if stats.p_def is not None else 0
            self.res += stats.res if stats.res is not None else 0
            self.pen += stats.pen if stats.pen is not None else 0
            self.hp += stats.hp if stats.hp is not None else 0
            self.cri += stats.cri if stats.cri is not None else 0
            self.eva += stats.eva if stats.eva is not None else 0

    def __add__(self, other):
        result = Stat()

        for k in self.iterkeys():
            result.add(k, getattr(self, k, 0))

            if hasattr(other, k):
                result.add(k, getattr(other, k, 0))

        return result


class StatBox(object):
    def __init__(self):
        self.static_stat = dict()  # desc='컨텐츠별 추가 스탯(고정값). key: 컨텐츠명')
        self.percent_stat = dict()  # desc='컨텐츠별 추가 스탯(퍼센트 값). key: 컨텐츠명')

        # 마스터 데이터에서 컨텐츠명들을 얻어오는게 맞긴하나, 고정값이라서 하드 코딩함
        for o in ['normal', 'pvp', 'pve', 'clan']:
            self.static_stat[o] = Stat()
            self.percent_stat[o] = Stat()

    def add(self, stat, val, content='normal'):
        if stat is None or val is None:
            return

        target_dict = self.static_stat

        # 퍼센트 스탯의 경우 2017.6.28 현재 _percent로만 끝나기 때문에, 해당 문자로 구분하도록 함
        offset = stat.find('_percent')
        if offset != -1:
            target_dict = self.percent_stat
            stat = stat[:offset]

        if content == 'normal':
            for o in target_dict.values():
                o.add(stat, val)
        else:
            target_dict[content].add(stat, val)

    def add_multiplier(self, stat, val, content='normal'):
        if stat is None or val is None:
            return
        
        if content == 'normal':
            for o in self.percent_stat.values():
                o.add(stat, val)
        else:
            self.percent_stat[content].add(stat, val)

    def get_static_stat(self, content='normal'):
        return self.static_stat.get(content, Stat())

    def get_percent_stat(self, content='normal'):
        return self.percent_stat.get(content, Stat())

    def add_all(self, stat, stat_type='static'):
        if stat_type == 'static':
            for o in self.static_stat.values():
                o.add_all(stat)
        else:
            for o in self.percent_stat.values():
                o.add_all(stat)

