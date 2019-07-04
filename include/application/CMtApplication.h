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
This is the base class of applications which need to use python's multithread support.
*/

#pragma once
#include "CApplication.h"

namespace application
{
	//提供脚本的多线程支持
	class CMtApplication :public CApplication
	{
	protected:
		CMtApplication();
		virtual ~CMtApplication();

	public:
		virtual void InitScript(const char* szModuleName);
		virtual void StartScript();
		virtual void UnInitScript();
		virtual void OnUpdate();
		virtual void InitNcb();
		virtual void InitNcbClient();

	};

	//以下是网络回调函数
	void mt_connect_cb(NetService* ns, uint32 pid, std::string ip);
	void mt_recv_cb(NetService* ns, uint32 pid, t_proto proto_type, std::shared_ptr<std::string> msg);
	void mt_disconnect_cb(NetService* ns, uint32 pid);
	void mt_connect_cb_cli(NetClient* nc, AsioConnection& conn);
	void mt_connect_fail_cb_cli(NetClient* nc, std::string msg);
	void mt_recv_cb_cli(NetClient* nc, uint32 pid, t_proto proto_type, std::shared_ptr<std::string> msg);
	void mt_disconnect_cb_cli(NetClient* nc);
}