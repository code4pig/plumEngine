#include "mtplum/CMtPlum.h"
#include "common/common.h"

namespace mtplum
{
	static CMtPlum* g_pMtPlum = NULL;

	CMtPlum::CMtPlum()
	{

	}

	CMtPlum::~CMtPlum()
	{

	}

	CMtPlum* CMtPlum::GetInstance()
	{
		if (g_pMtPlum == NULL)
		{
			g_pMtPlum = new CMtPlum();
		}
		return g_pMtPlum;
	}

	void CMtPlum::Release()
	{
		SAFE_DELETE(g_pMtPlum);
	}

}