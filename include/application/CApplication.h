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
This is the base class of all applications, any app should derived from it.
*/

#pragma once
#include "common/common.h"
#include "python/Python.h"
#include "CAsioService.h"
#include "network/NetService.h"
#include "network/NetClient.h"
#include "common/TTickUserEx.h"
#include "signal.h"

using namespace common;

namespace common
{
	class CNewTimeSystem;
}

namespace application
{
	class CApplication :public TTickUserEx<CApplication>
	{
	protected:
		CApplication();
		virtual ~CApplication();
		static CApplication*& Inst();
		void OnHeartBeatTick();
		void OnCheckHeartBeatTick();

	public:
		static CApplication* GetInstance();
		void Init(const char* appName, const char* szConf, const char* szLog);
		int32 Run();
		void UnInit();
		void Quit();
		CNewTimeSystem* GetTimeSystem();
		CAsioService* GetAsioService();
		PyObject* GetPyObject();
		virtual void InitFrameRate(uint8 framerate);
		virtual void InitNcb();
		virtual void InitNcbClient();
		virtual void StartScript();
		virtual void StartNetwork(int32 nettype, const char* ip, int32 port, uint16 limit_msg_num, uint8 limit_invalid_num, bool encrypt = false, int32 maxclients = 5000);
		virtual void ConnectToServer(int32 nettype, const char* szAddr, int32 port, bool encrypt = false, int32 retrytimes = 0, int32 retrysec = 5);
		void OpenHeartBeat(int32 sendTick, int32 checkTick);
		void InitSignalHandler(void);
		void OnCatchSignal(int nSignal);
		void DispatchSignal(int nSignal);

		void OnException(std::exception &exp);
		void OnException(void);

		static void GenMemStat();
		static void Sleep(uint32 ms);
		static void GenErr(const char* szErr);
#ifndef _WIN32
		static void	SignalHandler(int nSignal);
		static void GenErrnoErr();
#else
		static BOOL WINAPI	SignalHandler(DWORD dwCtrlType);
#endif

		virtual void InitTimeSystem();
		virtual void UnInitTimeSystem();
		virtual void InitNetwork();
		virtual void InitScript(const char* szModuleName);
		virtual void InitLogger(const char* szLog);
		virtual void InitDir(const char* szNewDir);
		virtual void UnInitNetwork();
		virtual void UnInitScript();
		virtual void UnInitLogger();

		virtual void OnUpdate();
		virtual void OnLogicStart();
		virtual void OnFrameIdle(int32 uRestTime);

	protected:
		std::string m_strAppName;
		std::string m_strConfig;
		uint8 m_uFrameRate;
		uint32 m_uFrameTimeInMS;
		CNewTimeSystem* m_pTimeSys;
		CAsioService* m_pAsioService;
		PyObject* m_pyObject;
		bool m_bQuit;
		char m_szOldDir[512];
		network::NetService::S_NCB* m_pNcb;
		network::NetClient::S_NCB_CLI* m_pNcb_Cli;

#ifndef _WIN32
		struct sigaction m_sigaction;
#endif
		bool m_bIncomingSignal;
		int m_nSignal;
	};

	//以下是网络回调函数
	void connect_cb(NetService* ns, uint32 pid, std::string ip);
	void recv_cb(NetService* ns, uint32 pid, t_proto proto_type, std::shared_ptr<std::string> msg);
	void disconnect_cb(NetService* ns, uint32 pid);
	void connect_cb_cli(NetClient* nc, AsioConnection& conn);
	void connect_fail_cb_cli(NetClient* nc, std::string msg);
	void recv_cb_cli(NetClient* nc, uint32 pid, t_proto proto_type, std::shared_ptr<std::string> msg);
	void disconnect_cb_cli(NetClient* nc);
}

