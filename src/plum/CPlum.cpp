#include "plum/CPlum.h"
#include "common/common.h"

namespace plum
{
	static CPlum* g_pPlum = NULL;

	CPlum::CPlum()
	{

	}

	CPlum::~CPlum()
	{

	}

	CPlum* CPlum::GetInstance()
	{
		if (g_pPlum == NULL)
		{
			g_pPlum = new CPlum();
		}
		return g_pPlum;
	}

	void CPlum::Release()
	{
		SAFE_DELETE(g_pPlum);
	}

}