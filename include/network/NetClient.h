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
This is the NetClient service based on asio's io_service and uses one thread to deal with
network events.
*/

#pragma once
#include <thread>
#include "asio/asio.hpp"
#include "BaseNetService.h"
#include "CClientConnection.h"
#include <memory>
#include <deque>
#include <unordered_set>
#include <chrono>

using asio::ip::tcp;

namespace network{

	class NetClient:public BaseNetService
	{
	public:

		typedef std::function<void(NetClient*, AsioConnection&)> t_on_connect_cb;
		typedef std::function<void(NetClient*, std::string)> t_on_connect_fail_cb;
		typedef std::function<void(NetClient*, uint32, t_proto, std::shared_ptr<std::string>)> t_on_recv_cb;
		typedef std::function<void(NetClient*)> t_on_disconnect_cb;

		typedef struct
		{
			t_on_connect_cb ccb;
			t_on_connect_fail_cb cfcb;
			t_on_recv_cb rcb;
			t_on_disconnect_cb dcb;
		}S_NCB_CLI;

		NetClient(asio::io_service& main_io, bool encrypt = false);
		virtual ~NetClient();

		virtual bool init(int32 nettype, t_on_connect_cb conn_cb, t_on_connect_fail_cb conn_fail_cb, t_on_recv_cb recv_cb, t_on_disconnect_cb discon_cb);

		bool connect(const char* szAddr, int port, bool encrypt = false, int32 retrytimes = 0, int32 retrysec = 5);
		bool disconnect();
		bool send(t_proto proto_type, const char* msg, size_t msglen);
		virtual void shutdown();
		virtual void on_connect_cb(AsioConnection& conn);
		virtual void on_connect_fail_cb(AsioConnection& conn, std::string errmsg);
		virtual void on_recvmsg_cb(AsioConnection& conn, t_proto proto_type, std::shared_ptr<std::string> msg);
		void on_disconnect_cb();
		virtual void do_close(AsioConnection& conn);
		int32 get_client_type();
		int32 get_retry_times();
		std::string& get_addr_str();
		uint16 get_port();
		void HeartBeat();

	private:
		bool do_connect();
		bool do_send(t_proto proto_type, const std::shared_ptr<std::string>& msg);

	private:
		std::shared_ptr<CClientConnection> conn_;
		t_on_connect_cb on_connect_cb_;
		t_on_connect_fail_cb on_connect_fail_cb_;
		t_on_recv_cb on_recvmsg_cb_;
		t_on_disconnect_cb on_disconnect_cb_;
		std::string m_addrStr;
		uint16 m_port;
		int32 m_tCli;
		int32 m_retrys;
		int32 m_retrysec;
	};

};
