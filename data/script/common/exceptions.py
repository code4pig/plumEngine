# coding=utf8

from __future__ import unicode_literals
import sys
import traceback


class ExceptionBase(Exception):
    """
    기본 예외. 원인 불가
    """
    code = 1


class ExceptionUnknown(ExceptionBase):
    """
    알 수 없는 예외. 예외가 처리되지 않음.
    """
    code = 1


class ExceptionProcessCommand(ExceptionBase):
    """
    알 수 없는 예외. 명령어 처리 시 예외가 발생함.
    """
    code = 10000


class ExceptionRequest(ExceptionBase):
    """
    알 수 없는 예외. 요청 처리 시 예외가 발생함.
    """
    code = 20000

# add by ZHM, JoyGames, ALPHA GROUP CO.,LTD, at 2017-04-06 for 定义项目组自己的code从50000开始
class ExceptionAOFEI(ExceptionBase):

    code = 50000


# 0 ~ 100: for wittybong
class ExceptionNotEnoughCommandParameter(ExceptionBase):
    """
    스키마상의 커맨드 파라미터(request) 와 실제로 인입된 커맨드 파라미터가 일치하지 않을 때.
    클라-서버간 프로토콜이 일치하지 않을 때 발생하는 문제로, 보통의 경우 개발 오류. 개발 기간중에만 발생할 것으로 추정
    """
    code = ExceptionProcessCommand.code + 1


class ExceptionIncorrectTicket(ExceptionBase):
    """
    개발용도 임시 로그인 요청 시, 암호로 사용되는 키 데이터가 일치하지 않음.
    임시 로그인 시 사용하는 키 코드가 클라-서버간 일치하지 않음. 변경되었을 수 있음.
    개발 시에만 발생. 운영시에는 해당 커맨드가 제외됨.
    """
    code = ExceptionProcessCommand.code + 2


class ExceptionUserAlreadyExist(ExceptionBase):
    """
    기사단이 이미 존재함.
    주로 기사단 생성하려고 할 때 발생.
    """
    code = ExceptionProcessCommand.code + 3


class ExceptionUserNotExist(ExceptionBase):
    """
    기사단이 존재하지 않음.
    게임 최초 접속자의 경우에는 항상 한번 발생함. 보통, 예외코드로 전달되지는 않음.
    기존에 게임을 진행하던 기사단에 이 에러가 나오면 문제가 있는 것.
    """
    code = ExceptionProcessCommand.code + 4


class ExceptionNameAlreadyExist(ExceptionBase):
    """
    기사단 이름이 이미 존재한다.
    기사단 생성 시 중복된 이름이 이미 생성되어 있을 때 발생
    """
    code = ExceptionProcessCommand.code + 5


class ExceptionInvalidMasterId(ExceptionBase):
    """
    미사용
    """
    code = ExceptionProcessCommand.code + 6


class ExceptionHeroAlreadyExist(ExceptionBase):
    """
    영웅이 이미 존재함.
    이미 존재하는 영웅을 다시 생성하려고 시도할 때 발생.
    기사단 생성 시 발생하는 경우에는, 계정 생성 과정에 문제가 있어 기사단 생성은 실패하고 영웅만 생성된 경우일 수 있음.
    """
    code = ExceptionProcessCommand.code + 7


class ExceptionPetsAlreadyExist(ExceptionBase):
    """
    소환수가 이미 존재함.
    소환수를 추가하려고 하는데, 이미 보유한 소환수일 경우 발생. 소환, 구매 등등
    """
    code = ExceptionProcessCommand.code + 8


class ExceptionPetNotExist(ExceptionBase):
    """
    보유하지 않은 소환수를 사용하려고 할 때 발생
    """
    code = ExceptionProcessCommand.code + 9


class ExceptionRequiredColumnNotExist(ExceptionBase):
    """
    프로토콜, 데이터 파싱 실패. 비교적 심각한 예외.
    클라-서버간 프로토콜이 맞지 않을 때 혹은,
    서버에서 데이터베이스 문서의 스키마와 실 데이터가 맞지 않을 때 발생 가능
    """
    code = ExceptionProcessCommand.code + 10


class ExceptionNoEmptySlot(ExceptionBase):
    """
    미사용
    """
    code = ExceptionProcessCommand.code + 11


class ExceptionAlreadyJoined(ExceptionBase):
    """
    미사용
    """
    code = ExceptionProcessCommand.code + 12


class ExceptionItemCannotEquip(ExceptionBase):
    """
    장착할 수 없는 아이템임.
    장비가 아닌데 장착하려 할 경우 발생. 정확히는, 장착 부위 정보가 없는 경우 발생.
    """
    code = ExceptionProcessCommand.code + 13


class ExceptionPetDuplicated(ExceptionBase):
    """
    소환수를 중복해서 사용하려고 할 경우 발생.
    덱에 같은 소환수를 두번 넣는다거나.
    """
    code = ExceptionProcessCommand.code + 14


class ExceptionNotExistInMaster(ExceptionBase):
    """
    마스터에 존재하지 않는 아이템일 경우.
    장비 장착 시 발생하는 듯
    """
    code = ExceptionProcessCommand.code + 15


class ExceptionDoNotHave(ExceptionBase):
    """
    보유하지 않은 아이템을 사용하려 할 경우
    """
    code = ExceptionProcessCommand.code + 16


class ExceptionHeroNotExist(ExceptionBase):
    """
    영웅이 없음
    선택된 영웅이 없거나, 존재하지 않는 영웅을 사용하려고 할 경우 발생.
    """
    code = ExceptionProcessCommand.code + 17


class ExceptionNotEnoughAdena(ExceptionBase):
    """
    아데나가 부족함
    """
    code = ExceptionProcessCommand.code + 18


class ExceptionSkillMaxLevel(ExceptionBase):
    """
    스킬 레벨업 하려 하였으나, 이미 최고 레벨일 경우
    """
    code = ExceptionProcessCommand.code + 19


class ExceptionSubStageNotExist(ExceptionBase):
    """
    유저가 도달하지 못했거나, 애초에 존재하지 않는(마스터에) 스테이지를 이용하려고 했을 경우
    """
    code = ExceptionProcessCommand.code + 20


class ExceptionNotEnoughPetSoul(ExceptionBase):
    """
    미사용
    """
    code = ExceptionProcessCommand.code + 21


class ExceptionGuildAlreadyJoined(ExceptionBase):
    """
    현재는 미사용. 옛날거.
    """
    code = ExceptionProcessCommand.code + 22


class ExceptionNotExistSkill(ExceptionBase):
    """
    보유하지 않은 영웅 스킬을 장착하려고 함
    """
    code = ExceptionProcessCommand.code + 23


class ExceptionAlreadyEquipSkill(ExceptionBase):
    """
    이미 장착된 영웅 스킬을 다시 장착하려고 함
    """
    code = ExceptionProcessCommand.code + 24


class ExceptionNotEnoughTryCount(ExceptionBase):
    """
    요일던전 입장회수 부족함
    """
    code = ExceptionProcessCommand.code + 25


class ExceptionMonarchCannotLeave(ExceptionBase):
    """
    현재 미사용. 옛날거
    """
    code = ExceptionProcessCommand.code + 26


class ExceptionEnoughPotion(ExceptionBase):
    """
    현재 미사용. 옛날거
    """
    code = ExceptionProcessCommand.code + 27


class ExceptionCostumeNotExist(ExceptionBase):
    """
    미사용
    """
    code = ExceptionProcessCommand.code + 28


class ExceptionDeleteUserNotFoundID(ExceptionBase):
    """
    미사용
    """
    code = ExceptionProcessCommand.code + 29


class ExceptionCombatantsNotExist(ExceptionBase):
    """
    해당 combatants(영웅, 소환수, 몬스터)가 존재하지 않음
    """
    code = ExceptionProcessCommand.code + 30


class ExceptionExceedMaxRarity(ExceptionBase):
    """
    소환수 등급(희귀도, 별)을 한도 이상 올렸을때.(올리려고 할 때)
    """
    code = ExceptionProcessCommand.code + 31


class ExceptionHeroClassNotExist(ExceptionBase):
    """
    존재하지 않는 종류의 영웅을 생성하려 할 경우.
    """
    code = ExceptionProcessCommand.code + 32


class ExceptionNotEnoughMaterial(ExceptionBase):
    """
    재료가 모자람. 제작 시.
    """
    code = ExceptionProcessCommand.code + 33


class ExceptionStageDailyTryLimit(ExceptionBase):
    """
    스토리 탐험 일 도전횟수 초과.
    스토리 탐험 및 소탕
    """
    code = ExceptionProcessCommand.code + 34


class ExceptionFieldNotOpened(ExceptionBase):
    """
    필드가 오픈되지 않음.
    오픈되지 않은 필드의 스테이지에 도전하려 하거나, 소탕하려 할 때
    """
    code = ExceptionProcessCommand.code + 35


class ExceptionDifficultyNotOpened(ExceptionBase):
    """
    도전할 수 없는 난이도.
    스토리, 요일던전에 해당
    """
    code = ExceptionProcessCommand.code + 36


class ExceptionPreviousStageNotCleared(ExceptionBase):
    """
    이전 스테이지가 클리어되지 않음.
    클리어하지 않은 스테이지를 건너뛰어 도전하려 할 경우
    """
    code = ExceptionProcessCommand.code + 37


class ExceptionItemNotExist(ExceptionBase):
    """
    존재하지 않는 아이템을 사용하려 할 경우 발생.
    보유하지 않거나, 애초에 존재하지 않는 아이템
    """
    code = ExceptionProcessCommand.code + 38


class ExceptionExceedMaxTrainingLevel(ExceptionBase):
    """
    미사용
    """
    code = ExceptionProcessCommand.code + 39


class ExceptionExceedMaxHeroSkillLevel(ExceptionBase):
    """
    미사용
    """
    code = ExceptionProcessCommand.code + 40


class ExceptionFieldNotCleared(ExceptionBase):
    """
    미사용
    """
    code = ExceptionProcessCommand.code + 50


class ExceptionFieldInvestFull(ExceptionBase):
    """
    미사용
    """
    code = ExceptionProcessCommand.code + 51


class ExceptionAlreadyInvestigating(ExceptionBase):
    """
    이미 탐색 중이 필드에 다시 도전하려 함
    """
    code = ExceptionProcessCommand.code + 52


class ExceptionInvestigationNotExist(ExceptionBase):
    """
    탐색을 보내지 않은 필드에 접근하려 함.(기록을 보려고 함)
    """
    code = ExceptionProcessCommand.code + 53


class ExceptionInvestigationCannotStop(ExceptionBase):
    """
    탐색을 중단할 수 없음.
    탐색 보낸 시간이 경과하지 않음
    """
    code = ExceptionProcessCommand.code + 54


class ExceptionCannotInvestigate(ExceptionBase):
    """
    미사용
    """
    code = ExceptionProcessCommand.code + 55


class ExceptionFieldIsNotFull(ExceptionBase):
    """
    미사용
    """
    code = ExceptionProcessCommand.code + 56


class ExceptionCannotFindPlundee(ExceptionBase):
    """
    미사용
    거점약탈 있을 때 사용하던 것
    """
    code = ExceptionProcessCommand.code + 57


class ExceptionNoResident(ExceptionBase):
    """
    미사용
    """
    code = ExceptionProcessCommand.code + 58


class ExceptionNotReserved(ExceptionBase):
    """
    약탈 대상자 관련 오류

    """
    code = ExceptionProcessCommand.code + 59


class ExceptionAlreadyReserved(ExceptionBase):
    """
    이미 다른 유저가 공격중인 사람을 공격하려고 함.
    자원탐색 약탈, 콜로세움(PVP)
    """
    code = ExceptionProcessCommand.code + 60


class ExceptionAlreadyRemodelingAnotherSlot(ExceptionBase):
    """
    이미 한 슬롯의 옵션을 개조했는데, 다른 슬롯의 옵션을 개조하려 할 경우.
    한 슬롯밖에 개조 불가
    """
    code = ExceptionProcessCommand.code + 61


