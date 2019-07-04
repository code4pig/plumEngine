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
This is the tick which can be used for timer tick for freedom.
*/

#pragma once
#include "common.h"
#include "TickEntry.h"

namespace common
{
	class CNewTickMgr;

	class CNewTick
	{
		friend class CNewTickMgr;
	public:
		CNewTick();
		virtual ~CNewTick(void);

		uint32 GetInterval()const { return m_uInterval; }	// 获得这个tick每隔多长时间运行一次
		CNewTickMgr* GetTickMgr()const { return m_pTickMgr; }
		virtual void OnTick(){}

		bool IsRegistered() const;
		const char* GetTickName() const;

	protected:
		void UnRegister();
		void SetTickName(const char* szName) { *m_pstrTickName = szName; }

	private:
		uint32 m_uInterval;		//多少时间处理一次,毫秒做单位
		CNewTickMgr* m_pTickMgr;//挂在哪个mgr上，构造的时候为空
		stTickEntry* m_pTickEntry;
		std::string* m_pstrTickName;
	};
}


