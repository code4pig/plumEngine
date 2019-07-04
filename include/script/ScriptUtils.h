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
This is utils functions of script related.
*/

#pragma once
#include "common/common.h"
#include "python/Python.h"
#include "script/CObject.h"

#define Py_RETURN_OBJECT(x) return Py_INCREF(x), x
#define PY_RETURN_OK return PyInt_FromLong(1)
#define PY_RETURN_ZERO return PyInt_FromLong(0)
#define PY_RETURN_TRUE return PyBool_FromLong(1)
#define PY_RETURN_FALSE return PyBool_FromLong(0)
#define PY_RETURN_BOOL(x) return (x)?PyBool_FromLong(1):PyBool_FromLong(0)
#define PY_RETURN_ERROR_INT_VALUE return PyInt_FromLong(-1)
#define PY_RETURN_EMPTY_STR return PyString_FromString("")

#define ScriptRegConst( value )	script::AddIntConstToModule( #value,value )

#define GAME_PYTHON_HOME "schome"

#ifndef HIGHEST_PROTOCOL
#define HIGHEST_PROTOCOL 2
#endif

namespace script
{
	const int ENV_MAX = 4096;
	const int DEF_EXP_LEN = 256;
	static int pproto = HIGHEST_PROTOCOL;//���л�����Э��š�����ο��ĵ���cPickle����

	PyObject *GetImportedModule(const char* szModule);

	CObject GetModuleConst(const char* szModule, const char* szConstName, const char* szAtrr);

	CObject GetPyModule(const char* szModule);//���һ��ģ�飮�������������,add by shadow

	CObject GetPyModuleFromFile(const char* szFile);

	// ��directory\filename.py��ʽת����package.module��ʽ
	void FilenameToModulename(const char* szFilename, char* szModulename, uint32 uModLen);

	// ��szModule�ж�����ΪszException���쳣
	void DefineException(const char* szModule, const char* szException);

	script::CObject Run(const char* szFileName, const char* szFunc, const char* format, ...);
	script::CObject Run_valist(const char* szFileName, const char* szFunc, const char* format, va_list va);

	// ���ڵ��ü���һЩ������ֵ
	CObject Invoke(const char* szModuleName, const char* szFunc, const char* format, ...);

	CObject CallFunction(PyObject *callable, char *format, ...);

	// ��"abc.def.xyz"ת��ΪpyModule, �ٵ��� CallObjectMethod(pyObj ...
	// ·��ͳһʹ��"."��񣬿���ʡȥFilenameToModulename��distill����
	CObject CallModuleFunction(const char* szModuleName, const char *szMethod, const char *format = "", ...);

	PyObject* vCall(PyObject* pModule, const char* szFunc, const char* format, va_list va);

	CObject CallObjectMethod(PyObject *pObj, const char *pszMethod, const char *format = "", ...);
	CObject CallObjectMethod_valist(PyObject *pObj, const char *pszMethod, const char *format, va_list va);

	// ��õ�ǰ����ִ�е�ģ��
	char* GetCurExecutedModuleName();
	PyObject* GetCurExecuteModule();
	int32 GetCurExecutedLine();

	// ��python����·���в���·��
	void InsertPath(int nPos, const char *szPath);
	const char* GetPythonPath();
	const char* GetPath();
	void GetPyErrorFileLine(std::string& lastFileName, int&  nLastLine);

	void Init_Import(void);
	PyObject* ReImport(const char* szModuleName);
	void AddIntConstToModule(const char* szName, long nValue, const char * szModule = "game");
	void AddStringConstToModule(PyObject *module, const char *name, const char *value);
	bool DumpPyObject(PyObject* pyobject, std::string& value);
	PyObject* AssemblePyObject(const char* szBuff, int nSize);
	void PrintTrackBack();

	PyObject * GetAttrString(PyObject *, char *);
	PyObject * GetAttrStringNoExcept(PyObject *, const char *);//����Ҳ������׳��쳣


	//��һ���ֽ���������py�ַ���.���ʧ�ܷ���NULL
	CObject PyStringFromData(const char* szBuff, int nSize);

	void ProcessPyError();
	void ChkPyErr();

	//ͨ��python object����string
	std::string GenStrFromPyObject(PyObject* pObject);
	std::string GetTickStrFromPyObject(PyObject* pObject);

	//�ض���
	PyObject* readline(PyObject *self, PyObject *args);
	PyObject* write(PyObject *self, PyObject *args);
	PyObject* isatty(PyObject* self, PyObject *args);

}