class ExceptionCountNotMatch(ExceptionBase):
    """
    미사용
    """
    code = ExceptionProcessCommand.code + 62


class ExceptionNoMatchItemRarity(ExceptionBase):
    """
    서로 다른 등급의 아이템을 개조 재료료 사용할 수 없음
    """
    code = ExceptionProcessCommand.code + 63


class ExceptionCannotFindPvpTarget(ExceptionBase):
    """
    미사용
    """
    code = ExceptionProcessCommand.code + 64


class ExceptionCannotPvpThatRank(ExceptionBase):
    """
    미사용
    """
    code = ExceptionProcessCommand.code + 65


class ExceptionClassObjectParseError(ExceptionBase):
    """
    파싱 에러. 심각한 예외.
    클라-서버간 프로토콜 오류 혹은,
    서버의 데이터베이스 스키마와 실 데이터가 맞지 않는 오류
    """
    code = ExceptionProcessCommand.code + 66


class ExceptionBookingTimeout(ExceptionBase):
    """
    미사용
    """
    code = ExceptionProcessCommand.code + 67


class ExceptionEquipmentLocked(ExceptionBase):
    """
    잠금 아이템을 사용하려 함
    판매하려고 한다거나..
    """
    code = ExceptionProcessCommand.code + 68


class ExceptionEquipmentLackRarity(ExceptionBase):
    """
    희귀도가 2 이하인 아이템을 개조하려 시도함
    """
    code = ExceptionProcessCommand.code + 69


class ExceptionNotEnoughDailyTryCount(ExceptionBase):
    """
    일 도전횟수 초과. 더 이상 도전할 수 없음.
    콜로세움, 오만의 탑
    """
    code = ExceptionProcessCommand.code + 70


class ExceptionNotEnoughDailyBossTryCount(ExceptionBase):
    """
    미사용
    """
    code = ExceptionProcessCommand.code + 71


class ExceptionNotMatchFloorBeginAndEnd(ExceptionBase):
    """
    오만의 탑 도전 오류. 도전 시작과 종료가 짝이 맞지 않음.
    도전을 개시한 기록이 없는데, 도전 완료 요청이 온 경우
    """
    code = ExceptionProcessCommand.code + 72


class ExceptionLockedItem(ExceptionBase):
    """
    슬라임에게 분해 불가한 아이템을 먹이려 할 때.
    잠근 아이템이거나, 장착중인 아이템일 때
    """
    code = ExceptionProcessCommand.code + 73


class ExceptionNoCurseEquipment(ExceptionBase):
    """
    저주받지 않은 아이템을 저주해제하려 할 경우
    """
    code = ExceptionProcessCommand.code + 74


class ExceptionNoMatchMaterialItem(ExceptionBase):
    """
    주문서의 종류가 용도에 맞지 않을 때
    """
    code = ExceptionProcessCommand.code + 75


class ExceptionFullStrengthenEquipment(ExceptionBase):
    """
    이미 강화도가 최대인 장비를 강화하려고 시도함
    """
    code = ExceptionProcessCommand.code + 76


class ExceptionAlreadyCurseEquipment(ExceptionBase):
    """
    저주받은 아이템을 강화하려 함
    """
    code = ExceptionProcessCommand.code + 77


class ExceptionNoMatchEquipmentType(ExceptionBase):
    """
    장비 옵션 변경 시, 부합하지 않는 재료를 사용하려 함
    """
    code = ExceptionProcessCommand.code + 78


class ExceptionDoNotHaveDeck(ExceptionBase):
    """
    아직 덱을 지정하지 않음. (레이드)
    """
    code = ExceptionProcessCommand.code + 79


class ExceptionNoMatchRaidID(ExceptionBase):
    """
    현재 시즌의 레이드 보스가 아님.
    """
    code = ExceptionProcessCommand.code + 80


class ExceptionNoSearchLevelExp(ExceptionBase):
    """
    지정된 레벨이 존재하지 않음. 레벨을 0 이하로 지정했을 때.
    """
    code = ExceptionProcessCommand.code + 81


class ExceptionNotParameter(ExceptionBase):
    """
    미사용
    """
    code = ExceptionProcessCommand.code + 82


class ExceptionNotTrainingLevel(ExceptionBase):
    """
    존재하지 않는 연성 레벨을 지정함. 최대 연성 레벨 이상 연성하려고 할 때
    """
    code = ExceptionProcessCommand.code + 83


class ExceptionExceptionAlreadyLearnSkill(ExceptionBase):
    """
    이미 배운 스킬을 다시 배우려 함
    """
    code = ExceptionProcessCommand.code + 84


class ExceptionNotHaveTransform(ExceptionBase):
    """
    습득하지 않은 변신을 하려 함
    """
    code = ExceptionProcessCommand.code + 85


class ExceptionAlreadyHaveTransform(ExceptionBase):
    """
    이미 습득한 변신을 습득하려 함
    """
    code = ExceptionProcessCommand.code + 86


class ExceptionNotMatchTransformOwner(ExceptionBase):
    """
    변신과 영웅이 부합하지 않음. (변신 습득 시)
    """
    code = ExceptionProcessCommand.code + 87


class ExceptionProudTowerOverFloor(ExceptionBase):
    """
    도전 가능한 층 이상을 도전하려 함
    """
    code = ExceptionProcessCommand.code + 88


class ExceptionApiErrorInventoryNotFound(ExceptionBase):
    """
    운영툴 용
    """
    code = ExceptionProcessCommand.code + 89


class ExceptionNotMatchItemKey(ExceptionBase):
    """
    영혼석/축영혼석 종류가 맞지 않게 사용하려고 함. 소환/축복
    """
    code = ExceptionProcessCommand.code + 90


class ExceptionAlreadyRecvFirstClearReward(ExceptionBase):
    """
    이미 수령한 최초 클리어 보상을 다시 받으려고 함
    """
    code = ExceptionProcessCommand.code + 91


class ExceptionNotEnoughStageStar(ExceptionBase):
    """
    스테이지 클리어 별 개수가 부족함. (소탕 불가)
    """
    code = ExceptionProcessCommand.code + 92


class ExceptionOverSweepCount(ExceptionBase):
    """
    미사용
    """
    code = ExceptionProcessCommand.code + 93


class ExceptionNotEnoughCrackDungeonStar(ExceptionBase):
    """
    요일던전 클리어 별 개수가 부족함. (소탕 불가)
    """
    code = ExceptionProcessCommand.code + 94


class ExceptionNotFoundStageInfo(ExceptionBase):
    """
    해당 스테이지를 클리어하지 않음. (소탕 불가)
    """
    code = ExceptionProcessCommand.code + 95


class ExceptionNoMatchDeckHero(ExceptionBase):
    """
    현재 선택되지 않은 영웅이 덱에 포함됨
    """
    code = ExceptionProcessCommand.code + 96


class ExceptionNoMatchDeckPets(ExceptionBase):
    """
    미사용
    """
    code = ExceptionProcessCommand.code + 97


class ExceptionNotEnoughSlimePoint(ExceptionBase):
    """
    슬라임 포인트가 부족함
    """
    code = ExceptionProcessCommand.code + 98


class ExceptionOverEquipmentSlimeFeed(ExceptionBase):
    """
    먹일 수 있는 최대 장비수를 초과하여 슬라임에게 먹이려 함
    """
    code = ExceptionProcessCommand.code + 99


# 101 ~ 200: for magi


class ExceptionRestrictionFail(ExceptionBase):
    """
    덱 편성이 요건을 충족하지 않음
    """
    code = ExceptionProcessCommand.code + 101


class ExceptionDungeonNotAvailable(ExceptionBase):
    """
    오픈되지 않은 요일던전을 이용하려 함
    """
    code = ExceptionProcessCommand.code + 102


class ExceptionDifficultyNotInRange(ExceptionBase):
    """
    존재하지 않는 난이도의 요일던전에 도전하려한 경우
    """
    code = ExceptionProcessCommand.code + 103


class ExceptionNotEnoughAp(ExceptionBase):
    """
    단검이 부족함
    """
    code = ExceptionProcessCommand.code + 104


class ExceptionNotStarted(ExceptionBase):
    """
    도전 시작하지 않은 요일던전을 종료하려 함
    """
    code = ExceptionProcessCommand.code + 105


class ExceptionNotEnoughCount(ExceptionBase):
    """
    미사용
    """
    code = ExceptionProcessCommand.code + 106


class ExceptionOccupied(ExceptionBase):
    """
    (다른) 영웅이 장착한 장비를 장착/판매 하려 한 경우
    """
    code = ExceptionProcessCommand.code + 107


class ExceptionApiGateFail(ExceptionBase):
    """
    플랫폼으로의 요청이 실패됨. 원인은 다양할 수 있음. 현재는 해당 플랫폼이 무엇이냐에 따라 세분화된 별개의 예외가 발생할 것임. 현재는 아마도 미사용
    """
    code = ExceptionProcessCommand.code + 108


class ExceptionNotEnoughDiamond(ExceptionBase):
    """
    다이아몬드가 부족함
    """
    code = ExceptionProcessCommand.code + 109


class ExceptionTransformAlreadyExist(ExceptionBase):
    """
    이미 획득한 변신을 획득하려 함
    """
    code = ExceptionProcessCommand.code + 110


class ExceptionCannotTransform(ExceptionBase):
    """
    미사용
    """
    code = ExceptionProcessCommand.code + 111


class ExceptionHaveNotEnough(ExceptionBase):
    """
    미사용
    """
    code = ExceptionProcessCommand.code + 112


class ExceptionAlreadyExist(ExceptionBase):
    """
    이미 보유한 코스튬을 구매하려 함
    """
    code = ExceptionProcessCommand.code + 113


class ExceptionCannotPurchase(ExceptionBase):
    """
    코스튬을 구매할 수 없음. 획득 조건 미달성.
    """
    code = ExceptionProcessCommand.code + 114


class ExceptionHeroSummarizeFail(ExceptionBase):
    """
    미사용
    """
    code = ExceptionProcessCommand.code + 115


class ExceptionNotReward(ExceptionBase):
    """
    축적한 보상이 부족하여 약탈할 수 없음
    """
    code = ExceptionProcessCommand.code + 116


class ExceptionCloakLimit(ExceptionBase):
    """
    투명망토 적용 개수 초과
    """
    code = ExceptionProcessCommand.code + 117


class ExceptionNotEnoughParty(ExceptionBase):
    """
    탐색 파티 인원수가 부족함
    """
    code = ExceptionProcessCommand.code + 118


class ExceptionNotEnoughAsset(ExceptionBase):
    """
    가진 자산이 부족해 비용을 차감할 수 없음
    """
    code = ExceptionProcessCommand.code + 119


class ExceptionInvalidMailId(ExceptionBase):
    """
    존재하지 않는 메일을 수령하려 함
    """
    code = ExceptionProcessCommand.code + 120


class ExceptionRaidFindCooldown(ExceptionBase):
    """
    미사용. 사용중이긴 하나 클라에 전달되지 않음.
    """
    code = ExceptionProcessCommand.code + 121


class ExceptionNoCurrentRaid(ExceptionBase):
    """
    현재 보스레이드 시즌이 아님
    """
    code = ExceptionProcessCommand.code + 122


class ExceptionInvalidPartRequestOnRaid(ExceptionBase):
    """
    해당 레이드 부위를 공격할 수 없음. 이유는 다양.
    """
    code = ExceptionProcessCommand.code + 123


class ExceptionNoEmptyPartOnRaid(ExceptionBase):
    """
    도전하려는 보스레이드 부위에 이미 누군가 전투중임
    """
    code = ExceptionProcessCommand.code + 124


class ExceptionNotFoundUserIdOnRaid(ExceptionBase):
    """
    미사용
    """
    code = ExceptionProcessCommand.code + 125


