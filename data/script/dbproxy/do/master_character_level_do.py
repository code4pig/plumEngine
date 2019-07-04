# coding=utf8

from __future__ import unicode_literals

from script.common.db.class_obj import Class, Dict, String, ClassObject, Integer
from script.common.db.database import db_game
from script.common.db.base_do import MasterDoBase


class MasterCharacterLevelRow(ClassObject):
    key = String(desc='레벨')
    exp = Integer(desc='경험치')


class MasterCharacterLevel(ClassObject):
    version = String(desc='마스터 버전.')
    items = Dict(Class(MasterCharacterLevelRow), desc='MasterCharacterLevel row')


class MasterCharacterLevelDo(MasterDoBase):
    def __init__(self, context):
        super(MasterCharacterLevelDo, self).__init__(context)

        # 레벨 순서대로 정렬. [(1 레벨, 경험치 100), (2 레벨, 경험치 200), ...]
        self.leveling = [(int(level), row.exp) for level, row in self.doc.items.iteritems()]
        self.leveling.sort()

    @classmethod
    def cls(cls):
        return MasterCharacterLevel

    # @classmethod
    # def get_prefix(cls):
    #     return 'MST_BehaviorsBase'

    @classmethod
    def get_db(cls):
        return db_game()

    def get_level(self, new_exp):
        for level, exp in self.leveling:
            if new_exp < exp:
                return level

    def get_exp(self, level_key):
        return self.doc.items[level_key].exp

    def get_max_exp(self):
        return self.leveling[-1][1] - 1

    def get_max_exp_of_level(self, level):
        return self.doc.items[str(level)].exp - 1


class MasterHeroLevelDo(MasterCharacterLevelDo):
    def __init__(self, context):
        super(MasterHeroLevelDo, self).__init__(context)

    @classmethod
    def get_prefix(cls):
        return 'MST_HeroLevel'


class MasterPetLevelDo(MasterCharacterLevelDo):
    def __init__(self, context):
        super(MasterPetLevelDo, self).__init__(context)

    @classmethod
    def get_prefix(cls):
        return 'MST_PetLevel'
