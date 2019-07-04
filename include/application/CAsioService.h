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
This is the wrapper of network related functions.
*/

#pragma once
#include "asio/asio.hpp"
#include "common/common.h"
#include "common/CBaseService.h"
#include "CNetServer.h"
#include "CNetClient.h"
#include <map>

using namespace common;

namespace application
{
	class CAsioService:public CBaseService
	{
	public:
		CAsioService();
		~CAsioService();

		void InitNetwork(int32 nettype, network::NetService::S_NCB* p_ncb);
		void InitClient(int32 nettype, network::NetClient::S_NCB_CLI* p_ncb_cli);

		void StartNetwork(int32 nettype, const char* ip, int32 port, uint16 limit_msg_num, uint8 limit_invalid_num, bool encrypt, int32 maxclients);
		void ConnectServer(int32 nettype, const char* szAddr, int32 port, bool encrypt, int32 retrytimes, int32 retrysec);
		void UninitNetwork(int32 nettype = -1);

		void SendToClient(int32 netType, uint32 pid, t_proto proto_type, const char* msg, size_t msglen);
		void SendToServer(int32 netType, t_proto proto_type, const char* msg, size_t msglen);

		CNetServer* GetNetServer(int32 nettype);
		CNetClient* GetNetClient(int32 nettype);

		size_t Poll();

		void HeartBeat();
		void CheckHeartBeat();

	private:
		std::map<int32, CNetServer*> m_NetServers;
		std::map<int32, CNetClient*> m_NetClients;
	};
}