class ExceptionTimeoutOnRaid(ExceptionBase):
    """
    보스레이드 도전 시간이 초과 됨. 보스 발견 후 두시간 제한 or 전투 개시 후 2분 제한
    """
    code = ExceptionProcessCommand.code + 126


class ExceptionDeckSize(ExceptionBase):
    """
    덱 편성 인원수가 기준에 부합하지 않음
    """
    code = ExceptionProcessCommand.code + 127


class ExceptionLockDocumentFail(ExceptionBase):
    """
    동일한 데이터베이스 데이터에 동시에 접근함. 같은 점령지에 둘 이상이 동시에 공격한다거나. 일시적으로 발생할 수 있는 에러. 다시 시도하면 될 가능성이 높음.
    """
    code = ExceptionProcessCommand.code + 128


class ExceptionCofigurationFail(ExceptionBase):
    """
    임시 테스트코드로 인증 시도할 경우 발생할 수 있는 에러. 라이브 운영시 발생하지 않음
    """
    code = ExceptionProcessCommand.code + 129


class ExceptionNotEnoughStackable(ExceptionBase):
    """
    행위에 대한 비용을 지불할 수 없음. 재료(자산, 횟수)가 모자람.
    """
    code = ExceptionProcessCommand.code + 130


class ExceptionMasterRowNotExist(ExceptionBase):
    """
    마스터 데이터에 해당 데이터가 존재하지 않음. 데이터 에러.
    """
    code = ExceptionProcessCommand.code + 131


class ExceptionInvalidParameter(ExceptionBase):
    """
    파라미터가 의도한 것과 다르게 전달됨. 프로그램 오류.
    """
    code = ExceptionProcessCommand.code + 132


class ExceptionIndexNotExist(ExceptionBase):
    """
    마스터 데이터에서 해당 데이터를 검색하는데 실패함. 데이터 오류
    """
    code = ExceptionProcessCommand.code + 133


class ExceptionStageNotBegun(ExceptionBase):
    """
    정상적으로 도전이 시작되지 않은 스테이지를 전투 종료하려 함
    """
    code = ExceptionProcessCommand.code + 134


class ExceptionCannotLevelUp(ExceptionBase):
    """
    더 이상 레벨업 할 수 없음. 한계치까지 레벨업 함. 경험치 물약 사용 시
    """
    code = ExceptionProcessCommand.code + 135


class ExceptionContentLocked(ExceptionBase):
    """
    미사용. 클라이언트에 전달되지 않음. 해당 컨텐츠를 임시로 잠금. 운영적 이슈.
    """
    code = ExceptionProcessCommand.code + 136


class ExceptionNotOwner(ExceptionBase):
    """
    착용할 수 없는 장비를 착용하려 함. 해당 장비를 사용할 수 있는 영웅 클래스가 아님
    """
    code = ExceptionProcessCommand.code + 137


class ExceptionTutorialAlreadyDone(ExceptionBase):
    """
    이미 완료한 튜토리얼을 다시 진행하려 함
    """
    code = ExceptionProcessCommand.code + 138


class ExceptionContentsPaused(ExceptionBase):
    """
    운영상 컨텐츠를 임시로 잠금. 해당 컨텐츠를 현재 이용할 수 없음.
    """
    code = ExceptionProcessCommand.code + 139


class ExceptionExceedMaxExp(ExceptionBase):
    """
    최대 한도를 넘는 기사단 경험치를 보유한 경우. 주로 임의로 경험치를 조작한 경우에 발생.
    """
    code = ExceptionProcessCommand.code + 141


class ExceptionCannotLevelDown(ExceptionBase):
    """
    유틸리티용 기능. 라이브 서비스 시 미사용.
    """
    code = ExceptionProcessCommand.code + 142


class ExceptionBannedWord(ExceptionProcessCommand):
    """
    금칙어에 포함됨. 기사단 이름 지정 시
    """
    code = ExceptionProcessCommand.code + 143


class ExceptionInvalidServer(ExceptionBase):
    """
    존재하지 않은 서버로 입장하려 함
    """
    code = ExceptionProcessCommand.code + 144


class ExceptionAnotherLoggedIn(ExceptionBase):
    """
    이중접속으로 차단됨
    """
    code = ExceptionProcessCommand.code + 145


class ExceptionApiGateAuthFail(ExceptionBase):
    """
    플랫폼으로의 인증 요청이 실패함
    """
    code = ExceptionProcessCommand.code + 146


class ExceptionApiGateLeaderboardManagerFail(ExceptionBase):
    """
    플랫폼으로의 리더보드(랭킹) 요청이 실패함
    """
    code = ExceptionProcessCommand.code + 147


class ExceptionApiGateLeaderboardFail(ExceptionBase):
    """
    플랫폼으로의 리더보드(랭킹) 요청이 실패함
    """
    code = ExceptionProcessCommand.code + 148


class ExceptionApiGateStorageManagerFail(ExceptionBase):
    """
    플랫폼으로의 스토리지(프로필) 요청이 실패함
    """
    code = ExceptionProcessCommand.code + 149


class ExceptionApiGateStorageFail(ExceptionBase):
    """
    플랫폼으로의 스토리지(프로필) 요청이 실패함
    """
    code = ExceptionProcessCommand.code + 150


class ExceptionAppGateChattingFail(ExceptionBase):
    """
    플랫폼으로의 채팅 요청이 실패함
    """
    code = ExceptionProcessCommand.code + 151


class ExceptionAppGateWareHouseFail(ExceptionBase):
    """
    플랫폼으로의 웨어하우스 요청이 실패함
    """
    code = ExceptionProcessCommand.code + 152


class ExceptionReaderCannotWrite(ExceptionBase):
    """
    프로그램 에러. Reader 가 데이터를 수정하려고 시도함
    """
    code = ExceptionProcessCommand.code + 153


class ExceptionExceedStoryClearPeriod(ExceptionBase):
    """
    스토리 탐험 한도 기한인 10분을 넘어서 플레이가 진행됨.
    """
    code = ExceptionProcessCommand.code + 154


class ExceptionRaidMatch(ExceptionBase):
    """
    해당하는 레이드가 존재하지 않음.
    주로, 이미 시즌 종료된 레이드를 종료할 때 발생
    """
    code = ExceptionProcessCommand.code + 155


class ExceptionMinusCount(ExceptionBase):
    """
    리퀘스트 파라미터 중 카운트가 마이너스가 왔음
    """
    code = ExceptionProcessCommand.code + 156


class ExceptionNoRankInfo(ExceptionBase):
    """
    리더보드 조회하였으나 해당 데이터가 없음
    """
    code = ExceptionProcessCommand.code + 157


class ExceptionPowerLevel(ExceptionBase):
    """
    전투력 등급 계산 시 오류 발생함
    """
    code = ExceptionProcessCommand.code + 158


# end magi


# 201 ~ 300: for ys
class ExceptionNotEnoughBattleCoin(ExceptionBase):
    """
    혈맹코인이 비용을 지불하기에 부족함
    """
    code = ExceptionProcessCommand.code + 201


class ExceptionInvalidShopProductKey(ExceptionBase):
    """
    상점에 진열된 아이템이 아님
    """
    code = ExceptionProcessCommand.code + 202


class ExceptionNeedShopMstRefresh(ExceptionBase):
    """
    진열된 상품의 정보가 이상이 있을 경우 발생 함
    """
    code = ExceptionProcessCommand.code + 203


class ExceptionInShopProcess(ExceptionBase):
    """
    상품 구매가 정상 적으로 진행 되지 않을 경우 발생 함
    """
    code = ExceptionProcessCommand.code + 204


class ExceptionInvalidGachaDataFormat(ExceptionBase):
    """
    뽑은 갸차 상차자 이상이 있을 경우 발생 함
    """
    code = ExceptionProcessCommand.code + 205


class ExceptionNotEnoughGachaCoupon(ExceptionBase):
    """
    무료 쿠폰으로 10연차 가차 뽑기 요청시 발생 함
    """
    code = ExceptionProcessCommand.code + 206


class ExceptionCooldownGachaCoupon(ExceptionBase):
    """
    미사용
    """
    code = ExceptionProcessCommand.code + 207


class ExceptionInvalidGachaType(ExceptionBase):
    """
    잘못된 뽑기 데이터로 발생 할 수 있음
    """
    code = ExceptionProcessCommand.code + 208


class ExceptionBuyCountLimit(ExceptionBase):
    """
    미사용
    """
    code = ExceptionProcessCommand.code + 209


class ExceptionInvalidAddItemResultFormat(ExceptionBase):
    """
    아이템을 인벤토리에 추가 할때 아이템 데이터가 잘못 되어있을 경우 발생 함
    """
    code = ExceptionProcessCommand.code + 210


class ExceptionInvalidAddItemResult(ExceptionBase):
    """
        아이템을 인벤토리에 추가 할때 아이템 데이터가 잘못 되어있을 경우 발생 함
    """
    code = ExceptionProcessCommand.code + 211


class ExceptionBattleFieldRequireRetry(ExceptionBase):
    """
    점령전 초기화 진행 시 이미 점령전 키가 등록되 어 있는 경우 발생 할 수 있음
    """
    code = ExceptionProcessCommand.code + 220


class ExceptionBattleFieldPetDuplicated(ExceptionBase):
    """
    점령전 수비덱 / 탐색 / 등에서 중복된 소환수나 영웅을 사용 할 경우 발생 함
    """
    code = ExceptionProcessCommand.code + 221


class ExceptionIncorrectUseUpdateMethodInReadonlyDo(ExceptionBase):
    """
    데이터 클래스의 잘못된 사용에 대한 경고
    """
    code = ExceptionProcessCommand.code + 222


class ExceptionInvalidBattleFieldBlockStatus(ExceptionBase):
    """
    해당 블록은 전투중 이여서 전투 진행이 되지 않습니다
    """
    code = ExceptionProcessCommand.code + 223


class ExceptionInvalidBattleFieldAttackCommand(ExceptionBase):
    """
    거점 공격 타임 아웃이 발생하여 공격 결과를 반영할 수 없음
    """
    code = ExceptionProcessCommand.code + 224


class ExceptionInvalidBattleFieldReqReturnPets(ExceptionBase):
    """
    점령전 수비로 배치했던 소환수를 반환하던중 유효하지 않은 반환 요청이 들어온경우
    """
    code = ExceptionProcessCommand.code + 225


class ExceptionInvalidProclamationFortWar(ExceptionBase):
    """
    해당 블록 거점이 요새가 아닐 경우 발생 함
    """
    code = ExceptionProcessCommand.code + 226


class ExceptionAlreadyWarFort(ExceptionBase):
    """
    이미 요새전이 선포 되어 있을 경우 발생 함
    """
    code = ExceptionProcessCommand.code + 227


class ExceptionFortWarPetDuplicated(ExceptionBase):
    """
    거점에 이미 등록한 소환수를 또 등록 하려고 할 경우 발생 함
    """
    code = ExceptionProcessCommand.code + 228


class ExceptionBattleFieldNeedClan(ExceptionBase):
    """
    혈맹에 가입되어 있지 않은 상태에서 점령전 진행 할 경우 발생 함
    """
    code = ExceptionProcessCommand.code + 229


class ExceptionDestroyFortReq(ExceptionBase):
    """
    파괴된 요새에대한 요새전 요청
    """
    code = ExceptionProcessCommand.code + 230


class ExceptionNotEnoughFortWarAttackTicketCount(ExceptionBase):
    """
    더이상 요새전을 진행 할 수 없을 때 발생 함 ( 도전 횟수 전부 소진 _ )
    """
    code = ExceptionProcessCommand.code + 231


class ExceptionNotOwnBlockOrder(ExceptionBase):
    """
    해당 거점이 유저 점령지가 아닐 경우 명령을 내릴 때 발생 함
    """
    code = ExceptionProcessCommand.code + 232


class ExceptionDuplicatedReqConquestDailyReward(ExceptionBase):
    """
    이미 지급된 보상을 추가적으로 또 받겠다고 요청 올때 발생 함
    """
    code = ExceptionProcessCommand.code + 233


