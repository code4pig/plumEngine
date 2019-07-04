#include <iostream>
#include "mtplum/CMtPlum.h"
#include "gperftools/profiler.h"

using namespace mtplum;

int main(int argc, char* argv[])
{
	const char* szName = NULL;
	const char* szConf = "";
	const char* szProf = NULL;
	const char* szLog = NULL;

	if (argc < 3)
	{
		std::cout << "usage:./mtplum appname configfile [profpath] [logdir]" << std::endl;
		abort();
		return -1;
	}
	szName = argv[1];
	szConf = argv[2];
	if (argc > 3)
	{
		szProf = argv[3];
	}
	if (argc > 4)
	{
		szLog = argv[4];
	}
	if (szProf != NULL)
	{
#ifdef USE_TCMALLOC
		ProfilerStart(szProf);
#endif
	}
	CMtPlum::GetInstance()->Init(szName, szConf, szLog);
	CMtPlum::GetInstance()->Run();
	CMtPlum::GetInstance()->UnInit();
	CMtPlum::Release();
	if (szProf != NULL)
	{
#ifdef USE_TCMALLOC
		ProfilerStop();
#endif
	}
	return 0;
}