#include "application/pygame.h"
#include "script/ScriptUtils.h"
#include "application/CApplication.h"
#include "application/CAsioService.h"
#include "common/CTime.h"
#include "common/log.h"

namespace application
{
	//开启网络服务
	PyObject* StartNetwork(PyObject* self, PyObject* args);
	//连接服务器
	PyObject* ConnectToServer(PyObject* self, PyObject* args);
	//发送消息到服务器
	PyObject* SendMsgToServer(PyObject* self, PyObject* args);
	//发送消息到客户端
	PyObject* SendMsgToClient(PyObject* self, PyObject* args);
	//获取快速时间戳，单位秒
	PyObject* GetFastTimeInSec(PyObject* self, PyObject* args);
	//获取快速时间戳，单位毫秒
	PyObject* GetFastTimeInMs(PyObject* self, PyObject* args);
	//设置帧率
	PyObject* InitFrameRate(PyObject* self, PyObject* args);
	//写日志
	PyObject* Log(PyObject* self, PyObject* args);
	//输出内存统计
	PyObject* GenMemStat(PyObject* self, PyObject* args);
	//注册tick
	PyObject* RegTick(PyObject* self, PyObject* args);
	//删除tick
	PyObject* DelTick(PyObject* self, PyObject* args);
	//主动崩溃掉进程
	PyObject* GenCrash(PyObject* self, PyObject* args);
	//开启应用层的心跳包
	PyObject* OpenHeartBeat(PyObject* self, PyObject* args);
	//设置输出日志级别
	PyObject* SetLogLevel(PyObject* self, PyObject* args);

	static PyMethodDef Scripting_Methods[] =
	{
		{ "StartNetwork", (PyCFunction)StartNetwork, METH_VARARGS, "开启网络服务" },
		{ "ConnectToServer", (PyCFunction)ConnectToServer, METH_VARARGS, "连接服务器" },
		{ "SendMsgToServer", (PyCFunction)SendMsgToServer, METH_VARARGS, "发送消息给指定的服务器连接" },
		{ "SendMsgToClient", (PyCFunction)SendMsgToClient, METH_VARARGS, "发送消息给指定的客户端连接" },
		{ "GetFastTimeInSec", (PyCFunction)GetFastTimeInSec, METH_NOARGS, "获取快速时间戳，单位秒" },
		{ "GetFastTimeInMs", (PyCFunction)GetFastTimeInMs, METH_NOARGS, "获取快速时间戳，单位毫秒" },
		{ "InitFrameRate", (PyCFunction)InitFrameRate, METH_VARARGS, "初始化帧率" },
		{ "Log", (PyCFunction)Log, METH_VARARGS, "写日志" },
		{ "GenMemStat", (PyCFunction)GenMemStat, METH_NOARGS, "打印内存统计信息" },
		{ "RegTick", (PyCFunction)RegTick, METH_VARARGS, "注册tick" },
		{ "DelTick", (PyCFunction)DelTick, METH_VARARGS, "删除tick" },
		{ "GenCrash", (PyCFunction)GenCrash, METH_VARARGS, "脚本层主动触发崩溃" },
		{ "OpenHeartBeat", (PyCFunction)OpenHeartBeat, METH_VARARGS, "开启应用层的心跳包" },
		{ "SetLogLevel", (PyCFunction)SetLogLevel, METH_VARARGS, "设置输出日志级别" },
		{ NULL, NULL }
	};

	//脚本控制开启网络
	PyObject* StartNetwork(PyObject *self, PyObject *args)
	{
		int32 nettype = 0;
		char* szIP = 0;
		int32 port = 0;
		uint16 limit_msg_num = 0;
		uint8 limit_invalid_num = 0;
		bool encrypt = false;
		int32 maxclients = 5000;
		if (!PyArg_ParseTuple(args, "isiHB|Bi", &nettype, &szIP, &port, &limit_msg_num, &limit_invalid_num, &encrypt, &maxclients))
			return NULL;

		CApplication::GetInstance()->StartNetwork(nettype, szIP, port, limit_msg_num, limit_invalid_num, encrypt, maxclients);

		PY_RETURN_TRUE;
	}

	//脚本控制连接服务器
	PyObject* ConnectToServer(PyObject *self, PyObject *args)
	{
		int32 nettype = 0;
		char* szAddr = 0;
		int32 port = 0;
		bool encrypt = false;
		int32 retrytimes = 0;
		int32 retrysec = 5;
		if (!PyArg_ParseTuple(args, "isi|iiB", &nettype, &szAddr, &port, &retrytimes, &retrysec, &encrypt))
			return NULL;

		CApplication::GetInstance()->ConnectToServer(nettype, szAddr, port, encrypt, retrytimes, retrysec);

		PY_RETURN_TRUE;
	}

