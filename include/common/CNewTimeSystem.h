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
This is the timesystem which deal with time and tick functions.
*/

#pragma once
#include "CNewTickMgr.h"
#include "CTime.h"

namespace common
{
	class CNewTick;
	class CNewTickMgr;
	class CAdvanceTick;

	class CNewTimeSystem
	{
	public:
		CNewTimeSystem(uint32 uBaseCyc);
		~CNewTimeSystem();

		//--------------------------------------------------
		static void Init(uint32 uBaseCyc);
		static void Unit();
		static CNewTimeSystem*& Inst();
		//--------------------------------------------------

		void Register(CNewTick* pTick, uint32 uCyc, const char* szName);
		void Register(CAdvanceTick* pAdvanceTick,uint32 uBeginTime,uint32 uCyc,const char* szName);
		void UnRegister(CNewTick* pTick);

		CNewTickMgr* GetTickMgr() { return m_pTickMgr; }

		uint32 GetBaseCyc()const { return m_pTickMgr->GetInterval();}
		uint64 GetFrameTime()const { return m_uLogicTime;}
		uint64 GetBaseTime()const { return m_uLogicBaseTime;}

		void Reset() { Reset(GetTimeTickInMS()); }
		void Reset(uint64 uProcessTime) { m_uLogicBaseTime=m_uLogicTime=uProcessTime;}

		//推动逻辑时间前进
		int32 PushLogicTime() { return PushLogicTime(GetTimeTickInMS()); }
		int32 PushLogicTime(uint64 uRealTime);

		// 停止tick系统的推动
		void Stop(void) { m_bStop = true;}

	private:
		CNewTickMgr* m_pTickMgr;
		uint64 m_uLogicBaseTime;
		uint64 m_uLogicTime;
		uint64 m_uPushCount;//已推动的次数,可以保证地球还在的时候都不会溢出
		bool m_bStop;
	};
}
