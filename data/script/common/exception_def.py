# -*- coding:utf-8 -*-

from __future__ import unicode_literals
import sys
import traceback

__author__ = 'Yoray'


class ExceptionBase(Exception):
    code = 1


class ExceptionSuccess(ExceptionBase):
    code = 0


# 基础模块相关
class ExceptionEngineBase(ExceptionBase):
    code = 1


class ExceptionRequiredColumnNotExist(ExceptionBase):
    code = ExceptionEngineBase.code + 1


class ExceptionClassObjectParseError(ExceptionBase):
    code = ExceptionEngineBase.code + 2


class ExceptionLockDocumentFail(ExceptionBase):
    code = ExceptionEngineBase.code + 3


class ExceptionReaderCannotWrite(ExceptionBase):
    code = ExceptionEngineBase.code + 4


class ExceptionUnknown(ExceptionBase):
    code = ExceptionEngineBase.code + 5


class ExceptionFailToSave(ExceptionBase):
    code = ExceptionEngineBase.code + 6


# 通用业务相关
class ExceptionCommonBase(ExceptionBase):
    code = 1000


class ExceptionCheckLoginFailed(ExceptionBase):
    code = ExceptionCommonBase.code + 1


class ExceptionInvalidParameter(ExceptionBase):
    code = ExceptionCommonBase.code + 2


class ExceptionClanIdIsNone(ExceptionBase):
    # 没有公会
    code = ExceptionCommonBase.code + 100


# 聊天相关
class ExceptionChatBase(ExceptionBase):
    code = 2000


class ExceptionConnectNotFound(ExceptionBase):
    # connect不在connect字典中
    code = ExceptionChatBase.code + 1


class ExceptionConnectHasBind(ExceptionBase):
    # connect已绑定用户
    code = ExceptionChatBase.code + 3


class ExceptionUserHasBind(ExceptionBase):
    # 用户已绑定connect
    code = ExceptionChatBase.code + 4


class ExceptionAuthFail(ExceptionBase):
    # 验证失败
    code = ExceptionChatBase.code + 5


class ExceptionNeedLogin(ExceptionBase):
    # 需要先登录
    code = ExceptionChatBase.code + 6


class ExceptionUserServerNone(ExceptionBase):
    # 用户服务器为空
    code = ExceptionChatBase.code + 7


class ExceptionClanNotFound(ExceptionBase):
    # 找不到血盟
    code = ExceptionChatBase.code + 8


class ExceptionUserNotFound(ExceptionBase):
    # 找不到玩家
    code = ExceptionChatBase.code + 9


class ExceptionReceiverMsgFull(ExceptionBase):
    # 接收者消息邮箱已满
    code = ExceptionChatBase.code + 10


# 队伍相关
class ExceptionTeamBase(ExceptionBase):
    code = 3000


class ExceptionAlreadyHasTeam(ExceptionBase):
    code = ExceptionTeamBase.code + 1


class ExceptionLvNotEnough(ExceptionBase):
    code = ExceptionTeamBase.code + 2


class ExceptionCreateTeamFail(ExceptionBase):
    code = ExceptionTeamBase.code + 3


class ExceptionTeamCondiParam(ExceptionBase):
    code = ExceptionTeamBase.code + 4


class ExceptionHasNoTeam(ExceptionBase):
    code = ExceptionTeamBase.code + 5


class ExceptionNotTeamLeader(ExceptionBase):
    code = ExceptionTeamBase.code + 6


class ExceptionUserNotOnline(ExceptionBase):
    code = ExceptionTeamBase.code + 7


class ExceptionTeamNotExist(ExceptionBase):
    code = ExceptionTeamBase.code + 8


class ExceptionTeamFull(ExceptionBase):
    code = ExceptionTeamBase.code + 9


class ExceptionTeamLeaderCannotLeave(ExceptionBase):
    code = ExceptionTeamBase.code + 10


class ExceptionTeamKickSelf(ExceptionBase):
    code = ExceptionTeamBase.code + 11


class ExceptionKickNotMember(ExceptionBase):
    code = ExceptionTeamBase.code + 12


class ExceptionNoTeamCondi(ExceptionBase):
    code = ExceptionTeamBase.code + 13


class ExceptionTeamCondiNotMatch(ExceptionBase):
    code = ExceptionTeamBase.code + 14


class ExceptionAlreadyInMatch(ExceptionBase):
    code = ExceptionTeamBase.code + 15


class ExceptionUserNotExist(ExceptionBase):
    code = ExceptionTeamBase.code + 16


