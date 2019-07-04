# coding=utf8

from __future__ import unicode_literals

from script.common.db.class_obj import ClassObject, Integer, Dict, Class


class MasteryGroup(ClassObject):
    mastery_list = Dict(Integer(), desc='마스터리 목록. key: star_group, value: 레벨')
    used_point = Integer(default=0, desc='마스터리 레벨에 사용된 총 포인트')


class MasteryInfo(ClassObject):
    mastery_group_list = Dict(Class(MasteryGroup), desc='마스터리 목록')
    reset_count = Integer(default=0, desc='초기화한 횟수')