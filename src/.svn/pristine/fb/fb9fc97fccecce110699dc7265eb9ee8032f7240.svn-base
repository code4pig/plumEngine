#include <iostream>
#include "gperftools/profiler.h"
#include "plum/CPlum.h"

using namespace plum;

int main(int argc, char* argv[])
{
	int nRet = 0;
	const char* szName = NULL;
	const char* szConf = "";
	const char* szProf = NULL;
    const char* szLog = NULL;

	if (argc < 3)
	{
		std::cout << "usage:./plum appname configfile [profpath] [logdir]" << std::endl;
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
		//linux下链接libtcmalloc_and_profiler.a和-lunwind
		//pprof --text ./plum gateway.prof
		//pprof --pdf ./plum gateway.prof > gateway.pdf #依赖sudo yum install graphviz生成pdf
#ifdef USE_TCMALLOC
        ProfilerStart(szProf);
#endif
    }
	CPlum::GetInstance()->Init(szName, szConf, szLog);
	nRet = CPlum::GetInstance()->Run();
	CPlum::GetInstance()->UnInit();
	CPlum::Release();
    if (szProf != NULL)
    {
#ifdef USE_TCMALLOC
        ProfilerStop();
#endif
    }
	return nRet;
}
