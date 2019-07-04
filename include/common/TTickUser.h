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
This is TTickUser which can easily deal with ticks.
*/

#pragma once
#include "CNewTickMgr.h"
#include "CNewTick.h"
#include "TMyTick.h"

namespace common
{
	template<class ImpClass>
	class TTickUser
	{
	public:
		typedef void (ImpClass::*ONTICKFUNC)(void);
		TTickUser() :m_pTickMgr(NULL)
		{
		}

		virtual ~TTickUser()
		{
			//������ʱ������е�tick�ͷŵ�
			FreeSelfTicks();
		}

		void SetTickMgr(CNewTickMgr* pMgr) { m_pTickMgr = pMgr; }

	protected:
		//�����Ѿ�ע��ticks
		std::map<string, CNewTick*> m_ticksMap;//ÿ������(����)��tickֻ����һ����
		CNewTickMgr* m_pTickMgr;

		//ע��һ��tick�������ж��Ƿ��Ѿ���һ�����ֵ�tick,�еĻ���intervalһ������ʾ�Ѵ��ڡ�
		void RegTick(ONTICKFUNC pFunc, uint32 uInterval, const char * szName)
		{
			CNewTick* pTick = this->FindTick(szName);
			if (pTick)
			{
				if (pTick->GetInterval() == uInterval)
				{
					return;//��ȫһ����,�����,ֱ�ӷ���
				}
				else
				{
					RemoveTick(pTick);//����һ����ʱ�䲻ͬ����ɾ����
				}
			}
			AddNewTick(pFunc, uInterval, szName);
		}

		void AddNewTick(ONTICKFUNC pFunc, uint32 uInterval, const char * szName)
		{
			TMyTick<ImpClass> * pTick = new TMyTick<ImpClass>((ImpClass*)this, pFunc);
			m_pTickMgr->Register(pTick, uInterval, szName);
			std::string strName = szName;
			m_ticksMap.insert(make_pair(strName, pTick));
		}

	public:

		void UnRegister(CNewTick* pTick)
		{
			m_pTickMgr->UnRegister(pTick);
		}

		void UnRegister(const char *szName)
		{
			std::map<string, CNewTick*>::iterator it = m_ticksMap.find(szName);
			if (it != m_ticksMap.end())
			{
				m_pTickMgr->UnRegister(it->second);
			}
		}

		void RemoveTick(CNewTick* pTick)
		{
			RemoveTick(pTick->GetTickName());
		}

		void RemoveTick(const char* szName)
		{
			std::map<string, CNewTick*>::iterator it = m_ticksMap.find(szName);
			if (it != m_ticksMap.end())
			{
				SAFE_DELETE(it->second)
					m_ticksMap.erase(it);
			}
		}

		//ɾ��map��������Ч��tick
		void RemoveUnRegisterTick()
		{
			for (std::map<string, CNewTick*>::iterator it = m_ticksMap.begin(); it != m_ticksMap.end();)
			{
				CNewTick* pTick = it->second;
				if (pTick->IsRegistered())
				{
					it++;
				}
				else
				{
					m_ticksMap.erase(it++);
					SAFE_DELETE(pTick);
				}
			}
		}

	protected:

		CNewTick* FindTick(std::string szName)
		{
			std::map<string, CNewTick*>::iterator it = m_ticksMap.find(szName);
			if (it != m_ticksMap.end())
			{
				return it->second;
			}
			else
			{
				return NULL;
			}
		}

		void FreeSelfTicks()
		{
			for (std::map<string, CNewTick*>::iterator it = m_ticksMap.begin(); it != m_ticksMap.end(); ++it)
			{
				CNewTick* pTick = it->second;
				SAFE_DELETE(pTick);
			}
			m_ticksMap.clear();
		}
	};

}