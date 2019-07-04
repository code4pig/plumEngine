#include "script/ScriptUtils.h"
#include "common/log.h"
#include "script/CScripting.h"
#include "script/PyThreadStateLock.h"
#include "python/frameobject.h"
#include <iostream>
#include <stdio.h>

namespace script
{
	//////////////////////////////////////////////////////////////////////////
	// 重定向Python的IO
	PyObject* readline(PyObject *self, PyObject *args)
	{
		std::vector<char> line;
		while (!std::cin.eof())
		{
			char letter;
			std::cin.get(letter);
			if (letter == '\n')
			{
				line.push_back('\0');
				break;

			}
			line.push_back(letter);

		}
		const char* sInputLine = "";
		if (line.size() > 0)
		{
			sInputLine = &line[0];
		}
		return PyString_FromString(sInputLine);
	};

	void _scriptwrite(const char* szMsg)
	{
		bool bNeedWriteLogStart = false;
		static bool g_script_linestarted = false;

		if (!g_script_linestarted)
		{
			bNeedWriteLogStart = true;
			g_script_linestarted = true;

		}
		if (szMsg[0] == '\n')
		{
			g_script_linestarted = false;
		}

		//当前模块。
		char* szCurModuleName = GetCurExecutedModuleName();
		std::string strCurModuleName = "";
		if (szCurModuleName)
		{
			strCurModuleName = szCurModuleName;
			uint32 uSize = (uint32)strCurModuleName.size();
			uint32 uIdx = (uint32)strCurModuleName.find_last_of('.');
			if (uIdx != std::string::npos && uSize > uIdx)
				strCurModuleName = strCurModuleName.substr(uIdx + 1, uSize - uIdx - 1);
		}

		Py_BEGIN_ALLOW_THREADS
			//这个宏允许python多线程执行，因为写一般是个阻塞式的IO操作
			if (bNeedWriteLogStart)
			{
				LOG_SCRIPT_CACHE("[%s] %s", strCurModuleName.c_str(), szMsg);
			}
			else
			{
				if (szMsg[0] != '\n')
				{
					LOG_SCRIPT_CACHE("%s", szMsg);
				}
				else
				{
					LOG_SCRIPT_FLUSH();
				}
			}
		Py_END_ALLOW_THREADS
	}

	PyObject* write(PyObject *self, PyObject *args)
	{
		char * szMsg = NULL;
		int uLen = 0;

		if (!PyArg_ParseTuple(args, "s#", &szMsg, &uLen))//当py string中含有0字节的内容时候，会报错，所以这个采用s#
			return NULL;

		if (uLen <= 0)
		{
			Py_RETURN_NONE;
		}

		if (szMsg[uLen] != '\0'){//强制加0. 这种情况极少数发生，但py是有可能的。
			std::string s;
			s.assign(szMsg, uLen);
			s.push_back('\0');

			_scriptwrite(s.data());
		}
		else
		{
			_scriptwrite(szMsg);
		}

		PY_RETURN_OK;
	}

	PyObject* isatty(PyObject* self, PyObject *args)
	{
#ifdef _DEBUG
		return PyInt_FromLong(1);
#else
		return PyInt_FromLong(0);
#endif
	}

	PyObject* debugmode(PyObject* self, PyObject* args)
	{
#ifdef _DEBUG
		return PyInt_FromLong(1);
#else
		return PyInt_FromLong(0);
#endif
	};

	// 获取已经导入的模块对象
	PyObject *GetImportedModule(const char* szModule)
	{
		PyObject * pDict = PyImport_GetModuleDict();
		PyObject* retval = PyDict_GetItemString(pDict, const_cast<char*>(szModule));
		return retval;
	};

	//获取python模块中myconst结构的属性,szConstName为myconst结构名，szAtrr为具体哪个常量名
	CObject GetModuleConst(const char* szModule, const char* szConstName, const char* szAtrr)
	{
		return GetPyModule(szModule).GetAttr(szConstName).GetAttr(szAtrr);
	}