	//脚本控制连接服务器
	PyObject* SendMsgToClient(PyObject *self, PyObject *args)
	{
		int32 nettype = 0;
		uint32 pid = 0;
		uint8 proto_type = 0;
		char* msg = 0;
		uint32 uSize = 0;
		if (!PyArg_ParseTuple(args, "iIBs#", &nettype, &pid, &proto_type, &msg, &uSize))
			return NULL;

		if (msg == NULL || uSize == 0){
			PY_RETURN_FALSE;
		}

		CApplication::GetInstance()->GetAsioService()->SendToClient(nettype, pid, proto_type, msg, uSize);

		PY_RETURN_TRUE;
	}

	//脚本控制连接服务器
	PyObject* SendMsgToServer(PyObject *self, PyObject *args)
	{
		int32 nettype = 0;
		uint8 proto_type = 0;
		char* msg = 0;
		uint32 uSize = 0;
		if (!PyArg_ParseTuple(args, "iBs#", &nettype, &proto_type, &msg, &uSize))
			return NULL;

		if (msg == NULL || uSize == 0){
			PY_RETURN_FALSE;
		}

		CApplication::GetInstance()->GetAsioService()->SendToServer(nettype, proto_type, msg, uSize);

		PY_RETURN_TRUE;
	}

	PyObject* GetFastTimeInSec(PyObject* self, PyObject* args)
	{
		return PyLong_FromUnsignedLongLong(common::GetFastUTCTimeInSec());
	}

	PyObject* GetFastTimeInMs(PyObject* self, PyObject* args)
	{
		return PyLong_FromUnsignedLongLong(common::GetFastUTCTimeInMS());
	}

	PyObject* GenMemStat(PyObject* self, PyObject* args)
	{
		CApplication::GetInstance()->GenMemStat();
		PY_RETURN_TRUE;
	}

	//初始化帧率
	PyObject* InitFrameRate(PyObject *self, PyObject *args)
	{
		uint8 uFrameRate = 0;
		if (!PyArg_ParseTuple(args, "B", &uFrameRate))
			return NULL;
		CApplication::GetInstance()->InitFrameRate(uFrameRate);
		PY_RETURN_TRUE;
	}

	//脚本写日志
	PyObject* Log(PyObject *self, PyObject *args)
	{
		int32 logtype = 0;
		char* szMsg = 0;
		char* szMod = 0;
		if (!PyArg_ParseTuple(args, "iss", &logtype, &szMsg, &szMod))
			return NULL;

		common::LogMod((common::LogLevel)logtype, szMod, "script | %s", szMsg);

		PY_RETURN_TRUE;
	}

	//注册脚本tick
	PyObject* RegTick(PyObject *self, PyObject *args)
	{
		int nCnt = -1;
		uint32 uInterval = 0;
		PyObject* pArgs = NULL;
		PyObject* pCallBack = NULL;
		if (!PyArg_ParseTuple(args, "OOI|i", &pCallBack, &pArgs, &uInterval, &nCnt))
			return NULL;
		CApplication::GetInstance()->RegScriptTick(pCallBack, pArgs, uInterval, nCnt);
		PY_RETURN_TRUE;
	}

	//删除脚本tick
	PyObject* DelTick(PyObject *self, PyObject *args)
	{
		PyObject* pCallBack = NULL;
		if (!PyArg_ParseTuple(args, "O", &pCallBack))
			return NULL;
		CApplication::GetInstance()->DelScriptTick(pCallBack);
		PY_RETURN_OK;
	}

	PyObject* GenCrash(PyObject *self, PyObject *args)
	{
		char* szMsg = 0;
		if (!PyArg_ParseTuple(args, "s", &szMsg))
			return NULL;
		CApplication::GetInstance()->GenErr(szMsg);
		PY_RETURN_OK;
	}

	//脚本控制连接服务器
	PyObject* OpenHeartBeat(PyObject *self, PyObject *args)
	{
		int32 sendTick = 0;
		int32 checkTick = 0;
		if (!PyArg_ParseTuple(args, "ii", &sendTick, &checkTick))
			return NULL;
		CApplication::GetInstance()->OpenHeartBeat(sendTick, checkTick);
		PY_RETURN_OK;
	}

	//脚本设置日志输出界别
	PyObject* SetLogLevel(PyObject *self, PyObject *args)
	{
		int32 logtype = 0;
		if (!PyArg_ParseTuple(args, "i", &logtype))
			return NULL;

		common::SetLogLevel((common::LogLevel)logtype);

		PY_RETURN_TRUE;
	}

	PyObject* PyGame_Init()
	{
		Py_InitModule((char*) "game", Scripting_Methods);
		script::AddIntConstToModule("LOG_LV_DEBUG", LOG_LV_DEBUG);
		script::AddIntConstToModule("LOG_LV_INFO", LOG_LV_INFO);
		script::AddIntConstToModule("LOG_LV_WARNING", LOG_LV_WARNING);
		script::AddIntConstToModule("LOG_LV_ERROR", LOG_LV_ERROR);
		return script::GetImportedModule("game");
	}
}