class ExceptionParamError(ExceptionBase):
    code = ExceptionTeamBase.code + 17


class ExceptionNotActivityTime(ExceptionBase):
    code = ExceptionTeamBase.code + 18


class ExceptionTeamBossExpired(ExceptionBase):
    code = ExceptionTeamBase.code + 19


class ExceptionTeamBossFinished(ExceptionBase):
    code = ExceptionTeamBase.code + 20


class ExceptionTeamBossInBattle(ExceptionBase):
    code = ExceptionTeamBase.code + 21


class ExceptionTeamBossPartFinish(ExceptionBase):
    code = ExceptionTeamBase.code + 22


class ExceptionMemberNotEnough(ExceptionBase):
    code = ExceptionTeamBase.code + 23


class ExceptionMemberNotReady(ExceptionBase):
    code = ExceptionTeamBase.code + 24


class ExceptionLeaderNotOpen(ExceptionBase):
    code = ExceptionTeamBase.code + 25


class ExceptionFuncFlagNotCurOpened(ExceptionBase):
    code = ExceptionTeamBase.code + 26


class ExceptionOtherFuncOnGoing(ExceptionBase):
    code = ExceptionTeamBase.code + 27


class ExceptionAnyBattleOnGoing(ExceptionBase):
    code = ExceptionTeamBase.code + 28


class ExceptionNoFuncOpened(ExceptionBase):
    code = ExceptionTeamBase.code + 29


class ExceptionAlreadyApplyEnterTeam(ExceptionBase):
    code = ExceptionTeamBase.code + 30


class ExceptionUserHasNoRaid(ExceptionBase):
    code = ExceptionTeamBase.code + 31


class ExceptionUserRaidTimeout(ExceptionBase):
    code = ExceptionTeamBase.code + 32


class ExceptionTeamBossPreNotFinish(ExceptionBase):
    code = ExceptionTeamBase.code + 33


class ExceptionTeamLeaderCanNotChange(ExceptionBase):
    code = ExceptionTeamBase.code + 34


# 要塞战相关
class ExceptionFortWarBase(ExceptionBase):
    code = 3500


class ExceptionNotRegisterAlphaFortWar(ExceptionBase):
    code = ExceptionFortWarBase.code + 1


class ExceptionAlphaFortWarLuckyClan(ExceptionBase):
    code = ExceptionFortWarBase.code + 2


class ExceptionAlphaFortWarNotBattlePeriod(ExceptionBase):
    code = ExceptionFortWarBase.code + 3


class ExceptionAlphaFortWarPointFinish(ExceptionBase):
    code = ExceptionFortWarBase.code + 4


class ExceptionAlphaFortWarPreNotFinish(ExceptionBase):
    code = ExceptionFortWarBase.code + 5


class ExceptionAlphaFortWarUserFrozenTime(ExceptionBase):
    code = ExceptionFortWarBase.code + 6


class ExceptionClanNotFortBattle(ExceptionBase):
    code = ExceptionFortWarBase.code + 7


class ExceptionBattleFieldBusyAndTryLate(ExceptionBase):
    code = ExceptionFortWarBase.code + 8


def make_primitive(arg):
    if isinstance(arg, list) or isinstance(arg, tuple):
        return [make_primitive(v) for v in arg]
    elif isinstance(arg, dict):
        return dict((k, make_primitive(v)) for k, v in arg.iteritems())
    elif isinstance(arg, ExceptionBase):
        result = {}
        if hasattr(arg, 'args'):
            result['args'] = make_primitive(arg.args)
        if hasattr(arg, 'kwargs'):
            result['kwargs'] = make_primitive(arg.kwargs)
        return result
    else:
        return str(arg)


def log_exceptions(*args, **kwargs):
    result = {}

    result['status'] = 'ERROR'
    result['args'] = make_primitive(args)  # [str(e) for e in args]
    result['kwargs'] = make_primitive(kwargs)  # dict((k, str(v)) for k, v in kwargs.iteritems())
    exc_type, exc_value, exc_traceback = sys.exc_info()
    result['call stack'] = []
    for e in traceback.format_exception(exc_type, exc_value, exc_traceback):
        for line in e.split('\n'):
            result['call stack'].append(line)

    # print 'ERROR:',
    # for each in args:
    #     print each,
    # for k, v in kwargs.iteritems():
    #     print k, '=', v, ',',
    # print ':END'
    #
    # # exc_type, exc_value, exc_traceback = sys.exc_info()
    # for line in traceback.format_exception(exc_type, exc_value, exc_traceback):
    #     print line,

    return result