class ExceptionInvalidReqConquestDailyRewardPoint(ExceptionBase):
    """
    점령전에서 더이상 받을 보상이 없을 때 발생 함
    """
    code = ExceptionProcessCommand.code + 234


class ExceptionInvalidReqAttackAlliance(ExceptionBase):
    """
    동일한 동맹의 거점을 공격 하려고 할때 발생 함
    """
    code = ExceptionProcessCommand.code + 235


class ExceptionNotEnoughConquestTicketCount(ExceptionBase):
    """
    유저의 점령전 도전 횟수가 이슈가 있을 때 발생 함
    """
    code = ExceptionProcessCommand.code + 236


class ExceptionFortWarExceedUseItemCount(ExceptionBase):
    """
    요새전에서 구매할 수 있는 물약갯수 초과
    """
    code = ExceptionProcessCommand.code + 237


class ExceptionChattingChannelCreateRequireRetry(ExceptionBase):
    """
    미사용
    """
    code = ExceptionProcessCommand.code + 238


class ExceptionInvalidReqNotExistFortInfo(ExceptionBase):
    """
    이미 파괴된 요새에대한 정보 요청
    """
    code = ExceptionProcessCommand.code + 239


class ExceptionNotEnoughChattingChannelCoupon(ExceptionBase):
    """
    미사용
    """
    code = ExceptionProcessCommand.code + 240


class ExceptionAppGateFail(ExceptionBase):
    """
    플랫폼 AppGateFail 에러
    """
    code = ExceptionProcessCommand.code + 241


class ExceptionInvalidFortStatus(ExceptionBase):
    """
    요새가 아닌곳에 대한 요새관련 정보 요청
    """
    code = ExceptionProcessCommand.code + 242


class ExceptionExceedClanMissionCount(ExceptionBase):
    """
    군주명령 최대 갯수 초과
    """
    code = ExceptionProcessCommand.code + 243


class ExceptionExceedDefenseDeckCount(ExceptionBase):
    """
    점령전 지원 총 수치를 초과 하였습니다
    """
    code = ExceptionProcessCommand.code + 244


class ExceptionExceedFortDefenseDeckCount(ExceptionBase):
    """
    덱 세팅 인원을 초과 하였습니다
    """
    code = ExceptionProcessCommand.code + 245


class ExceptionAlreadySetChannelId(ExceptionBase):
    """
    미사용
    """
    code = ExceptionProcessCommand.code + 246


class ExceptionInvalidFortWarAttackCommand(ExceptionBase):
    """
    요새전 공격 타임아웃이 되어 공격이 무효처리된 경우
    """
    code = ExceptionProcessCommand.code + 247


class ExceptionFortWarExceedPotionCount(ExceptionBase):
    """
    아이템 보유 한도를 초과 했습니다
    """
    code = ExceptionProcessCommand.code + 248


class ExceptionBattleFieldPermissionDenied(ExceptionBase):
    """
    점령전 선포 권한이 없는 사용자 입니다
    """
    code = ExceptionProcessCommand.code + 249


class ExceptionNotEnoughSoulSculpture(ExceptionBase):
    """
    영혼석 조각이 비용을 지불하기에 부족함
    """
    code = ExceptionProcessCommand.code + 250


class ExceptionClosedRolkoShop(ExceptionBase):
    """
    롤코상점이 닫힌시간임
    """
    code = ExceptionProcessCommand.code + 251


class ExceptionInvalidReqDiaMileageRewardPoint(ExceptionBase):
    """
    다이아 마일리지로 교환할 상품이 없을때 발생함
    """
    code = ExceptionProcessCommand.code + 252


class ExceptionInvalidServerGroupId(ExceptionBase):
    """
    서버에서 핸들링하지 않는 서버 그룹아이디 global_def.py에 추가 해주세요
    """
    code = ExceptionProcessCommand.code + 253


class ExceptionInvalidServerUserId(ExceptionBase):
    """
    서버에서 핸들링하지 않는 서버 유져아이디 global_def.py에 추가 해주세요
    """
    code = ExceptionProcessCommand.code + 254


class ExceptionNotClanFort(ExceptionBase):
    """
    우리 혈맹의 요새가 아닌것에 대한 요청
    """
    code = ExceptionProcessCommand.code + 255


# 301 ~ 400: for mh
class ExceptionUpdateAchievement(ExceptionBase):
    """
    업적 업데이트 실패 : 키-타겟 개수 오류
    """
    code = ExceptionProcessCommand.code + 301


class ExceptionInvalidAchievementKey(ExceptionBase):
    """
    유효하지 않은 업적 키
    """
    code = ExceptionProcessCommand.code + 302


class ExceptionNotCompletedAchievement(ExceptionBase):
    """
    완료 조건을 만족하지 못함
    """
    code = ExceptionProcessCommand.code + 303


class ExceptionExpiredAchievementDay(ExceptionBase):
    """
    일일 업적이 리셋되어 완료 실패
    """
    code = ExceptionProcessCommand.code + 304


class ExceptionInvalidAchievementMainTheme(ExceptionBase):
    """
    유효하지 않은 성장 업적 키-주제
    """
    code = ExceptionProcessCommand.code + 305


class ExceptionInvalidAchievementMainGroup(ExceptionBase):
    """
    유효하지 않은 성장 업적 키-그룹
    """
    code = ExceptionProcessCommand.code + 306


class ExceptionAlreadyTakenAchievementMainGroupReward(ExceptionBase):
    """
    이미 보상을 받아간 성장 업적
    """
    code = ExceptionProcessCommand.code + 307


class ExceptionAlreadyCompleteAchievementPvp(ExceptionBase):
    """
    이미 완료한 콜로세움 업적
    """
    code = ExceptionProcessCommand.code + 308


class ExceptionInvalidAchievementPvpCompleteCount(ExceptionBase):
    """
    유효하지 않은 콜로세움 카운트 보상 키
    """
    code = ExceptionProcessCommand.code + 309


class ExceptionAlreadyTakenAchievementPvpCompleteCountReward(ExceptionBase):
    """
    이미 보상을 받아간 콜로세움
    """
    code = ExceptionProcessCommand.code + 310


class ExceptionNotEnoughAchievementPvpCompleteCount(ExceptionBase):
    """
    완료 조건을 만족하지 못함 - 콜로세움 업적 클리어 횟수
    """
    code = ExceptionProcessCommand.code + 311


class ExceptionAlreadyCompleteAchievementProudTower(ExceptionBase):
    """
    이미 완료한 업적 - 오만의 탑
    """
    code = ExceptionProcessCommand.code + 312


class ExceptionExpiredAchievementDayItem(ExceptionBase):
    """
    오픈 시간이 아닌 일일 업적 항목
    """
    code = ExceptionProcessCommand.code + 313


class ExceptionBossInvalidExistOnFloor(ExceptionBase):
    """
    보스가 존재하지 않는 오만의 탑 층
    """
    code = ExceptionProcessCommand.code + 314


class ExceptionInvalidAchievementReward(ExceptionBase):
    """
    미사용
    """
    code = ExceptionProcessCommand.code + 315


class ExceptionAlreadyCompleteAchievement(ExceptionBase):
    """
    이미 완료한 업적
    """
    code = ExceptionProcessCommand.code + 315


class ExceptionAlreadyHaveCrackTicket(ExceptionBase):
    """
    요일 던전 티켓을 갖고 있어서 구매 불가
    """
    code = ExceptionProcessCommand.code + 316


class ExceptionAlreadyPurchaseCrackTicket(ExceptionBase):
    """
    오늘 요일 던전 티켓을 구매한 적이 있어서 구매 불가
    """
    code = ExceptionProcessCommand.code + 317


class ExceptionAlreadyCompleteDestiny(ExceptionBase):
    """
    이미 완료 처리가 된 숙명
    """
    code = ExceptionProcessCommand.code + 318


class ExceptionAlreadyCompleteAchievementCombatants(ExceptionBase):
    """
    이미 완료 처리가 된 숙명
    """
    code = ExceptionProcessCommand.code + 319


class ExceptionNotCompleteAchievementCombatants(ExceptionBase):
    """
    완료 조건을 만족 하지 못한 숙명
    """
    code = ExceptionProcessCommand.code + 320


class ExceptionFriendAlready(ExceptionBase):
    """
    이미 친구인 상대
    """
    code = ExceptionProcessCommand.code + 321


class ExceptionFriendAlreadyInvite(ExceptionBase):
    """
    이미 초대한 상대
    """
    code = ExceptionProcessCommand.code + 322


class ExceptionFriendAlreadyDelete(ExceptionBase):
    """
    이미 삭제한 상대
    """
    code = ExceptionProcessCommand.code + 323


class ExceptionFriendNot(ExceptionBase):
    """
    친구 아님
    """
    code = ExceptionProcessCommand.code + 324


class ExceptionFriendExceedApSent(ExceptionBase):
    """
    하루에 보낼 수 있는 단검 수를 초과함
    """
    code = ExceptionProcessCommand.code + 325


class ExceptionFriendExceed(ExceptionBase):
    """
    친구 수가 초과 되었음
    """
    code = ExceptionProcessCommand.code + 326


class ExceptionFriendAlreadyBlock(ExceptionBase):
    """
    이미 차단한 친구
    """
    code = ExceptionProcessCommand.code + 327


class ExceptionFriendNotBlock(ExceptionBase):
    """
    차단한 상대가 아님
    """
    code = ExceptionProcessCommand.code + 328


class ExceptionFriendBlocked(ExceptionBase):
    """
    차단한 친구목록에 들어 있음
    """
    code = ExceptionProcessCommand.code + 329


class ExceptionFriendAlreadySentApOnDay(ExceptionBase):
    """
    이미 친구에게 단검을 선물 했음
    """
    code = ExceptionProcessCommand.code + 330


class ExceptionFriendExceedInviteOnDay(ExceptionBase):
    """
    하루에 초대할 수 있는 친구 수를 초과한 상태
    """
    code = ExceptionProcessCommand.code + 331


class ExceptionFriendExceedForgetOnDay(ExceptionBase):
    """
    하루에 삭제할 수 있는 친구 수를 초과한 상태
    """
    code = ExceptionProcessCommand.code + 332


class ExceptionFriendExceedBlock(ExceptionBase):
    """
    총 차단 가능 친구 수 초과
    """
    code = ExceptionProcessCommand.code + 333


class ExceptionFriendExceedFriendCount(ExceptionBase):
    """
    친구를 더이상 초대 할수 없음
    """
    code = ExceptionProcessCommand.code + 334


class ExceptionInvalidDocumentKey(ExceptionBase):
    """
    조회하고자 하는 document 를 찾을 수 없음
    """
    code = ExceptionProcessCommand.code + 335


class ExceptionInvalidDefenseHead(ExceptionBase):
    """
    대표 캐릭터로 설정하고자 하는 캐릭터 키가 수비대에 존재하지 않음
    """
    code = ExceptionProcessCommand.code + 336


class ExceptionNotEnoughPvpPlayCount(ExceptionBase):
    """
    콜로세움 플레이 횟수 부족
    - args
    현재 횟수
    차감 횟수
    """
    code = ExceptionProcessCommand.code + 337


class ExceptionNotEnoughPvpPoint(ExceptionBase):
    """
    콜로세움 플레이 포인트 부족
    - args
    현재 점수
    차감 점수
    """
    code = ExceptionProcessCommand.code + 338


class ExceptionTooManyPvpLike(ExceptionBase):
    """
    좋아요 한도 초과
    """
    code = ExceptionProcessCommand.code + 339


class ExceptionAlreadySendPvpLike(ExceptionBase):
    """
    이미 오늘 좋아요를 보낸 유저
    """
    code = ExceptionProcessCommand.code + 340


class ExceptionTooManyPvpLikeReceived(ExceptionBase):
    """
    대상 유저가 받을 수 있는 좋아요 한도 초과
    """
    code = ExceptionProcessCommand.code + 341