	//获取一个模块对象。如果不存在，尝试import
	CObject GetPyModule(const char* szModule)
	{//获得一个模块．如果不存在则导入
		PyObject* pModule = NULL;
		pModule = GetImportedModule(szModule);
		if (pModule != NULL)
		{
			Py_XINCREF(pModule);
		}
		else
		{
			pModule = CScripting::Import(szModule);
		}
		return pModule;
	}

	CObject GetPyModuleFromFile(const char* szFile)
	{
		char szModule[FILENAME_MAX];
		FilenameToModulename(szFile, szModule, FILENAME_MAX);

		return GetPyModule(szModule);
	}

	// 将"路径/文件名"格式转换为"包.模块"格式
	void FilenameToModulename(const char* szFilename, char* szModulename, uint32 uModLen)
	{
		if (strlen(szFilename) < 2)
		{
			szModulename[0] = '\0';
			return;
		};

		if (szFilename[0] == '.' && (szFilename[1] == '\\' || szFilename[1] == '/'))
		{
			strncpy(szModulename, szFilename + 2, uModLen);
		}
		else
		{
			strncpy(szModulename, szFilename, uModLen);
		}

		int32 uSize = (int32)strlen(szModulename);
		char *p = NULL;
		for (int32 i = uSize - 1; i >= 0; i--)
		{
			if (szModulename[i] == ' ')
			{
				szModulename[i] = '\0';
				continue;
			}
			if (szModulename[i] == 'y' && i - 1 >= 0 && szModulename[i - 1] == 'p' && i - 2 >= 0 && szModulename[i - 2] == '.')
			{
				p = szModulename + i - 2;
			}
			break;
		}
		if (p != NULL)
		{
			*p = '\0';
		}

		// 将路径方式转换成package访问方式
		p = szModulename;
		while (p != NULL && *p != '\0')
		{
			if (*p == '\\' || *p == '/')
			{
				*p = '.';
			}
			p++;
		}
	};

	// 定义新的异常类
	void DefineException(const char* szModule, const char* szException)
	{
		PyObject* module = Py_InitModule(const_cast<char*>(szModule), NULL);
		char szBuff[DEF_EXP_LEN];
		snprintf(szBuff, DEF_EXP_LEN, "%s.%s", szModule, szException);
		PyModule_AddObject(module, const_cast<char*>(szException), PyErr_NewException(szBuff, NULL, NULL));
	};

	char* GetCurExecutedModuleName()
	{
		struct _frame *pFrame = PyEval_GetFrame();
		if (pFrame)
		{
			PyObject* pName = PyDict_GetItemString(pFrame->f_globals, "__name__");
			return PyString_AsString(pName);
		}
		//这是静态的字符串。
		return (char*)"";
	}

	PyObject* GetCurExecuteModule()
	{
		return GetImportedModule(GetCurExecutedModuleName());
	}

	int32 GetCurExecutedLine()
	{
		struct _frame *pFrame = PyEval_GetFrame();
		if (pFrame)
		{
			return pFrame->f_lineno;
		}
		return 0;
	}


