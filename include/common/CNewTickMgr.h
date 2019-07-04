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
This is the tick manager.
*/

#pragma once
#include "CNewTick.h"
#include "list.h"

using namespace std;

// 5,5,5,5,12
#define TVN_BITS 5					// TVN = time vector node
#define TVR_BITS 12					// TVR = time vector root 都是从linux内核抄过来的
#define TVN_SIZE (1 << TVN_BITS)
#define TVR_SIZE (1 << TVR_BITS)
#define TVN_MASK (TVN_SIZE - 1)
#define TVR_MASK (TVR_SIZE - 1)

#define INDEX(N) (uint32)((m_uCurrentTime >> (TVR_BITS + (N) * TVN_BITS)) & TVN_MASK)

namespace common
{
	struct tvec
	{
		struct list_head vec[TVN_SIZE];
	};

	struct tvec_root
	{
		struct list_head vec[TVR_SIZE];
	};

	class CNewTickMgr
		:public CNewTick
	{
		friend class CNewTick;

	private:
		uint64 m_uCurrentTime;			//当前的时间
		uint32 m_uTickInterval;

		struct tvec_root tv1;
		struct tvec tv2;
		struct tvec tv3;
		struct tvec tv4;
		struct tvec tv5;

	public:

		CNewTickMgr( uint32 uTickCyc = 33 );	//uTickCyc Tick的周期=多少毫秒Tick一次
		virtual ~CNewTickMgr();

		uint32 GetInterval()const				{ return m_uTickInterval; }
		void OnTick();

		bool Register( CNewTick* pTick, uint32 uInterval, const char * szName );	//uInterval Tick的周期=多少毫秒Tick一次
		void UnRegister( CNewTick* pTick );

	private:
		void ClearTickList( struct list_head* phead );		// 清除list中的所有tick
		void InternalRegister( stTickEntry * pTickEntry );	// 将tick根据时间注册到不同的time vector中
		void TickStep();									// 时间到了，call tick
		uint32 Cascade(struct tvec *tv, int index);			// copy linux内核的，开始遍历所有time vector，搬移tick
	};
}

