#include "common/CAdvanceTick.h"
#include "common/CNewTimeSystem.h"

namespace common
{
CAdvanceTick::CAdvanceTick(void)
:m_pTimeSystem(NULL)
,m_uBeginTime(0)
,m_uCyc(0)
,m_bFirstTick(false)
{
}

CAdvanceTick::~CAdvanceTick(void)
{
}

void CAdvanceTick::OnTick()
{
	if(m_bFirstTick)
	{
		m_bFirstTick = false;
		m_pTimeSystem->UnRegister(this);
		m_pTimeSystem->Register( this, m_uCyc, GetTickName() );
	}
}

}