	// 调用脚本
	PyObject* vCallProf(PyObject* callable, const char* format, va_list va)
	{
		// 以下代码部分复制于PyObject_CallFunction
		PyObject * args, *retval;
		retval = NULL;
		static int count = 0;
		ChkPyErr();
		try
		{
			if (!callable)
			{
				return retval;
			}

			if (callable == Py_None)
			{
				LOG_ERROR("%s", "call func is None");
				ChkPyErr();
			}

			if (format && *format)
			{
				args = Py_VaBuildValue((char*)format, va);
				if (!args)
				{
					LOG_ERROR("%s", "vCallProf Py_VaBuildValue failed.");
					ChkPyErr();
					return NULL;
				}

				if (!PyTuple_Check(args))
				{
					PyObject * aTmpTuple;
					aTmpTuple = PyTuple_New(1);

					if (aTmpTuple == NULL)
					{
						LOG_ERROR("%s", "vCallProf aTmpTuple == NULL.");
						return NULL;
					}
					if (PyTuple_SetItem(aTmpTuple, 0, args) < 0)
					{
						LOG_ERROR("%s", "vCallProf PyTuple_SetItem failed.");
						return NULL;
					}
					args = aTmpTuple;
				}
			}
			else
			{
				args = PyTuple_New(0);
			}

			if (!args)
			{
				LOG_ERROR("%s", "vCallProf args is NULL.");
				return NULL;
			}

			PyObject* pProfile = NULL;
			PyObject* runall = NULL;

			try
			{
				if (runall && count == 0)
				{
					count = count + 1;
					PyObject *pList = PyList_New(PyTuple_Size(args) + 1);
					PyList_SetItem(pList, 0, callable);

					for (int i = 0; i < PyTuple_Size(args); i++)
					{
						PyObject* pItem = PyTuple_GetItem(args, i);
						Py_INCREF(pItem);
						PyList_SetItem(pList, i + 1, pItem);
					}
					Py_DECREF(args);
					Py_INCREF(callable);

					args = PyList_AsTuple(pList);
					retval = PyObject_Call(runall, args, NULL);
					count = count - 1;
					Py_DECREF(pList);
				}
				else
				{
					retval = PyObject_Call(callable, args, NULL);
				}
				ChkPyErr();
			}
			catch (...)
			{
				Py_XDECREF(runall);
				Py_XDECREF(pProfile);
				Py_DECREF(args);
				throw;
			}
			Py_XDECREF(runall);
			Py_XDECREF(pProfile);
			Py_DECREF(args);
		}
		catch (std::exception& exp)
		{
			PyObject* pCallableStr = PyObject_Str(callable);
			char* szCallableName = PyString_AsString(pCallableStr);
			char* szCurExcModuleName = GetCurExecutedModuleName();
			int32 nLineNum = GetCurExecutedLine();
			LOG_ERROR("vCallProf got std::exception:%s szCallableName:%s szCurExcModuleName:%s nCurExcLineNum:%d", exp.what(), szCallableName, szCurExcModuleName, nLineNum);
		}
		catch (...)
		{
			LOG_ERROR("%s", "vCallProf got c exception.");
			PyObject* pCallableStr = PyObject_Str(callable);
			char* szCallableName = PyString_AsString(pCallableStr);
			char* szCurExcModuleName = GetCurExecutedModuleName();
			int32 nLineNum = GetCurExecutedLine();
			LOG_INFO("Script| [E] vCallProf got c exception szCallableName:%s szCurExcModuleName:%s nCurExcLineNum:%d", szCallableName, szCurExcModuleName, nLineNum);
			Py_XDECREF(pCallableStr);
		}

		return retval;
	}


	// PyObject_CallFunction的代替品
	// 将输出调用过程的异常信息并清理异常标志
	CObject CallFunction(PyObject *callable, char *format, ...)
	{
		va_list mylist;
		va_start(mylist, format);
		PyThreadStateLock pylock;
		PyObject* ret = vCallProf(callable, format, mylist);
		va_end(mylist);
		return ret;
	}


	PyObject* vCall(PyObject* pModule, const char* szFunc, const char* format, va_list va)
	{
		PyObject* retval = NULL;
		PyObject* callable = NULL;

		if (pModule == NULL)
		{
			LOG_INFO("Script| [E] pModule == NULL Func = %s", szFunc == NULL ? "Null" : szFunc);
			goto failout;
		}
		if (pModule == Py_None)
		{
			LOG_INFO("Script| [E] pModule == None Func = %s", szFunc == NULL ? "Null" : szFunc);
			goto failout;
		}

		callable = GetAttrString((PyObject*)pModule, (char*)szFunc);

		if (!callable || (callable == Py_None))
		{
			std::string strModuleName;
			PyObject* pModuleName = GetAttrStringNoExcept(pModule, "__name__");
			if (pModuleName)
			{
				strModuleName = PyString_AsString(pModuleName);
			}
			else
			{
				PyObject* pType = PyObject_Type(pModule);
				if (pType)
				{
					PyObject* pyTypeName = PyObject_Str(pType);
					strModuleName = PyString_AsString(pyTypeName);
					Py_XDECREF(pType);
					Py_XDECREF(pyTypeName);
				}
				else
				{
					ChkPyErr();
				}
			}
			LOG_INFO("Script| [E] callable is NULL or None : mod_name = %s , func_name = %s", strModuleName.c_str(), szFunc);

			Py_XDECREF(pModuleName);
			goto failout;
		}

		retval = vCallProf(callable, format, va);

	failout:
		ChkPyErr();
		Py_XDECREF(callable);
		return retval;
	};