class ExceptionSelfPvpLike(ExceptionBase):
    """
    본인에게 좋아요 보내기
    """
    code = ExceptionProcessCommand.code + 342


# 401 ~ 500: for sm and kanghoon
class ExceptionAlreadyRecvStarReward(ExceptionBase):
    """
    해당 스테이지 에 별클리어 보상을 이미 수령 함
    """
    code = ExceptionProcessCommand.code + 401


class ExceptionNotEnoughStar(ExceptionBase):
    """
    보상 받기에 필요한 별 개수가 부족함
    """
    code = ExceptionProcessCommand.code + 402


class ExceptionNotEnoughItem(ExceptionBase):
    """
    아이템을 사용 할 경우 필요 개수 만큼 보유 하고 있지 않을 때 발생 함
    """
    code = ExceptionProcessCommand.code + 403


class ExceptionEquipmentSlotIsFull(ExceptionBase):
    """
    장비 창이 가득 차서 더 이상 장비를 수령 할 수 없음
    """
    code = ExceptionProcessCommand.code + 404


class ExceptionInvalidItemGroup(ExceptionBase):
    """
    경험치 포션을 사용 하는 주체가 영웅 / 소환수 둘다 가 아닌 경우 발생 함
    """
    code = ExceptionProcessCommand.code + 405


class ExceptionInvalidUseCount(ExceptionBase):
    """
    아이템을 사용 할 때 사용 개수가 잘못 된 값이 올 경우 발생 함
    """
    code = ExceptionProcessCommand.code + 406


class ExceptionApIsFull(ExceptionBase):
    """
    이미 단검 주머니가 가득 차서 단검 물약을 사용 할 수 없음
    """
    code = ExceptionProcessCommand.code + 407


class ExceptionNotMatchRate(ExceptionBase):
    """
    랜덤박스 아이템에 확률이 맞지 않음
    """
    code = ExceptionProcessCommand.code + 408


class ExceptionCreateClan(ExceptionBase):
    """
    create_clan 함수에서 예외 발생
    """
    code = ExceptionProcessCommand.code + 409


class ExceptionGetClanList(ExceptionBase):
    """
    get_clan_list 함수에서 예외 발생
    """
    code = ExceptionProcessCommand.code + 410


class ExceptionJoinClan(ExceptionBase):
    """
    join_clan 함수에서 예외 발생
    """
    code = ExceptionProcessCommand.code + 411


class ExceptionLeaveClan(ExceptionBase):
    """
    leave_clan 함수에서 예외 발생
    """
    code = ExceptionProcessCommand.code + 412


class ExceptionChangeClanInfo(ExceptionBase):
    """
    change_clan_config 함수에서 예외 발생
    """
    code = ExceptionProcessCommand.code + 413


class ExceptionGetClanApplicantList(ExceptionBase):
    """
    get_clan_applicant_list 함수에서 예외 발생
    """
    code = ExceptionProcessCommand.code + 414


class ExceptionSelectClanApplicant(ExceptionBase):
    """
    select_clan_applicant 함수에서 예외 발생
    """
    code = ExceptionProcessCommand.code + 415


class ExceptionGiveClanCoin(ExceptionBase):
    """
    give_clan_coin 함수에서 예외 발생
    """
    code = ExceptionProcessCommand.code + 416


class ExceptionGetClanConfig(ExceptionBase):
    """
    get_clan_config 함수에서 예외 발생
    """
    code = ExceptionProcessCommand.code + 417


class ExceptionGetClanCoin(ExceptionBase):
    """
    get_clan_coin 함수에서 예외 발생
    """
    code = ExceptionProcessCommand.code + 418


class ExceptionGetClanTrophy(ExceptionBase):
    """
    get_clan_trophy 함수에서 예외 발생
    """
    code = ExceptionProcessCommand.code + 419


class ExceptionKickClanMember(ExceptionBase):
    """
    kick_clan_member 함수에서 예외 발생
    """
    code = ExceptionProcessCommand.code + 420


class ExceptionChangeClanRole(ExceptionBase):
    """
    change_clan_role 함수에서 예외 발생
    """
    code = ExceptionProcessCommand.code + 421


class ExceptionGiveLike(ExceptionBase):
    """
    give_like 함수에서 예외 발생
    """
    code = ExceptionProcessCommand.code + 422


class ExceptionRewardClanCoin(ExceptionBase):
    """
    reward_clan_coin 함수에서 예외 발생
    """
    code = ExceptionProcessCommand.code + 423


class ExceptionDonateFortFacility(ExceptionBase):
    """
    donate_fort_facility 함수에서 예외 발생
    """
    code = ExceptionProcessCommand.code + 424


class ExceptionChangeClanConfig(ExceptionBase):
    """
    set_config 함수에서 예외 발생
    """
    code = ExceptionProcessCommand.code + 425


class ExceptionGetClanLikeInfo(ExceptionBase):
    """
    get_clan_like_info 함수에서 예외 발생
    """
    code = ExceptionProcessCommand.code + 426


class ExceptionGetClanMemberList(ExceptionBase):
    """
    get_clan_member_list 함수에서 예외 발생
    """
    code = ExceptionProcessCommand.code + 427


class ExceptionGetClanReport(ExceptionBase):
    """
    get_clan_report 함수에서 예외 발생
    """
    code = ExceptionProcessCommand.code + 428


class ExceptionGetClanInfo(ExceptionBase):
    """
    get_clan_info 함수에서 예외 발생
    """
    code = ExceptionProcessCommand.code + 429


class ExceptionChangeMercenary(ExceptionBase):
    """
    change_mercenary 함수에서 예외 발생
    """
    code = ExceptionProcessCommand.code + 430


class ExceptionEmployMercenary(ExceptionBase):
    """
    employ_mercenary 함수에서 예외 발생
    """
    code = ExceptionProcessCommand.code + 431


class ExceptionAddEmployedMercenary(ExceptionBase):
    """
    add_employed_mercenary 함수에서 예외 발생
    """
    code = ExceptionProcessCommand.code + 432


class ExceptionChangeUserProfileImage(ExceptionBase):
    """
    change_user_profile_image 함수에서 예외 발생
    """
    code = ExceptionProcessCommand.code + 433


class ExceptionUpdateFieldBattleResult(ExceptionBase):
    """
    update_field_battle_result 함수에서 예외 발생
    """
    code = ExceptionProcessCommand.code + 434


class ExceptionStorageSrvUpdateObject(ExceptionBase):
    """
    storage_srv_update_object 함수에서 예외 발생
    """
    code = ExceptionProcessCommand.code + 435


class ExceptionStorageSrvAddObject(ExceptionBase):
    """
    storage_srv_add_object 함수에서 예외 발생
    """
    code = ExceptionProcessCommand.code + 436


class ExceptionInvestClanBuff(ExceptionBase):
    """
    invest_clan_buff 함수에서 예외 발생
    """
    code = ExceptionProcessCommand.code + 437


class ExceptionGetClanBuffInfo(ExceptionBase):
    """
    get_clan_buff_info 함수에서 예외 발생
    """
    code = ExceptionProcessCommand.code + 438


class ExceptionResetInvestedClanBuff(ExceptionBase):
    """
    reset_invested_clan_buff 함수에서 예외 발생
    """
    code = ExceptionProcessCommand.code + 439


class ExceptionClanIdIsNone(ExceptionBase):
    """
    혈맹 id가 None이 아니여야 하는데 None 값이 들어온 경우
    """
    code = ExceptionProcessCommand.code + 440


class ExceptionGiveClanTrophy(ExceptionBase):
    """
    give_clan_trophy 함수에서 예외 발생
    """
    code = ExceptionProcessCommand.code + 441


class ExceptionGetUserMercenaryList(ExceptionBase):
    """
    get_user_mercenary_list 함수에서 예외 발생
    """
    code = ExceptionProcessCommand.code + 442


class ExceptionBattleFieldClanReward(ExceptionBase):
    """
    battle_field_clan_reward 함수에서 예외 발생
    """
    code = ExceptionProcessCommand.code + 443


class ExceptionGiveLikeMember(ExceptionBase):
    """
    give_like_member 함수에서 예외 발생
    """
    code = ExceptionProcessCommand.code + 444


class ExceptionInvalidProductKey(ExceptionBase):
    """
        유효하지 않은 상품 키
    """
    code = ExceptionProcessCommand.code + 445


class ExceptionCannotPvpRevenge(ExceptionBase):
    """
        pvp 복수전을 할 수 없다
    """
    code = ExceptionProcessCommand.code + 446


class ExceptionCannotBuyApPotion(ExceptionBase):
    """
        ap 물약을 살 수 없다.
    """
    code = ExceptionProcessCommand.code + 447


class ExceptionClanNoAuth(ExceptionBase):
    """
    혈맹 간부가 아닌데 간부 명령을 요청한 경우
    """
    code = ExceptionProcessCommand.code + 448


class ExceptionPetBuffInactive(ExceptionBase):
    """
        펫 버프가 활성화 되어 있지 않다
    """
    code = ExceptionProcessCommand.code + 449


class ExceptionAlreadyPetBuffActive(ExceptionBase):
    """
        이미 펫 버프가 활성화 되어있슴
    """
    code = ExceptionProcessCommand.code + 450


class ExceptionNotYetPetBuffRewardTime(ExceptionBase):
    """
        펫 버프를 보상을 받을 시간이 아직 안됨
    """
    code = ExceptionProcessCommand.code + 451


class ExceptionCannotAddPetBuff(ExceptionBase):
    """
    펫 버프를 더 이상 추가 할 수 없다
    """
    code = ExceptionProcessCommand.code + 452


class ExceptionExistActivePetBuff(ExceptionBase):
    """
    이미 활성화된 펫 효과
    """
    code = ExceptionProcessCommand.code + 453


class ExceptionNeedEventID(ExceptionBase):
    """
    이벤트 id가 필요한 부분에 None 값이 들어온 경우
    """
    code = ExceptionProcessCommand.code + 454


class ExceptionDetectAbusing(ExceptionBase):
    """
        어뷰징이 검출됨
    """
    code = ExceptionProcessCommand.code + 455


class ExceptionCannotRechageTryCount(ExceptionBase):
    """
        스테이지 횟수 충전이 가능하지 않다
    """
    code = ExceptionProcessCommand.code + 456


class ExceptionCannotRechageStageDifficulty(ExceptionBase):
    """
        해당 스테이지가 횟수 충전 가능한 난이도가 아님
    """
    code = ExceptionProcessCommand.code + 457


class ExceptionApiGatePushEventFail(ExceptionBase):
    """
    플랫폼으로의 Puch 이벤트 미션 등록 요청이 실패함
    """
    code = ExceptionProcessCommand.code + 458


class ExceptionFreeForAllLackTryCount(ExceptionBase):
    """
    난투전 도전 횟수 부족
    """
    code = ExceptionProcessCommand.code + 459


class ExceptionFreeForAllInvalidBattle(ExceptionBase):
    """
    유효하지 않은 난투전 대결
    """
    code = ExceptionProcessCommand.code + 460


class ExceptionFreeForAllLackRechargeCost(ExceptionBase):
    """
    난투전 도전 횟수 재충전 비용 부족
    """
    code = ExceptionProcessCommand.code + 461


class ExceptionFreeForAllRemainTryCount(ExceptionBase):
    """
    난투전 도전 횟수가 아직 남아 있다.
    """
    code = ExceptionProcessCommand.code + 462


class ExceptionFreeForAllInvalidWinValue(ExceptionBase):
    """
    난투전 승패값이 유효하지 않음.
    """
    code = ExceptionProcessCommand.code + 463


class ExceptionFreeForAllInvalidDeck(ExceptionBase):
    """
    난투전 덱이 유효하지 않음.
    """
    code = ExceptionProcessCommand.code + 464


class ExceptionFreeForAllNotFoundTargetUser(ExceptionBase):
    """
    난투전 상대를 찾지 못했음.
    """
    code = ExceptionProcessCommand.code + 465


