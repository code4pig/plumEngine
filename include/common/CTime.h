/*
Copyright (C) 2017, Zhang Baofeng.

BSD 2-Clause License (http://www.opensource.org/licenses/bsd-license.php)

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

* Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above
copyright notice, this list of conditions and the following disclaimer
in the documentation and/or other materials provided with the
distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

You can contact the author via email : zhangbaofeng@joygame.cc
This is the real time functions.
*/

#pragma once
#include "common.h"
#ifdef _WIN32
#include <sys/timeb.h>
#endif

namespace common{

#ifdef __cplusplus
	extern "C"{
#endif
		// 返回：从UTC时间1970年1月1日午夜(00:00:00)起累计的时间
		PLUMAPI uint64 GetUTCTimeInSec(void);
		PLUMAPI uint64 GetUTCTimeInMS(void);

		// 获取程序启动到现在所经过的时间
		PLUMAPI uint64 GetTimeTickInMS(void);

		// fast time
		PLUMAPI void UpdateFastTime(void);
		PLUMAPI uint64 GetFastTimeTickInMs(void);
		PLUMAPI uint64 GetFastUTCTimeInSec(void);
		PLUMAPI uint64 GetFastUTCTimeInMS(void);
#ifdef __cplusplus
	}
#endif

	class CTime
	{
	private:
		CTime();
		~CTime() {}

		static uint64 ms_uBaseTime;
#ifdef _WIN32
		static LARGE_INTEGER ms_uFrequency;
#endif

		uint64 m_uFastTimeTickInMS;
		uint64 m_uFastUTCTimeInMS;
		uint64 m_uFastUTCTimeInSec;

	public:
		static CTime* Instance(void);
		static void Release();

		// 获取程序启动到现在所经过的时间
		uint64 GetTimeTickInMS(void);

		// fast time
		void UpdateFastTime(void);

		uint64 GetFastTimeTickInMs(void) { return m_uFastTimeTickInMS; }
		uint64 GetFastUTCTimeInSec(void) { return m_uFastUTCTimeInSec; }
		uint64 GetFastUTCTimeInMS(void) { return m_uFastUTCTimeInMS; }
	};

};
