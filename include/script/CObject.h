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
This is the wrapper of PyObject but dealwith the refrence correctly.
*/

#pragma once
#include "common/common.h"
#include "python/Python.h"

using namespace common;

namespace script
{
	class CObject
	{
	public:
		CObject();
		CObject(PyObject* pObject);
		CObject(const CObject &rhs);
		CObject& operator=(const CObject& rhs);
		PyObject* operator ()();
		~CObject();

		bool IsValid()
		{
			return m_pObject && m_pObject != Py_None;
		}
		operator int() { return this->to_int(); }
		operator std::string(){ return this->to_string(); }
		operator bool(){ return this->to_bool(); }

		unsigned long long to_ulong(const unsigned long long nDefaultValue = 0);
		long long to_longlong(const long long nDefaultValue = 0);
		int to_int(const int nDefaultValue = -1);
		float to_float(const float nDefaultValue = 0.0);
		unsigned to_uint(const unsigned nDefaultValue = 0);
		bool to_bool(const bool bDefaultValue = false);
		std::string to_string(const std::string& strDefaultValue = "");
		bool to_string_full(std::string& value);//如果是py字符串，把里面所有的字节取出来。忽略中间是否字符串结束符
		const char*  to_c_str(uint32& uLen);
		double to_double(const double dDefaultValue = -1);
		void* to_pointer();

		bool is_string();
		bool is_int();
		bool is_list();
		bool is_tuple();
		
		PyObject* GetPyObj();
		void SetPyObj(PyObject* pObj) { m_pObject = pObj; }
		CObject GetAttr(const char * atts);
		bool HasAttr(const char * atts);

		CObject CallMethod(const char *pszMethod, const char *format = "", ...);

	private:
		void* m_pObject;

	};
}