class ExceptionFreeForAllDeckIsNone(ExceptionBase):
    """
    난투전 덱 정보가 없음.
    """
    code = ExceptionProcessCommand.code + 466


class ExceptionExpiredEvent(ExceptionBase):
    """
       만료된 이벤트입니다
    """
    code = ExceptionProcessCommand.code + 467


class ExceptionWrongStageDifficuty(ExceptionBase):
    """
    잘못된 스테이지 난이도가 입력됨
    """
    code = ExceptionProcessCommand.code + 468


class ExceptionCannotUseMercenary(ExceptionBase):
    """
    도전 모드는 용병을 사용하지 못함
    """
    code = ExceptionProcessCommand.code + 469


class ExceptionCannotChangeHardStageMission(ExceptionBase):
    """
    도전 모드 미션을 변경할 수 없다. 이미 완료된 상태
    """
    code = ExceptionProcessCommand.code + 470


class ExceptionInvalidRankingType(ExceptionBase):
    """
    유효하지 않은 랭킹 타입
    """
    code = ExceptionProcessCommand.code + 471


class ExceptionNotHavePetBuff(ExceptionBase):
    """
    보유하지 않은 펫 버프
    """
    code = ExceptionProcessCommand.code + 472


class ExceptionNotEnoughPetBuffRemainTime(ExceptionBase):
    """
    펫 버프의 남은 시간이 충분하지 않음
    """
    code = ExceptionProcessCommand.code + 473


class ExceptionNotReservedPetBuff(ExceptionBase):
    """
    예약 된 펫 버프가 아님
    """
    code = ExceptionProcessCommand.code + 474


class ExceptionCannotCancelPetBuff(ExceptionBase):
    """
    펫 버프 예약을 취소할 수 없다
    """
    code = ExceptionProcessCommand.code + 475


class ExceptionChangeClanDungeonInfo(ExceptionBase):
    """
    clan dungeon 관련 lock document fail 등 동기화 관련 예외 발생시
    """
    code = ExceptionProcessCommand.code + 476


class ExceptionInvalidClanDungeonInfo(ExceptionBase):
    """
    clan dungeon 정보가 없거나 정상적이지 않을 경우
    """
    code = ExceptionProcessCommand.code + 476  # 동기화 이슈로 발생할 가능성이 있어 코드값은 동일하게..


class ExceptionExistClanDungeonRankReward(ExceptionBase):
    """
    clan dungeon 던전 클리어 순위 보상을 수령하지 않았음
    """
    code = ExceptionProcessCommand.code + 476  # 동기화 이슈로 발생할 가능성이 있어 코드값은 동일하게..


class ExceptionClanDungeonNoAuth(ExceptionBase):
    """
    clan dungeon 권한 없음
    """
    code = ExceptionProcessCommand.code + 476  # 동기화 이슈로 발생할 가능성이 있어 코드값은 동일하게..


class ExceptionBossClanDungeonNotOpen(ExceptionBase):
    """
    clan dungeon 보스 던전이 오픈 조건을 충족하지 못했음
    """
    code = ExceptionProcessCommand.code + 476  # 동기화 이슈로 발생할 가능성이 있어 코드값은 동일하게..


class ExceptionInvalidClanDungeonActiveUser(ExceptionBase):
    """
    clan dungeon 전투 진행중인 유저가 없거나 잘못됐음
    """
    code = ExceptionProcessCommand.code + 476  # 동기화 이슈로 발생할 가능성이 있어 코드값은 동일하게..


class ExceptionInvalidClanDungeonStatus(ExceptionBase):
    """
    clan dungeon 유효하지 않은 던전 상태
    """
    code = ExceptionProcessCommand.code + 476  # 동기화 이슈로 발생할 가능성이 있어 코드값은 동일하게..


class ExceptionClanDungeonBattleTimeOut(ExceptionBase):
    """
    혈맹던전 전투 시간 초과
    """
    code = ExceptionProcessCommand.code + 476  # 동기화 이슈로 발생할 가능성이 있어 코드값은 동일하게..


class ExceptionResetClanDungeonLackUserClanCoin(ExceptionBase):
    """
    clan dungeon 초기화 비용을 유저 기사단증표 포함 결재할 경우 유저가 보유한 기사단 증표수가 부족 할때
    """
    code = ExceptionProcessCommand.code + 477


class ExceptionClanDungeonLimitLevel(ExceptionBase):
    """
    clan dungeon 오픈 레벨이 되지 않았음
    """
    code = ExceptionProcessCommand.code + 478


class ExceptionClanDungeonInvalidFieldID(ExceptionBase):
    """
    clan dungeon 필드 id가 유효하지 않음
    """
    code = ExceptionProcessCommand.code + 479


class ExceptionClanDungeonInvalidTicketInfo(ExceptionBase):
    """
    clan dungeon 입장권 정보가 유효하지 않음
    """
    code = ExceptionProcessCommand.code + 480


class ExceptionInvalidClanDungeonType(ExceptionBase):
    """
    clan dungeon 타입이 유효하지 않음
    """
    code = ExceptionProcessCommand.code + 481


class ExceptionLackClanDungeonTicket(ExceptionBase):
    """
    clan dungeon 입장권 부족
    """
    code = ExceptionProcessCommand.code + 482


class ExceptionInvalidClanDungeonPhaseNo(ExceptionBase):
    """
    clan dungeon 전투 페이즈가 유효하지 않음
    """
    code = ExceptionProcessCommand.code + 483


class ExceptionInvalidClanDungeonDonateType(ExceptionBase):
    """
    clan dungeon 기부 타입이 유효하지 않음
    """
    code = ExceptionProcessCommand.code + 484


class ExceptionLackClanDungeonDonateExp(ExceptionBase):
    """
    clan dungeon 기부 경험치 부족
    """
    code = ExceptionProcessCommand.code + 485


class ExceptionAlreadyMaxClanDungeonDonateExp(ExceptionBase):
    """
    clan dungeon 기부 경험치가 이미 최대치임
    """
    code = ExceptionProcessCommand.code + 486


class ExceptionLackStruggleTowerTryCount(ExceptionBase):
    """
    투쟁의 탑 도전 횟수 부족
    """
    code = ExceptionProcessCommand.code + 487


class ExceptionStruggleTowerInvalidMatchTarget(ExceptionBase):
    """
    투쟁의 탑 유효하지 않은 상대
    """
    code = ExceptionProcessCommand.code + 488


class ExceptionStruggleTowerInvalidTeamDeck(ExceptionBase):
    """
    투쟁의 탑 유효하지 덱 
    """
    code = ExceptionProcessCommand.code + 489


class ExceptionClanDungeonIsNotClanMember(ExceptionBase):
    """
    혈맹원이 아니라서 혈맹던전 입장 불가
    """
    code = ExceptionProcessCommand.code + 490


class ExceptionStruggleTowerChangeSeason(ExceptionBase):
    """
    투쟁의 탑 시즌이 변경 됐음
    """
    code = ExceptionProcessCommand.code + 491


class ExceptionStruggleTowerInvalidTierInfo(ExceptionBase):
    """
    투쟁의 탑 티어 정보가 유효하지 않음
    """
    code = ExceptionProcessCommand.code + 492


class ExceptionStruggleTowerInvalidTargetInfo(ExceptionBase):
    """
    투쟁의 탑 상대 정보가 유효하지 않음
    """
    code = ExceptionProcessCommand.code + 493


class ExceptionStruggleTowerSeasonWaitTime(ExceptionBase):
    """
    투쟁의 탑 시즌 대기 시간에 전투 요청
    """
    code = ExceptionProcessCommand.code + 494


class ExceptionOverClanDonateTotalCount(ExceptionBase):
    """
    당일 clan 총 기부 가능 횟수 초과
    """
    code = ExceptionProcessCommand.code + 495


class ExceptionClandungeonExceedResetCount(ExceptionBase):
    """
    당일 clandungeon 초기화 횟수 초과
    """
    code = ExceptionProcessCommand.code + 496


# error 500 ~ 600 hyobong

# class ExceptionUserKick(ExceptionBase):
#     """
#         운영자에 의해 접속이 종료되었습니다
#     """
#     code = ExceptionProcessCommand.code + 500
#
#
# class ExceptionUnlockContents(ExceptionBase):
#     """
#         컨텐츠 점검으로 인하여 해당 컨텐츠를 이용할 수 없습니다. 자세한 내용은 공지사항을 확인해주세요.
#     """
#     code = ExceptionProcessCommand.code + 501


class ExceptionNotHaveCostume(ExceptionBase):
    """
       해당 소환수의 코스튬이 존재 하지 않습니다
    """
    code = ExceptionProcessCommand.code + 502


class ExceptionNotFoundPetEquipmentInfo(ExceptionBase):
    """
        해당 소환수의 장비 정보가 일치 하지 않습니다
    """
    code = ExceptionProcessCommand.code + 503


class ExceptionAlreadyOpenEquipment(ExceptionBase):
    """
        해당 소환수의 장비 정보가 일치 하지 않습니다
    """
    code = ExceptionProcessCommand.code + 504


class ExceptionMaxLevelEquipment(ExceptionBase):
    """
        해당 소환수의 장비 정보가 일치 하지 않습니다
    """
    code = ExceptionProcessCommand.code + 505


class ExceptionOverCount(ExceptionBase):
    """
    리퀘스트 파라미터 중 카운트가 오버 된 값이 올 경우
    """
    code = ExceptionProcessCommand.code + 506


class ExceptionClanMailCountMinus(ExceptionBase):
    """
    혈맹 메일 발송 시 일일 카운트 사용 다 함
    """
    code = ExceptionProcessCommand.code + 507


# error 600 ~ 700


class ExceptionNotMatchedSVN(ExceptionBase):
    """
    요청한 param을 가진 SVN Dir이 없음
    """
    code = ExceptionProcessCommand.code + 600


# error 700 ~ 800 jinhwi
class ExceptionAlreadyOpenTile(ExceptionBase):
    """
        이미 열려 있는 타일 입니다.
    """
    code = ExceptionProcessCommand.code + 700


class ExceptionNotHavePetID(ExceptionBase):
    """
        pet_id가 없습니다.
    """
    code = ExceptionProcessCommand.code + 701


class ExceptionNotCorrectTileIndex(ExceptionBase):
    """
        타일 인덱스 정보가 정확하지 않습니다.
    """
    code = ExceptionProcessCommand.code + 702


class ExceptionNotEnoughSecretStorageFreeCount(ExceptionBase):
    """
       비밀 창고 무료 열쇠가 부족 합니다.
    """
    code = ExceptionProcessCommand.code + 703


class ExceptionEnoughSecretStorageFreeCount(ExceptionBase):
    """
       비밀 창고 무료 열쇠 남아 있습니다.
    """
    code = ExceptionProcessCommand.code + 704


class ExceptionAlreadyRecvBingoReward(ExceptionBase):
    """
       이미 빙고 줄 보상을 받았습니다.
    """
    code = ExceptionProcessCommand.code + 705


class ExceptionDoNotRecvBingoReward(ExceptionBase):
    """
       빙고 줄 보상을 받을 수 없습니다.
    """
    code = ExceptionProcessCommand.code + 706


class ExceptionAlreadySelectedPetID(ExceptionBase):
    """
       이미 pet_id가 지정 되어 있습니다.
    """
    code = ExceptionProcessCommand.code + 707


class ExceptionWrongPetID(ExceptionBase):
    """
       pet_id가 잘못 되었습니다.
    """
    code = ExceptionProcessCommand.code + 708


class ExceptionNotExistSecretStorageNeedRefresh(ExceptionBase):
    """
       비밀창고 정보가 없습니다. 갱신이 필요 합니다.
    """
    code = ExceptionProcessCommand.code + 709


class ExceptionNotEnoughSecretStorageRechargeCount(ExceptionBase):
    """
       열쇠 충전 횟수가 부족합니다.
    """
    code = ExceptionProcessCommand.code + 710


