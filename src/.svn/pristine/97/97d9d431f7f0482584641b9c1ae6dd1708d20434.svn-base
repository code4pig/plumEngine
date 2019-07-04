#include "script/CObject.h"
#include "script/ScriptUtils.h"
#include "common/log.h"

namespace script
{
	CObject::CObject()
	{
		m_pObject = NULL;
	}

	CObject::CObject(const CObject& rhs)
	{
		m_pObject = rhs.m_pObject;
		Py_XINCREF((PyObject*)m_pObject);
	}

	CObject::CObject(PyObject* pObject)
	{
		m_pObject = (void*)pObject;
	}

	CObject& CObject::operator = (const CObject& rhs)
	{
		if (m_pObject == rhs.m_pObject)
		{
			return *this;
		}
		Py_XDECREF((PyObject*)m_pObject);
		m_pObject = rhs.m_pObject;
		Py_XINCREF((PyObject*)m_pObject);
		return *this;
	}

	CObject::~CObject()
	{
		Py_XDECREF((PyObject*)m_pObject);
	}

	PyObject* CObject::operator ()()
	{
		if (m_pObject == NULL)
		{
			return Py_None;
		}

		return (PyObject *)m_pObject;
	};

	double CObject::to_double(const double dDefaultValue/* = 0.0 */)
	{
		double res = dDefaultValue;
		if (m_pObject == NULL)
		{
			return res;
		}
		if (PyLong_Check((PyObject*)m_pObject))
		{
			res = PyLong_AsDouble((PyObject*)m_pObject);
		}

		else if (PyInt_Check((PyObject*)m_pObject))
		{
			res = PyInt_AsLong((PyObject*)m_pObject);
		}
		else if (PyFloat_Check((PyObject*)m_pObject))
		{
			res = PyFloat_AsDouble((PyObject*)m_pObject);
		}
		else
		{
			const char* tpname = ((PyObject*)m_pObject)->ob_type->tp_name;
			if (tpname)
			{
				LOG_ERROR("类型检查错误！to_double 但是tpname为 %s", tpname);
			}
			else
			{
				LOG_ERROR("%s", "类型检查错误！");
			}
			PrintTrackBack();
		}
		return res;
	}

	float CObject::to_float(const float nDefaultValue /* = 0.0 */)
	{
		float fRes = nDefaultValue;
		if (m_pObject == NULL)
		{
			return fRes;
		}
		if (PyFloat_Check((PyObject*)m_pObject))
		{
			fRes = (float)PyFloat_AsDouble((PyObject*)m_pObject);
		}
		else if (PyInt_Check((PyObject*)m_pObject))
		{
			fRes = (float)PyInt_AsLong((PyObject*)m_pObject);
		}
		else if (PyLong_Check((PyObject*)m_pObject))
		{
			fRes = (float)PyLong_AsLong((PyObject*)m_pObject);
		}
		else
		{
			const char* tpname = ((PyObject*)m_pObject)->ob_type->tp_name;
			if (tpname)
			{
				LOG_ERROR("类型检查错误！to_float 但是tpname为 %s", tpname);
			}
			else
			{
				LOG_ERROR("%s", "类型检查错误！");
			}
			PrintTrackBack();
		}

		return fRes;
	}

	bool CObject::is_int()
	{

		if (m_pObject != NULL && PyInt_Check((PyObject*)m_pObject))
		{
			return true;
		}
		return false;
	}

	int CObject::to_int(int defaultValue/* = 0*/)
	{
		int res = defaultValue;
		if (m_pObject == NULL)
		{
			return res;
		}

		if (PyInt_Check((PyObject*)m_pObject))
		{
			res = PyInt_AsLong((PyObject*)m_pObject);
		}
		else if (PyLong_Check((PyObject*)m_pObject))
		{
			res = PyLong_AsLong((PyObject*)m_pObject);
		}
		else if (PyFloat_Check((PyObject*)m_pObject))
		{
			res = (int)PyFloat_AsDouble((PyObject*)m_pObject);
		}
		else
		{
			const char* tpname = ((PyObject*)m_pObject)->ob_type->tp_name;
			if (tpname)
			{
				LOG_ERROR("类型检查错误！to_int 但是tpname为 %s", tpname);
			}
			else
			{
				LOG_ERROR("%s", "类型检查错误！");
			}
			PrintTrackBack();
		}
		return res;
	}

	unsigned CObject::to_uint(unsigned defaultValue/* = 0*/)
	{
		unsigned res = defaultValue;
		if (m_pObject == NULL)
		{
			return res;
		}

		if (PyInt_Check((PyObject*)m_pObject))
		{
			res = PyInt_AsLong((PyObject*)m_pObject);
		}
		else if (PyLong_Check((PyObject*)m_pObject))
		{
			res = PyLong_AsUnsignedLong((PyObject*)m_pObject);
		}
		else if (PyFloat_Check((PyObject*)m_pObject))
		{
			res = (unsigned)PyFloat_AsDouble((PyObject*)m_pObject);
		}
		else
		{
			const char* tpname = ((PyObject*)m_pObject)->ob_type->tp_name;
			if (tpname)
			{
				LOG_ERROR("类型检查错误！to_uint 但是tpname为 %s", tpname);
			}
			else
			{
				LOG_ERROR("%s", "类型检查错误！");
			}
			PrintTrackBack();
		}
		return res;
	}


