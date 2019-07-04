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
This is the script tick.
*/

#pragma once
#include "CNewTick.h"
#include "script/ScriptUtils.h"
#include "script/PyThreadStateLock.h"

namespace common
{
	class ScriptTick : public CNewTick
	{
	public:
		ScriptTick(PyObject* pCallback, PyObject* pArgs, int nCnt = -1) :CNewTick()
		{
			m_nCallCnt = nCnt;
			m_pCallback = pCallback;
			Py_XINCREF(m_pCallback);
			m_pArgs = pArgs;
			Py_XINCREF(m_pArgs);
		}

		virtual ~ScriptTick()
		{
			Py_XDECREF(m_pCallback);
			m_pCallback = NULL;
			Py_XDECREF(m_pArgs);
			m_pArgs = NULL;
		}

		virtual void OnTick()//重载父函数
		{
			if (m_nCallCnt == 0)
			{
				this->UnRegister();
				return;
			}

			if (m_nCallCnt > 0)
			{
				--m_nCallCnt;
			}

			script::CallFunction(m_pCallback, "O", m_pArgs);
			//下面不可以有任何代码，因为脚本回调可能会删除tick。。。
		}

		virtual int GetCallCount()
		{
			return m_nCallCnt;
		}

	protected:
		PyObject* m_pCallback;
		PyObject* m_pArgs;
		int	m_nCallCnt;
	};

	/*
	这个类，支持py多线程环境下，c++ tick对py脚本的调用
	*/
	class CScriptTickMT
		: public ScriptTick
	{
	public:
		CScriptTickMT(PyObject* pCallback, PyObject* pArgs, int nCnt = -1)
			: ScriptTick(pCallback, pArgs, nCnt)
		{}

		virtual	void OnTick()
		{
			script::PyThreadStateLock threadlock;
			ScriptTick::OnTick();
		}

	};
}