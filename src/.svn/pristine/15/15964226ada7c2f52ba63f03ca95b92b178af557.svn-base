#include "script/CScripting.h"
#include "script/ScriptUtils.h"
#include "python/frameobject.h"
#include "python/marshal.h"
#include "common/log.h"
#include <stdio.h>

namespace script
{
	void CScripting::InsertPath(int nPos, const char* szPath)
	{
		char szBuffer[ENV_MAX];
		snprintf(szBuffer, ENV_MAX,
			"import sys\n"
			"if '%s' not in sys.path:\n"
			"    sys.path.insert(%d,'%s')\n"
			,
			szPath, nPos, szPath);
		PyRun_SimpleString(szBuffer);
	}

	//return New reference
	PyObject* CScripting::Import(const char* szModule)
	{
		PyObject* pNewModule = PyImport_ImportModule(const_cast<char*>(szModule));
		if (pNewModule == NULL)
		{
			LOG_ERROR("Script| [E] pModule == NULL : file_name = %s", szModule);
		}
		ChkPyErr();
		return pNewModule;
	}

	//szLoadFrom，表示加载者，nLoadType预留使用
	void CScripting::ImportDir(const char* szDir, const char* szPackage, const char* szLoadFrom, int nLoadType)
	{
		PyObject* pModule = Import("loadscript");
		PyObject* pResult = PyObject_CallMethod(pModule, (char*)"load", (char*)"sssi", const_cast<char*>(szDir), const_cast<char*>(szPackage), const_cast<char*>(szLoadFrom), nLoadType);
		Py_XDECREF(pResult);

		bool bGotErr = false;
		if (PyErr_Occurred())
		{
			bGotErr = true;
		}
		ChkPyErr();
		//如果loadscript发生异常，必须崩溃。否则服务器不知道还继续进行。
		if (bGotErr)
		{
			LOG_ERROR("%s", "Error occure when loadscript. please check log file to determine which script has error.");
			__FooCrash();
		}
	};

	const char* CScripting::GetPath()
	{
		const int ENV_MAX = 4096;
		static char szBuffer[ENV_MAX];
		int nSize = 0, i;
		char *p;
		PyObject *pItem;
		CObject sysModule = GetPyModule("sys");
		CObject pathObj = sysModule.GetAttr("path");
		nSize = (int)PyList_Size(pathObj.GetPyObj());

		memset(szBuffer, 0, ENV_MAX);
		p = szBuffer;
		for (i = 0; i < nSize; i++)
		{
			pItem = PyList_GetItem(pathObj.GetPyObj(), i);
			if (!PyString_Check(pItem))
				continue;
#if defined(_DEBUG) && !defined(__linux__)
			printf("%s\n", PyString_AsString(pItem));
#endif
			int strSize = (int)strlen(PyString_AsString(pItem));
#if defined _WINDOWS_
			sprintf( p, "%s;", PyString_AsString( pItem ) );
#elif !defined _WIN32
			sprintf( p, "%s:", PyString_AsString( pItem ) );
#endif

			p += strSize + 1;
		}
		ASSERT(strlen(szBuffer) < ENV_MAX);
		return szBuffer;
	};


	void CScripting::Init(const char* pyHome)
	{
		if (!Py_IsInitialized())
		{
			Py_SetPythonHome((char*)pyHome);

            LOG_INFO("PYTHONHOME is %s", Py_GetPythonHome());

			Py_Initialize();

			InitGameModule();

			InitPath();

			HookIO();

			InitDebugError();

		};
	};

	void CScripting::InitPath()
	{
		script::CScripting::InsertPath(0, ".");
	}

	void CScripting::InitGameModule()
	{
		static PyMethodDef Scripting_Methods[] = {
			// 为调试而设定的函数
			{ "readline", readline, METH_NOARGS, "重定向IO" },
			{ "write", write, METH_VARARGS, "重定向IO" },
			{ "isatty", isatty, METH_NOARGS, "终端类型" },
			{ NULL, NULL }
		};
#ifdef _DEBUG
		int nDebug = 1;
#else
		int nDebug = 0;
#endif

#ifdef __linux__
		int nLinux = 1;
#else
		int nLinux = 0;
#endif

#ifdef _WIN32
		int nWin = 1;
#else
		int nWin = 0;
#endif
		Py_InitModule((char*) "game", Scripting_Methods);
		AddIntConstToModule("isdebug", nDebug);
		AddIntConstToModule("islinux", nLinux);
		AddIntConstToModule("iswin32", nWin);
		AddIntConstToModule("pproto", pproto);
	}

	void CScripting::HookIO()
	{
		PyRun_SimpleString("import sys,game;sys.stdout=game;sys.stderr=game;sys.stdin=game;");
		ChkPyErr();
	};

	//出现脚本错误后是否进入调试模式。
	void CScripting::InitDebugError()
	{
		//int nEnbaleDebugErr = 0;
	}

	void CScripting::EnableDebugger(bool flag)
	{
		PyObject* pModule = GetImportedModule("__builtin__");
		if (NULL == pModule)
			return;

		PyObject* pDict = PyModule_GetDict(pModule);
		if (NULL == pDict)
			return;

		PyObject* enable_debugger = PyBool_FromLong(flag);

		PyDict_SetItemString(pDict, "__enable_debugger__", enable_debugger);
		Py_XDECREF(enable_debugger);
		ChkPyErr();
	}

}