class ExceptionNotEnoughDiaTrainingCount(ExceptionBase):
    """
       일일 다이아 연성 횟수 부족
    """
    code = ExceptionProcessCommand.code + 711


class ExceptionTargetLevelLowerThanNow(ExceptionBase):
    """
       목표 연성 레벨이 현재 레벨 보다 낮거나 같다
    """
    code = ExceptionProcessCommand.code + 712


class ExceptionNotEnoughNeedPetCount(ExceptionBase):
    """
       요구 소환수 보유 갯수가 부족 하다
    """
    code = ExceptionProcessCommand.code + 713


class ExceptionLimitedTrainingMaxLevel(ExceptionBase):
    """
       다이아 연성 최고 레벨 제한
    """
    code = ExceptionProcessCommand.code + 714


class ExceptionAlreadyMaxStrengthenEquipmentStep(ExceptionBase):
    """
        이미 최대 안전 강화 단계
    """
    code = ExceptionProcessCommand.code + 715


class ExceptionWrongSafetyStrengthenMaster(ExceptionBase):
    """
        안전 강화 마스터 데이터 문제( 저주/삭제가 발생)
    """
    code = ExceptionProcessCommand.code + 716


class ExceptionTargetStrengthenLowerThenEquipmentStrengthen(ExceptionBase):
    """
        목표 강화 단계가 장비의 강화단계 보다 낮다
    """
    code = ExceptionProcessCommand.code + 718


class ExceptionAlreadyTakenAchievementGuideCompleteCountReward(ExceptionBase):
    """
    이미 보상을 받아간 초보자 가이드
    """
    code = ExceptionProcessCommand.code + 719


class ExceptionNotEnoughAchievementGuideCompleteCount(ExceptionBase):
    """
    완료 조건을 만족하지 못함 - 초보자 가이드 업적 클리어 횟수
    """
    code = ExceptionProcessCommand.code + 720


class ExceptionInvalidAchievementGuideCompleteCount(ExceptionBase):
    """
    유효하지 않은 초보자 가이드 카운트 보상 키
    """
    code = ExceptionProcessCommand.code + 721


class ExceptionInvalidDiaGachaTime(ExceptionBase):
    """
    소환수 성장 소환석(고급 가챠: 저격가챠) 시간 정보가 유효하지 않습니다.
    """
    code = ExceptionProcessCommand.code + 722


class ExceptionInvalidDiaGachaDayOfWeek(ExceptionBase):
    """
    소환수 성장 소환석(고급 가챠: 저격가챠) 요일 정보가 유효하지 않습니다.
    """
    code = ExceptionProcessCommand.code + 723


# error 800 ~ 900 shirano
class ExceptionNotEnoughFreeRouletteTime(ExceptionBase):
    """
    무료 룰렛을 돌릴 시간이 되지 않았다.
    """
    code = ExceptionProcessCommand.code + 800


class ExceptionExceptionExpiredBuffKey(ExceptionBase):
    """
    현재 진행중이지 않은 버프 키이다
    """
    code = ExceptionProcessCommand.code + 801


class ExceptionNotEnoughFreeCount(ExceptionBase):
    """
    무료 횟수가 충분하지 않다
    """
    code = ExceptionProcessCommand.code + 802


class ExceptionExpiredEventKey(ExceptionBase):
    """
    만료되거나 존재하지 않는 이벤트 키이다.
    """
    code = ExceptionProcessCommand.code + 803


class ExceptionWrongClanGachaRewardStep(ExceptionBase):
    """
    클랜 가챠 보상 단계 입력이 잘못 되었다
    """
    code = ExceptionProcessCommand.code + 804


class ExceptionNotEnoughGachaPoint(ExceptionBase):
    """
    가챠 포인트가 비용을 지불하기에 부족함
    """
    code = ExceptionProcessCommand.code + 805


class ExceptionInvalidEvent(ExceptionBase):
    """
    현재 유효하지 않은 이벤트이다
    """
    code = ExceptionProcessCommand.code + 806


class ExceptionClosedEquipmentBox(ExceptionBase):
    """
    닫혀있는 장비함이다
    """
    code = ExceptionProcessCommand.code + 807


class ExceptionAlreadyOpenedEquipmentBox(ExceptionBase):
    """
    이미 열린 장비함이다.
    """
    code = ExceptionProcessCommand.code + 808


class ExceptionCannotOpenEquipmentBox(ExceptionBase):
    """
    장비함을 열 수 없다. (영웅이 없다든지..)
    """
    code = ExceptionProcessCommand.code + 809


class ExceptionCannotActivateEquipmentBoxStat(ExceptionBase):
    """
    장비 효과를 활성화 할 수 없다
    """
    code = ExceptionProcessCommand.code + 810


class ExceptionAlreadyOpenedMasteryGroup(ExceptionBase):
    """
    이미 열린 마스터리 그룹이다
    """
    code = ExceptionProcessCommand.code + 811


class ExceptionClosedMasteryGroup(ExceptionBase):
    """
    닫혀있는 마스터리 그룹이다
    """
    code = ExceptionProcessCommand.code + 812


class ExceptionNotEnoughCondition(ExceptionBase):
    """
    마스터리 오픈에 필요한 조건이 갖춰지지 않았다
    """
    code = ExceptionProcessCommand.code + 813


class ExceptionCannotFindPreviousMasteryGroup(ExceptionBase):
    """
    이전 단계 마스터리 그룹 정보를 찾을 수 없다. 데이터가 꼬인 경우
    """
    code = ExceptionProcessCommand.code + 814


class ExceptionWrongMasteryLevel(ExceptionBase):
    """
    잘못된 마스터리 레벨 값이다
    """
    code = ExceptionProcessCommand.code + 815


class ExceptionCannotReceiveClanGachaReward(ExceptionBase):
    """
    보상 인원 초과로 보상을 받을 수 없다.
    """
    code = ExceptionProcessCommand.code + 816


class ExceptionPreviousPvpTarget(ExceptionBase):
    """
    이전 pvp 대상이여서 매칭이 불가함
    """
    code = ExceptionProcessCommand.code + 817


class ExceptionWrongPvpTarget(ExceptionBase):
    """
    잘못된 pvp 대상이다. 시작시 주어진 대상 목록에 존재하지 않는다.
    """
    code = ExceptionProcessCommand.code + 818


class ExceptionCannotFindWeeklyPvpSeasonData(ExceptionBase):
    """
    주간 pvp 시즌 정보를 찾을 수 없다.
    """
    code = ExceptionProcessCommand.code + 819


class ExceptionWrongEnemySeasonInfo(ExceptionBase):
    """
    주간 pvp에서 상대방의 시즌 정보가 잘못 되었다. 내 시즌 정보와 다르다.
    """
    code = ExceptionProcessCommand.code + 829


class ExceptionNotEnoughGambleTicket(ExceptionBase):
    """
    주간 pvp 겜블 티켓이 모자르다
    """
    code = ExceptionProcessCommand.code + 830


class ExceptionWeeklyPvpLackTryCount(ExceptionBase):
    """
    주간 pvp 도전 횟수 부족
    """
    code = ExceptionProcessCommand.code + 831


class ExceptionWrongEnemyWeeklyPvpSeason(ExceptionBase):
    """
    상대의 시즌 정보가 잘못 되었다
    """
    code = ExceptionProcessCommand.code + 832


class ExceptionWrongWeeklyPvpDeck(ExceptionBase):
    """
    주간 pvp 덱 구성이 잘못 되었다
    """
    code = ExceptionProcessCommand.code + 833


class ExceptionNotRegistedMercenary(ExceptionBase):
    """
    상대 용병 정보에 등록된 펫이 아니다
    """
    code = ExceptionProcessCommand.code + 834


class ExceptionNotHaveMercenary(ExceptionBase):
    """
    용병을 빌리려는 사람에게 존재하지 않는 펫이다.
    """
    code = ExceptionProcessCommand.code + 835


class ExceptionInvaildMercenaryLevel(ExceptionBase):
    """
    유효하지 않은 용병 레벨이다. 내 레벨에 비해 너무 높다
    """
    code = ExceptionProcessCommand.code + 836


class ExceptionNeedToRefreshTargetList(ExceptionBase):
    """
    상대 정보에 문제가 있어서, 상대 목록 재검색이 필요하다
    """
    code = ExceptionProcessCommand.code + 837


class ExceptionNotRegistedWeeklyPvpDeck(ExceptionBase):
    """
    주간 pvp 덱이 설정되어 있지 않다.
    """
    code = ExceptionProcessCommand.code + 838


class ExceptionAlreadyFinishedSeason(ExceptionBase):
    """
    주간 pvp 시즌이 종료되어 결과가 적용되지 않는다.
    """
    code = ExceptionProcessCommand.code + 839


class ExceptionNotEnoughArenaCoin(ExceptionBase):
    """
    아레나 코인이 부족하다
    """
    code = ExceptionProcessCommand.code + 840


class ExceptionWrongWeeklyPvpRechargeCount(ExceptionBase):
    """
    주간 아레나 충전하려는 횟수값이 잘못 되었다.
    """
    code = ExceptionProcessCommand.code + 841


class ExceptionInvalidEventFlow(ExceptionBase):
    """
    이벤트 호출의 순서가 잘못 되었다.
    """
    code = ExceptionProcessCommand.code + 842


class ExceptionInvalidBoostingCardIndex(ExceptionBase):
    """
    선택한 부스팅 카드의 인덱스가 유효하지 않다
    """
    code = ExceptionProcessCommand.code + 843


class ExceptionNotEnoughCardSelectCount(ExceptionBase):
    """
    부스팅 이벤트에서 카드 뽑기 횟수가 충분하지 않다
    """
    code = ExceptionProcessCommand.code + 844


# 901~999 by ozzywow
class ExceptionExtortFortHasNotAttackPermission(ExceptionBase):
    """
    해당 요새에 공격할 권한을 갖고있지 않음
    """
    code = ExceptionProcessCommand.code + 901


class ExceptionExtortFortEnd(ExceptionBase):
    """
    해당 요새는 이미 쟁탈전이 끝났음!
    """
    code = ExceptionProcessCommand.code + 902


class ExceptionExtortFortOverCountHas(ExceptionBase):
    """
    이미 소유하고있는 요새와 진행중인 쟁탈전의 합이 3를 넘는다. 
    """
    code = ExceptionProcessCommand.code + 903


class ExceptionExtortFortInvalidValue(ExceptionBase):
    """
    특정 값이 유효하지 않을때.. 
    """
    code = ExceptionProcessCommand.code + 904


class ExceptionExtortFortReadyToDeclare(ExceptionBase):
    """
    요새쟁탈전 선포를 기다리는중..
    """
    code = ExceptionProcessCommand.code + 905


# error 1001 ~ 1100 aramch17
class ExceptionStackableMaxCount(ExceptionBase):
    """
    아이템 보유 한도 초과
    """
    code = ExceptionProcessCommand.code + 1001


class ExceptionNotEnoughToSatisfyStackAttendanceRewardCondition(ExceptionBase):
    """
    누적 출석 보상 받을 조건을 충족하지 못함
    """
    code = ExceptionProcessCommand.code + 1002


class ExceptionNotFoundStackAttendanceReward(ExceptionBase):
    """
    누적 출석 보상을 찾을 수 없음
    """
    code = ExceptionProcessCommand.code + 1003


class ExceptionAlreadyPurchasedSTWKeepRewardBoost(ExceptionBase):
    """
    투쟁의 탑 재화 생산 부스트가 이미 적용됨
    """
    code = ExceptionProcessCommand.code + 1004


class ExceptionAlreadyReceivedReward(ExceptionBase):
    """
    이미 보상을 받음
    """
    code = ExceptionProcessCommand.code + 1005


class ExceptionNotYetReceiveRewardTime(ExceptionBase):
    """
    아직 보상을 받을 시간이 아님
    """
    code = ExceptionProcessCommand.code + 1006


class ExceptionWrongRewardInfoNeedRefresh(ExceptionBase):
    """
    보상 정보 갱신 필요
    """
    code = ExceptionProcessCommand.code + 1007


