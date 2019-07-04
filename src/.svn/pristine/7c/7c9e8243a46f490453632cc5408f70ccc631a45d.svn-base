#ifdef _WIN32
#include <Windows.h>
#include <sys/timeb.h>
#else
#include <time.h>
#endif
#include "common/CTime.h"

namespace common{

	static CTime *g_pYyTime = NULL;

	uint64 CTime::ms_uBaseTime = 0;
#ifdef _WIN32
	LARGE_INTEGER CTime::ms_uFrequency = { 0 };
#endif

	CTime* CTime::Instance()
	{

		if (!g_pYyTime)
			g_pYyTime = new CTime;
		return g_pYyTime;
	}

	void CTime::Release()
	{
		SAFE_DELETE(g_pYyTime);
	}

	CTime::CTime()
	{
		m_uFastTimeTickInMS = 0;
		m_uFastUTCTimeInMS = 0;
		m_uFastUTCTimeInSec = 0;

#ifdef _WIN32
		LARGE_INTEGER uCounter;
		HANDLE hThread = ::GetCurrentThread();
		DWORD_PTR oldmask = ::SetThreadAffinityMask(hThread, 0x00000001);
		QueryPerformanceFrequency(&ms_uFrequency);
		QueryPerformanceCounter(&uCounter);
		::SetThreadAffinityMask(hThread, oldmask);

		ms_uBaseTime = uCounter.QuadPart;

#elif defined __linux__
		timespec ts;
		if (-1 == clock_gettime(CLOCK_MONOTONIC, &ts))
		{
			return;
		}
		ms_uBaseTime = ((uint64)ts.tv_sec) * 1000 + ts.tv_nsec/1000000;
#endif
	}

	uint64 CTime::GetTimeTickInMS()
	{
#ifdef _WIN32
		LARGE_INTEGER uTime;
		HANDLE hThread = ::GetCurrentThread();
		DWORD_PTR oldmask = ::SetThreadAffinityMask(hThread, 0x00000001);
		QueryPerformanceCounter(&uTime);
		::SetThreadAffinityMask(hThread, oldmask);

		uint64 nDelta = ((uint64)uTime.QuadPart) - ms_uBaseTime;
		return nDelta * 1000 / ms_uFrequency.QuadPart;

#elif defined __linux__
		timespec ts;
		if (-1 == clock_gettime(CLOCK_MONOTONIC, &ts))
		{
			return 0;
		}
		return ((uint64)ts.tv_sec) * 1000 + ts.tv_nsec/1000000 - ms_uBaseTime;

#else
		return 0;
#endif
	}

	// fast time
	void CTime::UpdateFastTime(void)
	{
		uint64 uTmpTickMs = GetTimeTickInMS();
		if (m_uFastTimeTickInMS < uTmpTickMs)
		{
			//防止多核时可能出现的时间不一致
			m_uFastTimeTickInMS = uTmpTickMs;
		}

#ifdef _WIN32
		struct __timeb64 timebuffer;
		_ftime64(&timebuffer);
		m_uFastUTCTimeInSec = timebuffer.time;
		m_uFastUTCTimeInMS = timebuffer.time * 1000 + timebuffer.millitm;

#else
		timespec ts;
		if (clock_gettime(CLOCK_REALTIME, &ts) != -1)
		{
			m_uFastUTCTimeInSec = ts.tv_sec;
			m_uFastUTCTimeInMS = ((uint64)ts.tv_sec) * 1000 + ts.tv_nsec / 1000000;
		}
#endif
	}

	//==================================================================================================

	// 返回：从UTC时间1970-01-01 08:00:00起累计的时间
	uint64 GetUTCTimeInSec()
	{
#ifdef _WIN32
		struct __timeb64 timebuffer;
		_ftime64(&timebuffer);
		return timebuffer.time;

#else
		timespec ts;
		if (-1 == clock_gettime(CLOCK_REALTIME, &ts))
		{
			return 0;
		}
		return ts.tv_sec;
#endif
	}

	uint64 GetUTCTimeInMS()
	{
#ifdef _WIN32
		struct __timeb64 timebuffer;
		_ftime64(&timebuffer);
		return timebuffer.time * 1000 + timebuffer.millitm;

#else
		timespec ts;
		if (-1 == clock_gettime(CLOCK_REALTIME, &ts))
		{
			return 0;
		}
		return ((uint64)ts.tv_sec) * 1000 + ts.tv_nsec/1000000;
#endif
	}

	// 获取程序启动到现在所经过的时间
	uint64 GetTimeTickInMS()
	{
		return CTime::Instance()->GetTimeTickInMS();
	}

	// fast time
	void UpdateFastTime(void)
	{
		CTime::Instance()->UpdateFastTime();
	}

	uint64 GetFastTimeTickInMs(void)
	{
		return CTime::Instance()->GetFastTimeTickInMs();
	}

	uint64 GetFastUTCTimeInSec(void)
	{
		return CTime::Instance()->GetFastUTCTimeInSec();
	}

	uint64 GetFastUTCTimeInMS(void)
	{
		return CTime::Instance()->GetFastUTCTimeInMS();
	}
};