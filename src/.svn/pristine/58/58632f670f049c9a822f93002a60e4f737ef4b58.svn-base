#include "common/CNewTimeSystem.h"
#include "common/CAdvanceTick.h"

namespace common
{
	CNewTimeSystem::CNewTimeSystem(uint32 uBaseCyc)
		:m_pTickMgr(NULL)
		,m_uLogicBaseTime(0)
		,m_uLogicTime(0)
		,m_uPushCount(0)
		,m_bStop(false)
	{
		m_pTickMgr = new CNewTickMgr(uBaseCyc);
		Reset();
	}

	CNewTimeSystem::~CNewTimeSystem()
	{
		SAFE_DELETE(m_pTickMgr);
	}

	void CNewTimeSystem::Init(uint32 uBaseCyc)
	{ 
		Inst() = new CNewTimeSystem(uBaseCyc); 
	}

	void CNewTimeSystem::Unit()
	{ 
		SAFE_DELETE(Inst()); 
	}

	CNewTimeSystem*& CNewTimeSystem::Inst()
	{ 
		static CNewTimeSystem* ls_Inst = NULL;
		return ls_Inst; 
	}

	void CNewTimeSystem::Register(CNewTick* pTick, uint32 uCyc, const char* szName)
	{ 
		m_pTickMgr->Register(pTick, uCyc, szName); 
	}

	void CNewTimeSystem::UnRegister(CNewTick* pTick)
	{ 
		m_pTickMgr->UnRegister(pTick); 
	}

	//注册tick
	void CNewTimeSystem::Register(CAdvanceTick* pAdvanceTick,uint32 uBeginTime,uint32 uCyc,const char* szName)
	{
		pAdvanceTick->m_pTimeSystem = this;
		pAdvanceTick->m_uBeginTime = uBeginTime;
		pAdvanceTick->m_uCyc = uCyc;

		if( 0 != uBeginTime )
		{
			pAdvanceTick->m_bFirstTick = true;
			Register(pAdvanceTick,uBeginTime,szName);
		}
		else
		{
			pAdvanceTick->m_bFirstTick = false;
			Register(pAdvanceTick,uCyc,szName);
		}
	}

	int32 CNewTimeSystem::PushLogicTime(uint64 uRealTime)
	{
		if (m_bStop)
			return 0;
		uint32 uInterval = m_pTickMgr->GetInterval();
		uint64 uTotal = uRealTime - GetBaseTime();
		uint64 uMustPushCount = uTotal / uInterval + 1;		//计算一共需推动多少次. +1 注册后确保会被推一次
		int32 uEnd = int32(uMustPushCount - m_uPushCount);//计算当前需要推动多少次
		for (int32 n = 0; n < uEnd; ++n)
		{
			m_pTickMgr->OnTick();
			m_uLogicTime += uInterval;
			++m_uPushCount;
		}
		return uEnd;
	}
}
