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
This is the TTickUserEx which can easily deal with script ticks.
*/

#pragma once
#include "TTickUser.h"
#include "CScriptTick.h"

namespace common
{
	template<class ImpClass, class TTick = ScriptTick>
	class TTickUserEx :public TTickUser<ImpClass>
	{
	public:
		TTickUserEx() :TTickUser<ImpClass>()
		{
		}

		virtual ~TTickUserEx()
		{
		}

	public:

		//ɾ���ű�tick
		void DelScriptTick(PyObject* pCallBack)
		{
			const string sName = script::GetTickStrFromPyObject(pCallBack);
			TTickUser<ImpClass>::RemoveTick(sName.c_str());
		}

		int32 GetScriptTickCallCnt(PyObject* pCallBack)
		{
			string sName = script::GetTickStrFromPyObject(pCallBack);
			TTick* pTick = (TTick*)TTickUser<ImpClass>::FindTick(sName);
			if (pTick == NULL)
			{
				return 0;
			}
			return pTick->GetCallCount();
		}

		//ɾ���ű�tick
		void DelScriptTickByCallBackName(const string& sName)
		{
			TTickUser<ImpClass>::RemoveTick(sName.c_str());
		}


		//ע��ű�tick
		void RegScriptTick(PyObject* pCallBack, PyObject* pArgs, uint32 uInterval, int nCnt = -1, PyObject* pTickName = NULL)
		{
			string sName;
			//nCnt Ϊ 0 ����Чtick
			if (nCnt == 0)
			{
				return;
			}


			if (pTickName == NULL)
			{
				sName = script::GetTickStrFromPyObject(pCallBack);
			}
			else
			{
				sName = script::GetTickStrFromPyObject(pTickName);
			}

			CNewTick* pTick = TTickUser<ImpClass>::FindTick(sName.c_str());
			TTick* pScriptTick = (TTick*)pTick;

			if (pScriptTick)
			{
				//ֻ�����޵��ô����ģ��Ų���ᡣ��Ȼ��ʵ�����滻�á�
				if (pScriptTick->GetInterval() == uInterval && pScriptTick->GetCallCount() == nCnt && nCnt == -1)
				{
					return;//��ȫһ����,�����,ֱ�ӷ���
				}
				else
				{
					TTickUser<ImpClass>::RemoveTick(pScriptTick);//����һ����ʱ�䲻ͬ����ɾ����
				}
			}
			AddNewScriptTick(pCallBack, pArgs, uInterval, sName, nCnt);
		}

	protected:

		void AddNewScriptTick(PyObject* pCallBack, PyObject* pArgs, uint32 uInterval, const string& sName, int nCnt)
		{
			//�����µ�tick����ע��
			TTick * pTick = new TTick(pCallBack, pArgs, nCnt);
			TTickUser<ImpClass>::m_pTickMgr->Register(pTick, uInterval, sName.c_str());
			TTickUser<ImpClass>::m_ticksMap.insert(make_pair(sName, pTick));
		}
	};
}