	unsigned long long CObject::to_ulong(const unsigned long long nDefaultValue)
	{
		if (NULL == m_pObject)
			return nDefaultValue;
		unsigned long long res = nDefaultValue;
		if (PyInt_Check((PyObject*)m_pObject))
		{
			res = PyInt_AsLong((PyObject*)m_pObject);
		}
		else if (PyLong_Check((PyObject*)m_pObject))
		{
			res = PyLong_AsUnsignedLongLong((PyObject*)m_pObject);
		}
		else if (PyFloat_Check((PyObject*)m_pObject))
		{
			res = (uint64)(PyFloat_AsDouble((PyObject*)m_pObject));
		}
		else
		{
			const char* tpname = ((PyObject*)m_pObject)->ob_type->tp_name;
			if (tpname)
			{
				LOG_ERROR("类型检查错误！to_ulong 但是tpname为 %s", tpname);
			}
			else
			{
				LOG_ERROR("%s", "类型检查错误！");
			}
		}
		return res;

	}

	long long CObject::to_longlong(const long long nDefaultValue)
	{
		if (NULL == m_pObject)
			return nDefaultValue;
		long long res = nDefaultValue;
		if (PyInt_Check((PyObject*)m_pObject))
		{
			res = PyInt_AsLong((PyObject*)m_pObject);
		}
		else if (PyLong_Check((PyObject*)m_pObject))
		{
			res = PyLong_AsLongLong((PyObject*)m_pObject);
		}
		else if (PyFloat_Check((PyObject*)m_pObject))
		{
			res = (int64)(PyFloat_AsDouble((PyObject*)m_pObject));
		}
		else
		{
			const char* tpname = ((PyObject*)m_pObject)->ob_type->tp_name;
			if (tpname)
			{
				LOG_ERROR("类型检查错误！to_longlong 但是tpname为 %s", tpname);
			}
			else
			{
				LOG_ERROR("%s", "类型检查错误！");
			}
		}
		return res;
	}

	bool CObject::to_bool(bool defaultValue/*= true*/)
	{
		if (NULL == m_pObject)
			return defaultValue;
		if ((PyObject*)m_pObject == Py_True)
			return true;
		if ((PyObject*)m_pObject == Py_False)
			return false;
		//加个int/long的支持
		if (PyInt_Check((PyObject*)m_pObject)){
			return PyInt_AsLong((PyObject*)m_pObject) != 0;
		}
		if (PyLong_Check((PyObject*)m_pObject)){
			return PyLong_AsLong((PyObject*)m_pObject) != 0;
		}
		LOG_WARNING("%s", "Script | Convert Python Bool to C++ bool failed. ");
		return defaultValue;
	}

	bool CObject::is_list()
	{
		if (m_pObject != NULL && PyList_Check((PyObject*)m_pObject))
		{
			return true;
		}
		return false;
	}

	bool CObject::is_tuple()
	{
		if (m_pObject != NULL && PyTuple_Check((PyObject*)m_pObject))
		{
			return true;
		}
		return false;
	}

	bool CObject::is_string()
	{
		if (m_pObject != NULL && PyString_Check((PyObject*)m_pObject))
		{
			return true;
		}
		return false;
	}

	std::string CObject::to_string(const std::string& strDefaultValue/* = "" */)
	{
		if (m_pObject != NULL && PyString_Check((PyObject*)m_pObject))
		{
			char *buf;
			buf = PyString_AsString((PyObject*)m_pObject);
			return std::string(buf);
		}
		LOG_WARNING("%s", "Script | Convert Python String to C++ String call failed. ");
		return strDefaultValue;
	}

	bool CObject::to_string_full(std::string& value)
	{
		if (m_pObject != NULL && PyString_Check((PyObject*)m_pObject))
		{
			int nStrLen = 0;
			char* strVal = NULL;
			PyString_AsStringAndSize(GetPyObj(), &strVal, (Py_ssize_t*)&nStrLen);
			value.clear();
			value.append(strVal, nStrLen);
			return true;
		}
		LOG_WARNING("%s", "Script | Convert Python String All  to C++ String call failed. ");
		return false;
	}

	const char*  CObject::to_c_str(uint32& uLen)
	{
		if (m_pObject != NULL && PyString_Check((PyObject*)m_pObject))
		{
			int nStrLen = 0;
			char* strVal = NULL;
			PyString_AsStringAndSize(GetPyObj(), &strVal, (Py_ssize_t*)&nStrLen);
			uLen = nStrLen;
			return strVal;
		}
		LOG_WARNING("%s", "Script | Convert Python object to c_str call failed. ");
		uLen = 0;
		return NULL;
	}

	//borrow reference
	void* CObject::to_pointer()
	{
		return m_pObject;
	}

	//borrow reference
	PyObject* CObject::GetPyObj()
	{
		return ((PyObject*)m_pObject);
	}


	CObject CObject::CallMethod(const char *pszMethod, const char *format, ...)
	{
		va_list valist;
		va_start(valist, format);
		CObject retObj = CallObjectMethod_valist(GetPyObj(), pszMethod, format, valist);
		va_end(valist);

		return retObj;
	}

	CObject CObject::GetAttr(const char * atts)
	{
		if (!IsValid())
		{
			return NULL;
		}
		PyObject * ret = PyObject_GetAttrString(GetPyObj(), (char*)atts);
		ChkPyErr();
		return ret;
	}


	bool CObject::HasAttr(const char * atts)
	{
		if (!IsValid())
		{
			return false;
		}
		return PyObject_HasAttrString(GetPyObj(), atts) > 0;
	}
}