	PyObject* vCall(const char* szModuleName, const char* szFunc, const char* format, va_list va)
	{
		PyObject* retval = NULL;
		CObject module = GetPyModule(const_cast<char*>(szModuleName));
		if (!module.IsValid())
		{
			LOG_ERROR("Script| [E] pModule == NULL : mod_name = %s  func = %s", szModuleName, szFunc);
			return retval;
		}
		retval = vCall(module.GetPyObj(), szFunc, format, va);
		return retval;
	};

	CObject CallModuleFunction(const char* szModuleName, const char *pszMethod, const char *format, ...)
	{
		CObject cModule = GetPyModule(szModuleName);
		if (!cModule.IsValid())
		{
			LOG_ERROR("Script| [E] pModule == NULL : mod_name = %s  func = %s", szModuleName, pszMethod);
			return NULL;
		}

		va_list valist;
		va_start(valist, format);
		CObject retObj = CallObjectMethod_valist(cModule.GetPyObj(), pszMethod, format, valist);
		va_end(valist);

		return retObj;
	}

	CObject CallObjectMethod(PyObject *pObj, const char *pszMethod, const char *format, ...)
	{
		va_list valist;
		va_start(valist, format);
		CObject retObj = CallObjectMethod_valist(pObj, pszMethod, format, valist);
		va_end(valist);

		return retObj;
	}

	CObject  CallObjectMethod_valist(PyObject *pObj, const char *pszMethod, const char *format, va_list valist)
	{
		PyObject *ret = vCall(pObj, pszMethod, format, valist);
		return ret;
	}

	CObject Invoke(const char* szFileName, const char* szFunc, const char* format, ...)
	{
		script::CObject retval;

		if (format && *format)
		{
			va_list va;
			va_start(va, format);
			retval = Run_valist(szFileName, szFunc, format, va);
			va_end(va);
		}
		else
		{
			retval = Run_valist(szFileName, szFunc, format, NULL);
		};
		return retval;
	};

	PyObject* ReImport(const char* szModuleName)
	{
		char szModule[FILENAME_MAX];
		FilenameToModulename(szModuleName, szModule, FILENAME_MAX);
		PyObject* pModule = GetImportedModule(szModule);
		if (pModule == NULL)
		{
			pModule = CScripting::Import(szModule);
		}
		else
		{
			pModule = PyImport_ReloadModule(pModule);
			if (pModule == NULL)
			{
				LOG_ERROR("Script | Reload script %s failed. ", szModuleName);
			}
		};
		ChkPyErr();
		return pModule;
	}

	void AddIntConstToModule(const char* szName, long nValue, const char *szModule)
	{
		PyObject* pModule = GetImportedModule(szModule);
		if (pModule != NULL)
		{
			if (PyModule_AddIntConstant(pModule, szName, nValue) != 0)
			{
				ChkPyErr();
			}
		}
	};

	void AddStringConstToModule(PyObject *pModule, const char *name, const char *value)
	{
		if (PyModule_AddStringConstant(pModule, name, value) != 0)
		{
			ChkPyErr();
		}
	};


