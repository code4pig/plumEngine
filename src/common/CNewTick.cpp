#include "common/CNewTick.h"
#include "common/CNewTickMgr.h"

namespace common
{
	CNewTick::CNewTick() :m_uInterval(0), m_pTickMgr(NULL), m_pTickEntry(NULL)
	{
		m_pstrTickName = new std::string("newtick");
	}

	CNewTick::~CNewTick(void)
	{
		UnRegister();
		SAFE_DELETE(m_pstrTickName);
	}

	bool CNewTick::IsRegistered() const
	{
		if (m_pTickEntry)
			return m_pTickEntry->bIsValid;
		return false;
	}

	const char* CNewTick::GetTickName() const
	{ 
		return m_pstrTickName->c_str(); 
	}

	void CNewTick::UnRegister()
	{
		if (m_pTickEntry != NULL)
		{
			m_pTickMgr->UnRegister(this);
			m_pTickEntry = NULL;
		}
	}
}