class ExceptionReceiveStruggleTowerReward(ExceptionBase):
    """
    투쟁의 탑 보상 획득 처리 중 익셉션 발생
    """
    code = ExceptionProcessCommand.code + 1008


class ExceptionStruggleTowerNeedRegister(ExceptionBase):
    """
    투쟁의 탑 랭킹 정보가 없음
    """
    code = ExceptionProcessCommand.code + 1009


class ExceptionBuyCountLimitPerItem(ExceptionBase):
    """
    상품별 구매 가능 횟수 초과
    """
    code = ExceptionProcessCommand.code + 1010


class ExceptionNotEnoughDrawWordPoint(ExceptionBase):
    """
    룬문자 뽑기 포인트 부족
    """
    code = ExceptionProcessCommand.code + 1011


class ExceptionDrawWordLimitTodayCount(ExceptionBase):
    """
    오늘 룬문자 뽑기 가능한 횟수 모두 사용
    """
    code = ExceptionProcessCommand.code + 1012


class ExceptionNotEnoughReplaceWordCount(ExceptionBase):
    """
    룬문자 교환 횟수 부족
    """
    code = ExceptionProcessCommand.code + 1013


class ExceptionNotFoundSTWReward(ExceptionBase):
    """
    보상 정보를 찾을 수 없음
    """
    code = ExceptionProcessCommand.code + 1014


class ExceptionAlreadyDoneRuneWords(ExceptionBase):
    """
    이미 모든 문자가 완성되어 있음, 교환 불가
    """
    code = ExceptionProcessCommand.code + 1015


class ExceptionRemainRuneWordFreeReplaceCount(ExceptionBase):
    """
    룬 문자 무료 교환 횟수가 남아 있음
    """
    code = ExceptionProcessCommand.code + 1016


class ExceptionNotEnoughExchangeCount(ExceptionBase):
    """
    교환 가능한 횟수가 없음
    """
    code = ExceptionProcessCommand.code + 1017


class ExceptionNotEnoughExchangeBaseItem(ExceptionBase):
    """
    교환할 아이템이 부족함
    """
    code = ExceptionProcessCommand.code + 1018


class ExceptionNotUsedExchangeBaseItem(ExceptionBase):
    """
    해당 아이템을 재료료 사용할 수 없음
    """
    code = ExceptionProcessCommand.code + 1019


class ExceptionOverflowExchangeBaseItem(ExceptionBase):
    """
    재료료 사용할 아이템 보다 더 많이 들어옴
    """
    code = ExceptionProcessCommand.code + 1020


# error 1100 ~  yukuns
class ExceptionCannotChargeFreeAp(ExceptionBase):
    """
    무료 단검을 충전할 수 없음
    """
    code = ExceptionProcessCommand.code + 1100


class ExceptionNotEnoughPlayCount(ExceptionBase):
    """
    콜로세움 일일보상시의 조건인 play count가 부족
    """
    code = ExceptionProcessCommand.code + 1101


class ExceptionAlreadyTakenDailyReward(ExceptionBase):
    """
    콜로세움 일일보상시 이미 받은 보상
    """
    code = ExceptionProcessCommand.code + 1102


class ExceptionMismatchDailyRewardKey(ExceptionBase):
    """
    콜로세움 일일보상시 클라이언트와 서버간에 맞지 않는 보상키
    """
    code = ExceptionProcessCommand.code + 1103


# ### IMPRINT ###############################################################################################
# class ExceptionInvalidImprintPhase(ExceptionBase):
#     """
#     [각인] 유효하지 않는 각인 단계
#     """
#     code = ExceptionProcessCommand.code + 1104
#
#
# class ExceptionInvalidImprint(ExceptionBase):
#     """
#     [각인] 유효하지 않는 각인
#     """
#     code = ExceptionProcessCommand.code + 1105
# ### IMPRINT ###############################################################################################

# 다이아 룰렛 : 1201~1300
class ExceptionOverTryCount(ExceptionBase):
    """
    [다이아 룰렛] 룰렛 도전횟수 초과
    """
    code = ExceptionProcessCommand.code + 1201


class ExceptionDiaRouletteMasterData(ExceptionBase):
    """
    [다이아 룰렛] 마스터 데이터 오류
    """
    code = ExceptionProcessCommand.code + 1202


# request exception
class ExceptionNeedLogin(ExceptionBase):
    """
    로그인이 되지 않음. 애초에 로그인 하지 않았거나, 만료되었음.
    """
    code = ExceptionRequest.code + 1


class ExceptionNotEnoughRequestParameter(ExceptionBase):
    """
    클라-서버간 요청 시 기본으로 필요한 정보가 충족되지 않음. 프로토콜 오류. 주로 개발단계에서만 발생 가능하며, 서비스 시에는 발생하지 않을 것으로 추정.
    """
    code = ExceptionRequest.code + 2


class ExceptionFailToSave(ExceptionBase):
    """
    데이터베이스 저장 실패
    """
    code = ExceptionRequest.code + 3


class ExceptionNoCommandHandler(ExceptionBase):
    """
    요청한 명령이 존재하지 않음. 서버 세팅이 잘못되었거나, 클라 요청이 잘못됨. 주로 개발단계에서만 발생 가능하며, 서비스 시에는 발생하지 않을 것으로 추정.
    """
    code = ExceptionRequest.code + 4


class ExceptionInvalidXigncode(ExceptionBase):
    """
    xign code 가 유효하지 않음
    """
    code = ExceptionRequest.code + 5


class ExceptionKickAllUser(ExceptionBase):
    """
        모든 유저 접속을 차단함. 주로 점검 상태. 운영에서 지정
    """
    code = ExceptionRequest.code + 6


class ExceptionBlockUser(ExceptionBase):
    """
        블락 된 유저입니다. 주로 처벌 상태. 운영에서 지정
    """
    code = ExceptionRequest.code + 7


class ExceptionUserKick(ExceptionBase):
    """
        운영자에 의해 접속이 종료되었습니다. 주로 처벌 상태. 운영에서 지정
    """
    code = ExceptionRequest.code + 8


class ExceptionUnlockContents(ExceptionBase):
    """
        컨텐츠 점검으로 인하여 해당 컨텐츠를 이용할 수 없습니다. 자세한 내용은 공지사항을 확인해주세요.
    """
    code = ExceptionRequest.code + 9


class ExceptionDatabaseLockTimeout(ExceptionRequest):
    """
        카우치베이스 저장을 위한 lock ttl 시간이 초과되었음. 요청 처리에 시간이 오래 걸려서 발생하는 오류.
    """
    code = ExceptionRequest.code + 10


# modify by ZHM, JoyGames, ALPHA GROUP CO.,LTD, at 2017-08-23
# >>>>>>>>>>>>>
class ExceptionBanChannel(ExceptionBase):
    """
        渠道限制
    """
    code = ExceptionRequest.code + 9998
# <<<<<<<<<<<<<

# modify by Yoray, JoyGames, ALPHA GROUP CO.,LTD, at 2017-05-04
# detail: 增加客户端版本限制
# >>>>>>>>>>>>>
class ExceptionClientVersion(ExceptionBase):
    """
        客户端版本限制
    """
    code = ExceptionRequest.code + 9999
# <<<<<<<<<<<<<


# >>add by ZHM, JoyGames, ALPHA GROUP CO.,LTD, at 2017-04-06 for 定义项目组自己的code从50000开始
class ExceptionTradeDownFail(ExceptionBase):
    """
    交易行下架商品失败，可能被其他玩家买了
    """
    code = ExceptionAOFEI.code + 1


class ExceptionTradeIndexFull(ExceptionBase):
    """
    交易行上架空间已满
    """
    code = ExceptionAOFEI.code + 2

class ExceptionItemNoTradable(ExceptionBase):
    """
    道具不可上架
    """
    code = ExceptionAOFEI.code + 3

class ExceptionNoStack(ExceptionBase):
    """
    材料不存在
    """
    code = ExceptionAOFEI.code + 4

class ExceptionWrongPrice(ExceptionBase):
    """
    价格超出上下限
    """
    code = ExceptionAOFEI.code + 5

class ExceptionWrongOrderid(ExceptionBase):
    """
    错误的订单号
    """
    code = ExceptionAOFEI.code + 6

class ExceptionOrderNoEnd(ExceptionBase):
    """
    订单未过期
    """
    code = ExceptionAOFEI.code + 7

class ExceptionNoOrderToBuy(ExceptionBase):
    """
    商品不存在，无法购买
    """
    code = ExceptionAOFEI.code + 8

class ExceptionNoBuySelfOrder(ExceptionBase):
    """
    无法购买自己的商品
    """
    code = ExceptionAOFEI.code + 9

class ExceptionNoEnoughOrderCount(ExceptionBase):
    """
    商品数量不足
    """
    code = ExceptionAOFEI.code + 10

class ExceptionOrderEnd(ExceptionBase):
    """
    商品已过期，无法购买
    """
    code = ExceptionAOFEI.code + 11

class ExceptionNotDebugLogin(ExceptionBase):
    """
    不可使用Debug LoginD
    """
    code = ExceptionAOFEI.code + 12


# 队伍相关从 + 1000开始
class ExceptionHasNoTeam(ExceptionBase):
    """
    没有队伍
    """
    code = ExceptionAOFEI.code + 1000


class ExceptionNoTeamBossTime(ExceptionBase):
    """
    不在team boss活动时间
    """
    code = ExceptionAOFEI.code + 1001


class ExceptionTeamBossNoData(ExceptionBase):
    """
    没有team boss 数据
    """
    code = ExceptionAOFEI.code + 1002


class ExceptionTeamBossFirstStageFinish(ExceptionBase):
    """
    第一阶段已结束
    """
    code = ExceptionAOFEI.code + 1003


class ExceptionTeamBossFirstStageInBattle(ExceptionBase):
    """
    有人在战斗中
    """
    code = ExceptionAOFEI.code + 1004


class ExceptionTeamBossFirstStageTimeout(ExceptionBase):
    """
    战斗超时
    """
    code = ExceptionAOFEI.code + 1005


class ExceptionNotTeamLeader(ExceptionBase):
    """
    不是队长
    """
    code = ExceptionAOFEI.code + 1006


class ExceptionLeaderNotOpen(ExceptionBase):
    """
    队长未开启
    """
    code = ExceptionAOFEI.code + 1007


class ExceptionTeamBossAlreadyOpened(ExceptionBase):
    """
    已开启
    """
    code = ExceptionAOFEI.code + 1008


class ExceptionTeamBossHasBattleGoing(ExceptionBase):
    """
    战斗正在进行中
    """
    code = ExceptionAOFEI.code + 1009


# 原有业务逻辑相关从 + 2000开始
class ExceptionEmployedMercenaryMaxTimes(ExceptionBase):
    """
    战斗正在进行中
    """
    code = ExceptionAOFEI.code + 2000

# <<add by ZHM, JoyGames, ALPHA GROUP CO.,LTD, at 2017-04-06 for 定义项目组自己的code从50000开始





import sys
import traceback


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
        e=e.decode("utf-8","ignore")
        for line in e.split('\n'):
            result['call stack'].append(line)

    print 'ERROR:',
    for each in args:
        print each,
    for k, v in kwargs.iteritems():
        print k, '=', v, ',',
    print ':END'

    # exc_type, exc_value, exc_traceback = sys.exc_info()
    for line in traceback.format_exception(exc_type, exc_value, exc_traceback):
        print line,

    #>>>add by ZHM, JoyGames, ALPHA GROUP CO.,LTD, at 2017-05-19 for 抛出异常时增加local打印
    exc_tb = exc_traceback
    while exc_tb:
        locals_arg = exc_tb.tb_frame.f_locals
        exc_tb = exc_tb.tb_next
    print "LOCALS:", locals_arg
    #<<<add by ZHM, JoyGames, ALPHA GROUP CO.,LTD, at 2017-05-19 for 抛出异常时增加local打印

    return result