	void distill(const std::string strSrcModule, const std::string strSrcObj, std::string& strDstModule, std::string& strDstObj)
	{
		strDstModule = strSrcModule;
		strDstObj = strSrcObj;

		if (strSrcObj != "")
		{
			/*  例如：在npc.py中
			* import script.general as general;
			* .....
			* Player.Talk("general.func1",....)
			* 这种情况下，就要把general.func1转换为script.general.func1
			* strDstModule = script.general, strDstObj = func1
			*/
			CObject module = GetPyModule(strSrcModule.c_str());

			if (!module.IsValid())
				return;

			std::string::size_type pos = 0;
			pos = strSrcObj.find_last_of(".");
			if (pos != std::string::npos)
			{
				strDstModule = strSrcObj.substr(0, pos);

				CObject attr, attr1;

				attr = module.GetAttr(strDstModule.c_str());

				if (!attr.IsValid())
					return;
				attr1 = attr.GetAttr("__name__");

				strDstModule = attr1.to_string();
				strDstObj = strSrcObj.substr(pos + 1);

			};
		}
		else
		{
			/* 例如，gcc远程调用gas上flag.py的DoBegin函数,调用形式为flag.DoBegin(...)
			* 转换为 strDstModule = flag, strDstObj = DoBegin
			*/
			std::string::size_type pos = 0;
			pos = strSrcModule.find_last_of(".");
			if (pos != std::string::npos)
			{
				strDstModule = strSrcModule.substr(0, pos);
				strDstObj = strSrcModule.substr(pos + 1);
			};
		}
	};

	script::CObject Run_valist(const char* szFileName, const char* szFunc, const char* format, va_list va)
	{
		const char* szOut = szFileName;
		std::string strScript = "";
		std::string strFunc = "";
		PyObject *retval = NULL;
		if (NULL == szFileName || NULL == szFunc || NULL == format)
		{
			goto failout;
		}

		char szModule[FILENAME_MAX];
		FilenameToModulename(szOut, szModule, FILENAME_MAX);

		if (szModule[0] == '\0')
		{
			goto failout;
		};

		distill(szModule, szFunc, strScript, strFunc);

		if (format && *format)
		{
			retval = script::vCall(strScript.c_str(), strFunc.c_str(), format, va);
		}
		else
		{
			retval = script::vCall(strScript.c_str(), strFunc.c_str(), format, NULL);
		};

	failout:
		return retval;
	}

	//c++调python
	script::CObject Run(const char* szFileName, const char* szFunc, const char* format, ...)
	{
		script::CObject retval;

		if (format && *format)
		{
			va_list va;
			va_start(va, format);
			retval = Run_valist(szFileName, szFunc, format, va);
			va_end(va);
		}
		else
		{
			retval = Run_valist(szFileName, szFunc, format, NULL);
		}

		return retval;
	};

	bool DumpPyObject(PyObject* pyobject, std::string& value)
	{
		if (pyobject == NULL)
			return false;

		CObject cpickle = GetPyModule("cPickle");
		if (!cpickle.IsValid())
			return false;
		CObject result = cpickle.CallMethod("dumps", "Oi", pyobject, pproto);
		return result.to_string_full(value);
	}

	//New reference
	PyObject* AssemblePyObject(const char* szBuff, int nSize)
	{
		ChkPyErr();
		if (nSize <= 0)
		{
			return PyString_FromString("");
		}

		CObject cpickle = GetPyModule("cPickle");
		if (!cpickle.IsValid())
			return NULL;

		PyObject* pyobject = PyString_FromStringAndSize(szBuff, nSize);
		PyObject* retval = PyObject_CallMethod(cpickle.GetPyObj(), (char*)"loads", (char*)"O", pyobject);
		Py_XDECREF((PyObject*)pyobject);

		ChkPyErr();
		return retval;
	};

	//New refrence
	CObject PyStringFromData(const char* szBuff, int nSize)
	{
		if (nSize <= 0)
		{
			return NULL;
		}
		ChkPyErr();
		PyObject* pyobject = PyString_FromStringAndSize(szBuff, nSize);
		ChkPyErr();
		return pyobject;

	}

	void PrintTrackBack()
	{
		typedef std::vector< _frame* > CallStack;
		CallStack callStack;
		struct _frame *frame = PyEval_GetFrame();
		while (frame)
		{
			callStack.push_back(frame);
			frame = frame->f_back;
		};
		CallStack::reverse_iterator where;

		for (where = callStack.rbegin(); where != callStack.rend(); where++)
		{
			frame = *where;
			LOG_INFO("Script| frame %s in %s at line %d.",
				PyString_AsString(frame->f_code->co_name),
				PyString_AsString(frame->f_code->co_filename),
				frame->f_code->co_firstlineno);
		};
	}

	void GetPyErrorFileLine(std::string& lastFileName, int& nLastLine)
	{
		PyObject *type_obj = NULL;
		PyObject *value_obj = NULL;
		PyObject *traceback_obj = NULL;
		PyErr_Fetch(&type_obj, &value_obj, &traceback_obj);
		if (traceback_obj != NULL)
		{
			PyTracebackObject *traceback = (PyTracebackObject *)traceback_obj;
			while (traceback)
			{
				if (NULL == traceback->tb_next)
				{
					PyCodeObject* codeobj = traceback->tb_frame->f_code;
					lastFileName = PyString_AsString(codeobj->co_filename);
					nLastLine = traceback->tb_lineno;
					break;
				}
				traceback = traceback->tb_next;
			}

		}
		if (type_obj || value_obj || traceback_obj)
		{
			PyErr_Restore(type_obj, value_obj, traceback_obj); // 因为 PyErr_Fetch 会清除错误记录，需要设置回去
		}
	}

	//此函数只有在调用了script::CScripting::Init函数之后才能被调用
	void ProcessPyError()
	{
		PyErr_Print();
	}

	PyObject * GetAttrString(PyObject * obj, char * atts)
	{
		PyObject * ret = PyObject_GetAttrString(obj, atts);
		ChkPyErr();
		return ret;
	}

	PyObject * GetAttrStringNoExcept(PyObject * obj, const char * atts)
	{
		PyObject * ret = PyObject_GetAttrString(obj, atts);
		if (PyErr_Occurred())
		{
			PyErr_Clear();
			return NULL;
		}
		return ret;
	}

	std::string GetTickStrFromPyObject(PyObject* pObject)
	{
		std::string sRes = "";
		std::ostringstream strm;

		//如果是方法，则要特殊处理，防止有人重载了 __repr__ 导致没办法唯一
		if (PyMethod_Check(pObject))
		{
			const char *sfuncname = "?", *sclasssname = "?";
			PyObject* pSelf = PyMethod_Self(pObject); //borrow ref 不用释放
			PyObject* pClass = PyMethod_Class(pObject); //borrow ref 不用释放
			PyObject* pFunc = PyMethod_Function(pObject); //borrow ref 不用释放

			PyObject* funcname = PyObject_GetAttrString(pFunc, "__name__");// new ref 需要释放
			PyObject* classname = PyObject_GetAttrString(pClass, "__name__");// new ref 需要释放

			//检查 func
			if ((funcname != NULL) && PyString_Check(funcname))
			{
				sfuncname = PyString_AsString(funcname);
			}
			Py_XDECREF(funcname);

			//检查 class
			if ((classname != NULL) && PyString_Check(classname))
			{
				sclasssname = PyString_AsString(classname);
			}
			Py_XDECREF(classname);

			sRes += sfuncname;
			sRes += sclasssname;
			if (pSelf != NULL)
			{
				strm << pSelf;
			}
			sRes += strm.str();
			return sRes;
		}

		return GenStrFromPyObject(pObject);
	}


	std::string GenStrFromPyObject(PyObject* pObject)
	{
		std::string sRes = "";

		PyObject* pStr = PyObject_Str(pObject);
		if (pStr == NULL)
		{
			ChkPyErr();
			return sRes;
		}

		char* szName = PyString_AsString(pStr);
		if (szName == NULL)
		{
			ChkPyErr();
			Py_XDECREF(pStr);
			return sRes;
		}
		sRes = szName;
		Py_XDECREF(pStr);
		return sRes;
	}

	void ChkPyErr()
	{
		if (!PyErr_Occurred())
		{
			return;
		}
		ProcessPyError();
	}

};
